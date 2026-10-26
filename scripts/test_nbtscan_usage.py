#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Capture nbtscan usage with no arguments. No scan target or packet operation."""
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true')
    args=parser.parse_args()
    assert shutil.which('nbtscan')
    record=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))['nbtscan']
    doc=record['documents'][0]
    manual=pathlib.Path(doc['installed_path'])
    before=sha(manual.read_bytes())
    commands=[]
    with tempfile.TemporaryDirectory(prefix='nbtscan-usage-') as temp:
        for argv,expected in [(['nbtscan'],2),(['dpkg-query','-W','-f='+chr(36)+'{Version}','nbtscan'],0)]:
            p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=15,cwd=temp,env=dict(os.environ,LC_ALL='C'))
            commands.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode,'expected_exit_status':expected})
        empty=not list(pathlib.Path(temp).iterdir())
    after=sha(manual.read_bytes())
    manifest=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    entry=manifest['nbtscan']['documents'][0]
    pattern=r'(?<!\w)(--[a-z][a-z-]*|-[A-Za-z])(?=[\s,=<]|$)'
    flags=sorted(set(re.findall(pattern,' '.join(entry['manual_structure']['option_syntax']))))
    usage=commands[0]['stdout']+commands[0]['stderr']
    installed=sorted(set(re.findall(pattern,usage,re.M)))
    observed_timeout='wait timeout milliseconds for response.' in usage and 'Default 1000.' in usage
    passed=all(c['exit_status']==c['expected_exit_status'] for c in commands) and bool(installed) and empty and before==after==doc['compressed_sha256'] and commands[1]['stdout']==record['binary_version'] and observed_timeout
    result={'passed':passed,'binary':'nbtscan','installed_version':'nbtscan '+commands[1]['stdout'],
        'test_status':'usage-only','commands':commands,'manual_options':flags,'installed_help_options':installed,
        'manual_options_not_listed_by_installed_help':sorted(set(flags)-set(installed)),
        'installed_help_options_not_in_manual':sorted(set(installed)-set(flags)),
        'source_manual_sha256':doc['sha256'],'test_script':'scripts/test_nbtscan_usage.py',
        'test_script_sha256':sha(pathlib.Path(__file__).read_bytes()),'temporary_directory_empty':empty,
        'installed_manual_before_sha256':before,'installed_manual_after_sha256':after,'installed_manual_unchanged':before==after,
        'packet_send_operation_requested':False,'scan_target_supplied':False,
        'timeout_documentation_discrepancy':{'manual_unit':'seconds','manual_default':1,'installed_usage_unit':'milliseconds','installed_usage_default':1000,'observed_in_usage':observed_timeout,'network_behavior_tested':False},
        'verification_scope_pt':'Executado nbtscan sem argumentos: código 2 de uso capturado pelo subprocesso, sem alvo; -h significa nomes de serviços, não ajuda. Há divergência em -t: o manual diz segundos/padrão 1; a mensagem instalada diz milissegundos/padrão 1000. A tradução preserva o manual e registra a divergência; nenhum envio ou tempo de resposta de rede foi testado.',
        'limits':['Usage/version metadata only; no scan, no target, no remote queries; timeout unit compared between documentation texts, not measured.']}
    if args.record:
        for path in [ROOT/'evidence/nbtscan-help-tests.json',ROOT/'vault/99-Assets/evidence/nbtscan-help-tests.json']:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False,indent=2))
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
