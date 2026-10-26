#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run bounded tests solely against an owned, temporary loopback fixture."""
import datetime
import hashlib
import http.server
import json
import pathlib
import platform
import shutil
import subprocess
import tempfile
import threading
import xml.etree.ElementTree as ET
from local_fixture import Handler

ROOT=pathlib.Path(__file__).resolve().parents[1]
records=[]
def run(argv):
    p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=45,cwd=ROOT)
    records.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode})
    if p.returncode:
        raise RuntimeError('Command failed: '+repr(argv))
    return p

assert shutil.which('nmap') and shutil.which('ffuf'), 'Installations are prerequisites; this script installs nothing.'
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=server.serve_forever,daemon=True)
thread.start()
port=server.server_address[1]
checks=[]
error=None
try:
    run(['nmap','--version'])
    run(['ffuf','-V'])
    with tempfile.TemporaryDirectory(prefix='fieldbook-pilot-') as temp:
        xml=str(pathlib.Path(temp)/'nmap.xml')
        run(['nmap','-sT','-Pn','-n','-p',str(port),'-oX',xml,'127.0.0.1'])
        tree=ET.parse(xml)
        checks.append({'check':'Nmap sees owned fixture port open',
                       'pass':tree.find('.//port/state').attrib['state']=='open'})
        output=str(pathlib.Path(temp)/'ffuf.json')
        wordlist=ROOT/'vault/99-Assets/fixtures/paths.txt'
        run(['ffuf','-noninteractive','-w',str(wordlist),'-u','http://127.0.0.1:'+str(port)+'/FUZZ',
             '-mc','200','-t','1','-rate','5','-of','json','-o',output])
        results=json.loads(pathlib.Path(output).read_text())['results']
        actual=sorted(r['input']['FUZZ'] for r in results)
        checks.append({'check':'ffuf matches admin and health, excludes missing',
                       'pass':actual==['admin','health'],'observed':actual})
except Exception as e:
    error=repr(e)
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)

passed=not error and len(checks)==2 and all(x['pass'] for x in checks)
result={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.system(),
        'target':'127.0.0.1 owned synthetic HTTP fixture','port':port,'passed':passed,'checks':checks,
        'commands':records,'error':error,'fixture_closed':True,
        'limits':['Only tool versions, one TCP connect/XML result and one bounded ffuf JSON recipe were executed.',
                  'Other cheatsheet commands, GUI appearance, Internet/VPN and complete manuals were not tested.']}
raw_json=json.dumps(result,ensure_ascii=False,indent=2)
result['evidence_format']='Path-normalized public evidence; machine-specific project/temp paths replaced.'
result['raw_evidence_sha256']=hashlib.sha256(raw_json.encode()).hexdigest()
normalized=json.dumps(result,ensure_ascii=False,indent=2).replace(str(ROOT),'<PROJECT_ROOT>')
if 'temp' in locals():
    normalized=normalized.replace(temp,'<TEST_DIR>')
result=json.loads(normalized)
out=ROOT/'evidence'
out.mkdir(exist_ok=True)
(out/'local-tests.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
asset=ROOT/'vault/99-Assets/evidence'
asset.mkdir(parents=True,exist_ok=True)
(asset/'local-tests.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
print(json.dumps({'passed':passed,'checks':checks,'commands':len(records),'fixture_closed':True,'error':error},ensure_ascii=False,indent=2))
raise SystemExit(0 if passed else 1)
