#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read only whois help/version and exact installed manual bytes. No queries."""
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true')
    args=parser.parse_args()
    assert shutil.which('whois')
    source=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))['whois']
    doc=source['documents'][0]
    manual=pathlib.Path(doc['installed_path'])
    before=sha(manual.read_bytes())
    records=[]
    env=dict(os.environ,LC_ALL='C')
    env.pop('WHOIS_OPTIONS',None); env.pop('WHOIS_SERVER',None)
    with tempfile.TemporaryDirectory(prefix='whois-help-') as temp:
        for argv in [['whois','--help'],['whois','--version'],['dpkg-query','-W','-f='+chr(36)+'{Version}','whois']]:
            p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=15,cwd=temp,env=env)
            records.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode})
        empty=not list(pathlib.Path(temp).iterdir())
    after=sha(manual.read_bytes())
    imports=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    note=imports['whois']['documents'][0]
    pattern=r'(?<!\w)(--[a-z][a-z-]*|-[A-Za-z])(?=[\s,=<]|$)'
    flags=sorted(set(re.findall(pattern,' '.join(note['manual_structure']['option_syntax']))))
    installed=sorted(set(re.findall(pattern,records[0]['stdout'],re.M)))
    passed=all(r['exit_status']==0 for r in records) and bool(installed) and empty and before==after==doc['compressed_sha256'] and records[2]['stdout']==source['binary_version']
    result={'passed':passed,'binary':'whois','installed_version':'whois '+records[2]['stdout'],
        'test_status':'help-only','commands':records,'manual_options':flags,'installed_help_options':installed,
        'manual_options_not_listed_by_installed_help':sorted(set(flags)-set(installed)),
        'installed_help_options_not_in_manual':sorted(set(installed)-set(flags)),
        'source_manual_sha256':doc['sha256'],'test_script':'scripts/test_whois_help.py',
        'test_script_sha256':sha(pathlib.Path(__file__).read_bytes()),
        'temporary_directory_empty':empty,'installed_manual_before_sha256':before,
        'installed_manual_after_sha256':after,'installed_manual_unchanged':before==after,
        'network_query_requested':False,
        'verification_scope_pt':'Conferidas somente whois --help, whois --version e a versão dpkg; nenhum domínio, IP, servidor ou objeto foi consultado.',
        'limits':['This checks help/version and local source identity, not remote service behavior or query results.']}
    if args.record:
        for path in [ROOT/'evidence/whois-help-tests.json',ROOT/'vault/99-Assets/evidence/whois-help-tests.json']:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False,indent=2))
    return 0 if passed else 1
if __name__=='__main__': raise SystemExit(main())
