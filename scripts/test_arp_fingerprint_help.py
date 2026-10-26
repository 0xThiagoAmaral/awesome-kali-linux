#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Inspect installed help/version only; never pass a target or request ARP discovery."""
import argparse,hashlib,json,pathlib,re,shutil,subprocess

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true',help='Maintainer action: replace frozen evidence')
    args=parser.parse_args()
    assert shutil.which('arp-fingerprint') and shutil.which('arp-scan'),'Prerequisites must already be installed.'
    records=[]
    for argv in [['arp-fingerprint','-h'],['arp-scan','--version']]:
        p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=15)
        records.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode})
    manifest=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    doc=next(d for d in manifest['arp-scan']['documents'] if d['source_path']=='arp-fingerprint.1')
    manual_flags=sorted({re.match(r'-[a-z]',s).group() for s in doc['manual_structure']['option_syntax']})
    help_flags=sorted(set(re.findall(r'^\s+(-[a-z])\b',records[0]['stdout'],re.M)))
    passed=all(r['exit_status']==0 for r in records) and 'Usage: arp-fingerprint' in records[0]['stdout'] and bool(help_flags)
    result={'passed':passed,'binary':'arp-fingerprint','installed_version':records[1]['stdout'].splitlines()[0],
            'version_scope':'Version of the arp-scan package binary; arp-fingerprint help does not report its own version',
            'test_status':'help-only','commands':records,
            'manual_options':manual_flags,'installed_help_options':help_flags,
            'manual_options_not_listed_by_installed_help':sorted(set(manual_flags)-set(help_flags)),
            'installed_help_options_not_in_manual':sorted(set(help_flags)-set(manual_flags)),
            'source_manual_sha256':doc['source_sha256'],
            'test_script':'scripts/test_arp_fingerprint_help.py',
            'test_script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'verification_scope_pt':'Conferidas somente a ajuda do arp-fingerprint e a versão do pacote arp-scan; nenhum alvo foi informado e a opção -l não foi executada.',
            'network_target_passed':False,'local_discovery_requested':False,
            'limits':['Help/version only; does not validate live fingerprint results, interfaces, privileges or every option.']}
    if args.record:
        for path in [ROOT/'evidence/arp-scan-local-tests.json',ROOT/'vault/99-Assets/evidence/arp-scan-local-tests.json']:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False,indent=2))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
