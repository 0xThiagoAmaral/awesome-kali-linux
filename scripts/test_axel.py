#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Test the installed Axel solely against a temporary owned loopback fixture."""
import hashlib
import argparse
import http.server
import json
import pathlib
import re
import shutil
import subprocess
import tempfile
import threading

ROOT=pathlib.Path(__file__).resolve().parents[1]
PAYLOAD=bytes(range(256))*256
REQUESTS=[]
RECORDS=[]

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args):
        pass
    def respond(self,body):
        if self.path!='/fixture.bin':
            self.send_error(404)
            return
        start,end=0,len(PAYLOAD)-1
        value=self.headers.get('Range')
        if value:
            match=re.fullmatch(r'bytes=(\d+)-(\d*)',value)
            if not match:
                self.send_error(416)
                return
            start=int(match.group(1))
            end=min(end,int(match.group(2))) if match.group(2) else end
            if start>end:
                self.send_error(416)
                return
        REQUESTS.append({'method':self.command,'range':value,
                         'user_agent':self.headers.get('User-Agent'),
                         'custom_header':self.headers.get('X-Fieldbook')})
        self.send_response(206 if value else 200)
        self.send_header('Accept-Ranges','bytes')
        self.send_header('Content-Type','application/octet-stream')
        self.send_header('Content-Length',str(end-start+1))
        if value:
            self.send_header('Content-Range',f'bytes {start}-{end}/{len(PAYLOAD)}')
        self.end_headers()
        if body:
            try:
                self.wfile.write(PAYLOAD[start:end+1])
            except (BrokenPipeError,ConnectionResetError):
                pass
    def do_HEAD(self):
        self.respond(False)
    def do_GET(self):
        self.respond(True)

def run(argv,require_success=True):
    process=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=20)
    RECORDS.append({'argv':argv,'stdout':process.stdout,'stderr':process.stderr,'exit_status':process.returncode})
    if require_success and process.returncode:
        raise RuntimeError('Axel command returned '+str(process.returncode))
    return process

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true',help='Maintainer action: replace the frozen public evidence files')
    args=parser.parse_args()
    assert shutil.which('axel'),'Axel must already be installed; this test installs nothing.'
    checks=[]
    error=None
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    server.daemon_threads=True
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    port=server.server_address[1]
    temp_name=None
    try:
        version=run(['axel','--version']).stdout.splitlines()[0]
        help_output=run(['axel','--help']).stdout
        with tempfile.TemporaryDirectory(prefix='fieldbook-axel-') as temp:
            temp_name=temp
            target=pathlib.Path(temp)/'download.bin'
            url=f'http://127.0.0.1:{port}/fixture.bin'
            first=run(['axel','-q','-n','2','-s','131072','-T','5',
                       '-H','X-Fieldbook: offline-fixture','-U','Fieldbook-Axel-Test',
                       '-o',str(target),url])
            actual=hashlib.sha256(target.read_bytes()).hexdigest()
            expected=hashlib.sha256(PAYLOAD).hexdigest()
            checks.append({'check':'Downloaded bytes match the owned fixture exactly','pass':actual==expected,
                           'bytes':target.stat().st_size,'sha256':actual})
            checks.append({'check':'Quiet mode stdout is empty','pass':first.stdout==''})
            checks.append({'check':'Custom header and user-agent reached the fixture',
                           'pass':any(r['custom_header']=='offline-fixture' and r['user_agent']=='Fieldbook-Axel-Test' for r in REQUESTS)})
            second=run(['axel','-c','-q','-o',str(target),url],require_success=False)
            checks.append({'check':'No-clobber preserves the existing complete file',
                           'pass':target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==expected,
                           'observed_exit_status':second.returncode})
            checks.append({'check':'No state file remains after successful download',
                           'pass':not pathlib.Path(str(target)+'.st').exists()})
    except Exception as exc:
        error=type(exc).__name__+': '+str(exc)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    registry=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    doc=next(x for x in registry['axel']['documents'] if x['source_path']=='doc/axel.txt')
    manual_flags=sorted({re.match(r'--[a-z0-9-]+',x).group() for x in doc['manual_structure']['option_syntax']})
    installed_flags=sorted(set(re.findall(r'^--[a-z0-9-]+',locals().get('help_output',''),re.M)))
    result={'passed':error is None and len(checks)==5 and all(x['pass'] for x in checks),
            'installed_version':locals().get('version'),'fixture':'Owned 127.0.0.1 HTTP server; no Internet requests',
            'fixture_port':port,'fixture_closed':not thread.is_alive(),'checks':checks,'commands':RECORDS,
            'requests':REQUESTS,'source_manual_sha256':doc['source_sha256'],
            'test_script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'manual_long_options':manual_flags,'installed_help_long_options':installed_flags,
            'manual_options_not_listed_by_installed_help':sorted(set(manual_flags)-set(installed_flags)),
            'installed_help_options_not_in_manual':sorted(set(installed_flags)-set(manual_flags)),
            'error':error,'limits':['Only version/help, one local range-capable HTTP download and no-clobber were exercised.',
                                    'Not a test of external URLs, TLS, proxies, FTP, GUI or every option.',
                                    'Documentation remains faithful to its pinned source even when installed flags differ.']}
    text=json.dumps(result,ensure_ascii=False,indent=2).replace(str(ROOT),'<PROJECT_ROOT>')
    if temp_name:
        text=text.replace(temp_name,'<TEST_DIR>')
    if args.record:
        for path in [ROOT/'evidence/axel-local-tests.json',ROOT/'vault/99-Assets/evidence/axel-local-tests.json']:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(text+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['commands','requests','manual_long_options','installed_help_long_options']},ensure_ascii=False,indent=2))
    return 0 if result['passed'] else 1

if __name__=='__main__':
    raise SystemExit(main())
