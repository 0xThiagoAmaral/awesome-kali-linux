#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Query help/version only, checking that the local OUI files are not modified."""
import argparse,hashlib,json,pathlib,re,shutil,subprocess,tempfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA_FILES=[pathlib.Path('/usr/share/arp-scan/ieee-oui.txt'),pathlib.Path('/etc/arp-scan/mac-vendor.txt')]

def snapshots():
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in DATA_FILES if p.is_file()}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true',help='Maintainer action: replace frozen evidence')
    args=parser.parse_args()
    assert shutil.which('get-oui') and shutil.which('arp-scan'),'Tools must already be installed.'
    before=snapshots(); records=[]
    with tempfile.TemporaryDirectory(prefix='get-oui-help-') as temp:
        for argv in [['get-oui','-h'],['arp-scan','--version']]:
            p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=15,cwd=temp)
            records.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode})
        empty=not list(pathlib.Path(temp).iterdir())
    after=snapshots()
    imports=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    doc=next(d for d in imports['arp-scan']['documents'] if d['source_path']=='get-oui.1.dist')
    flags=sorted({re.match(r'-[a-z]',s).group() for s in doc['manual_structure']['option_syntax']})
    installed=sorted(set(re.findall(r'^\s+(-[a-z])\b',records[0]['stdout'],re.M)))
    passed=all(r['exit_status']==0 for r in records) and bool(installed) and empty and before==after
    result={'passed':passed,'binary':'get-oui','installed_version':records[1]['stdout'].splitlines()[0],
            'version_scope':'Version of the arp-scan package binary; get-oui help does not report its own version',
            'test_status':'help-only','commands':records,'manual_options':flags,'installed_help_options':installed,
            'manual_options_not_listed_by_installed_help':sorted(set(flags)-set(installed)),
            'installed_help_options_not_in_manual':sorted(set(installed)-set(flags)),
            'source_manual_sha256':doc['source_sha256'],'test_script':'scripts/test_get_oui_help.py',
            'test_script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'verification_scope_pt':'Conferidas somente get-oui -h e a versão do pacote arp-scan; nenhuma atualização IEEE foi solicitada.',
            'download_operation_requested':False,'temporary_directory_empty':empty,
            'system_data_before_sha256':before,'system_data_after_sha256':after,'system_data_unchanged':before==after,
            'limits':['Help/version only; registry download, backup and conversion operations were not exercised.']}
    if args.record:
        for path in [ROOT/'evidence/get-oui-help-tests.json',ROOT/'vault/99-Assets/evidence/get-oui-help-tests.json']:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'commands','system_data_before_sha256','system_data_after_sha256'}},ensure_ascii=False,indent=2))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
