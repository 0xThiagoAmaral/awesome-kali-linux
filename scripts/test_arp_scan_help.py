#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare the installed main-tool help with the source manual; no targets supplied."""
import argparse,hashlib,json,pathlib,re,shutil,subprocess

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true',help='Maintainer action: replace frozen evidence')
    args=parser.parse_args()
    assert shutil.which('arp-scan'),'arp-scan must already be installed.'
    records=[]
    for argv in [['arp-scan','--help'],['arp-scan','--version']]:
        p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=15)
        records.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode})
    imports=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    doc=next(d for d in imports['arp-scan']['documents'] if d['source_path']=='arp-scan.1.dist')
    flags=sorted(set(re.findall(r'--[a-z][a-z0-9-]*',' '.join(doc['manual_structure']['option_syntax']))))
    installed=sorted(set(re.findall(r'^\s*(--[a-z][a-z0-9-]*)',records[0]['stdout'],re.M)))
    passed=all(r['exit_status']==0 for r in records) and bool(installed)
    result={'passed':passed,'binary':'arp-scan','installed_version':records[1]['stdout'].splitlines()[0],
            'test_status':'help-only','commands':records,'manual_options':flags,'installed_help_options':installed,
            'manual_options_not_listed_by_installed_help':sorted(set(flags)-set(installed)),
            'installed_help_options_not_in_manual':sorted(set(installed)-set(flags)),
            'source_manual_sha256':doc['source_sha256'],'test_script':'scripts/test_arp_scan_help.py',
            'test_script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'verification_scope_pt':'Conferidas somente --help e --version; nenhum alvo foi informado e nenhuma receita de varredura foi executada.',
            'network_target_passed':False,'local_discovery_requested':False,
            'limits':['Help/version only; no validation of live ARP responses, timing, privileges, interfaces or packet changes.']}
    if args.record:
        for path in [ROOT/'evidence/arp-scan-main-tests.json',ROOT/'vault/99-Assets/evidence/arp-scan-main-tests.json']:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'commands','manual_options','installed_help_options'}},ensure_ascii=False,indent=2))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
