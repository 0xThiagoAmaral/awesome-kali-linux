#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Help/version only. No active scan, passive capture, interface or target input."""
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,tempfile
from test_dns_help import FLAG_PATTERN,extract_help_flags
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--binary',required=True,choices=['netdiscover','fping','fping6'])
    parser.add_argument('--record',action='store_true')
    args=parser.parse_args();binary=args.binary
    tool='fping' if binary.startswith('fping') else binary
    registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
    record=registry[tool]
    doc=next(d for d in record['documents'] if d.get('binary',tool)==binary)
    path=shutil.which(binary);assert path,'Binary must already be installed'
    manual=pathlib.Path(doc['installed_path']);before=sha(manual.read_bytes())
    commands=[]
    selected=[[binary,'-h']]+([[binary,'-v']] if tool=='fping' else [])
    selected.append(['dpkg-query','-W','-f='+chr(36)+'{Version}',tool])
    with tempfile.TemporaryDirectory(prefix=binary+'-help-') as temporary:
        env=dict(os.environ,LC_ALL='C',HOME=temporary)
        for argv in selected:
            p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=15,cwd=temporary,env=env)
            expected=1 if binary=='netdiscover' and argv[0]==binary else 0
            commands.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode,'expected_exit_status':expected})
        empty=not list(pathlib.Path(temporary).iterdir())
    after=sha(manual.read_bytes())
    imported=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    entry=next(d for d in imported[tool]['documents'] if d['source_path']==doc['path'])
    flags=sorted(set(re.findall(FLAG_PATTERN,' '.join(entry['manual_structure']['option_syntax']))))
    usage=commands[0]['stdout']+commands[0]['stderr']
    installed=extract_help_flags(usage)
    passed=all(c['exit_status']==c['expected_exit_status'] for c in commands) and 'usage:' in usage.lower() and bool(installed) and empty and before==after==doc['compressed_sha256'] and commands[-1]['stdout']==record['binary_version']
    scope='Conferida somente a ajuda -h'+(' e a versão -v' if tool=='fping' else ' (código 1 observado)')+' e a versão dpkg. HOME temporário, nenhum alvo ou interface fornecido; nenhuma operação de envio, varredura ou captura foi solicitada. Ausência de uma opção na ajuda não demonstra sua rejeição pelo programa.'
    result={'passed':passed,'binary':binary,'installed_version':binary+'; pacote '+tool+' '+commands[-1]['stdout'],
        'test_status':'help-only','commands':commands,'manual_options':flags,'installed_help_options':installed,
        'manual_options_not_listed_by_installed_help':sorted(set(flags)-set(installed)),
        'installed_help_options_not_in_manual':sorted(set(installed)-set(flags)),
        'source_manual_sha256':doc['sha256'],'test_script':'scripts/test_network_help.py','test_script_sha256':sha(pathlib.Path(__file__).read_bytes()),
        'temporary_directory_empty':empty,'temporary_home_used':True,'installed_manual_before_sha256':before,
        'installed_manual_after_sha256':after,'installed_manual_unchanged':before==after,
        'target_supplied':False,'packet_send_operation_requested':False,'packet_capture_requested':False,
        'verification_scope_pt':scope,
        'limits':['Help/version and file identity only, no ICMP/ARP traffic or capture behavior tested.',
                  'Historical manual options/defaults preserved even when help differs.']}
    if binary=='fping6':
        main_path=shutil.which('fping');alias=pathlib.Path(path)
        relation={'executable':path,'is_symlink':alias.is_symlink(),'symlink_target':os.readlink(path) if alias.is_symlink() else None,
                  'same_resolved_executable_as_fping':bool(main_path) and alias.resolve()==pathlib.Path(main_path).resolve(),
                  'manual_is_separate_page':True}
        result['compatibility_relationship']=relation
        result['passed']=passed=passed and relation['is_symlink'] and relation['same_resolved_executable_as_fping']
        result['compatibility_summary_pt']='Confirmado que fping6 é link simbólico para o executável fping nesta instalação. A página de compatibilidade não lista opções; a listagem do executável não foi tratada como opções omitidas dessa página. Somente ajuda e versão foram executadas, sem alvo.'
    if args.record:
        for target in [ROOT/'evidence'/(binary+'-help-tests.json'),ROOT/'vault/99-Assets/evidence'/(binary+'-help-tests.json')]:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False,indent=2))
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
