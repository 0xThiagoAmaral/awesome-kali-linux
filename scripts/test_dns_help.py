#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Help/version only for installed DNS tools. Accepts no domain or scan target."""
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
FLAG_PATTERN=r'(?<![\w-])(--[a-z][a-z0-9_-]*|-[A-Za-z][A-Za-z0-9]*|-[0-9])(?=[\s,=<]|$)'
def extract_help_flags(text):
    declarations=[]
    for line in text.splitlines():
        if re.match(r'^\s*(?:--[a-z][a-z0-9_-]*|-[A-Za-z][A-Za-z0-9]*|-[0-9])(?=[,\s]|$)',line):
            declarations.append(line.split('\t',1)[0])
    return sorted(set(re.findall(FLAG_PATTERN,'\n'.join(declarations),re.M)))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--tool',required=True,choices=['dnsenum','dnsrecon'])
    parser.add_argument('--record',action='store_true')
    args=parser.parse_args();tool=args.tool
    assert shutil.which(tool)
    record=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))[tool]
    doc=record['documents'][0]
    manual=pathlib.Path(doc['installed_path'])
    before=sha(manual.read_bytes());commands=[]
    argv_list=[[tool,'--help'],[tool,'-h']]
    if tool=='dnsrecon':argv_list.append([tool,'-V'])
    argv_list.append(['dpkg-query','-W','-f='+chr(36)+'{Version}',tool])
    env=dict(os.environ,LC_ALL='C',PYTHONDONTWRITEBYTECODE='1',NO_COLOR='1')
    with tempfile.TemporaryDirectory(prefix=tool+'-help-') as temp:
        for argv in argv_list:
            p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=30,cwd=temp,env=env)
            expected=1 if tool=='dnsenum' and argv[0]==tool else 0
            commands.append({'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'exit_status':p.returncode,'expected_exit_status':expected})
        empty=not list(pathlib.Path(temp).iterdir())
    after=sha(manual.read_bytes())
    entry=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))[tool]['documents'][0]
    flags=sorted(set(re.findall(FLAG_PATTERN,' '.join(entry['manual_structure']['option_syntax']))))
    output=commands[0]['stdout']+commands[0]['stderr']
    plain=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',output)
    installed=extract_help_flags(plain)
    help_shown='usage:' in plain.lower() and '--help' in installed
    passed=all(c['exit_status']==c['expected_exit_status'] for c in commands) and help_shown and empty and before==after==doc['compressed_sha256'] and commands[-1]['stdout']==record['binary_version']
    scope='Conferidas somente as duas formas de ajuda, versão do pacote'+(' e dnsrecon -V' if tool=='dnsrecon' else '')+'. Nenhum domínio, endereço, servidor DNS ou alvo foi fornecido; nenhuma consulta de enumeração foi solicitada.'
    if tool=='dnsenum':
        scope+=' A ajuda retorna código 1. Manual e banner do executável dizem 1.3.1; a versão dpkg é '+record['binary_version']+'. O manual descreve --enum como --threads 5 -s 20 -w e --pages padrão 20; a ajuda instalada mostra -s 15 e padrão 5 páginas. Os textos de origem não foram alterados, e esses padrões não foram testados em consultas reais.'
    result={'passed':passed,'binary':tool,'installed_version':tool+' '+commands[-1]['stdout'],
        'test_status':'help-only','commands':commands,'manual_options':flags,'installed_help_options':installed,
        'manual_options_not_listed_by_installed_help':sorted(set(flags)-set(installed)),
        'installed_help_options_not_in_manual':sorted(set(installed)-set(flags)),
        'source_manual_sha256':doc['sha256'],'test_script':'scripts/test_dns_help.py','test_script_sha256':sha(pathlib.Path(__file__).read_bytes()),
        'temporary_directory_empty':empty,'installed_manual_before_sha256':before,'installed_manual_after_sha256':after,
        'installed_manual_unchanged':before==after,'network_query_requested':False,'target_supplied':False,
        'verification_scope_pt':scope,'help_header_lines':[s for s in plain.splitlines() if s.strip()][:5],
        'limits':['Help/version only; no DNS, AXFR, brute force, third-party search or Whois operation tested.',
                  'Option-name comparison does not demonstrate that all option combinations or backends work.']}
    if tool=='dnsenum':
        enum_match='Shortcut option equivalent to --threads 5 -s 15 -w.' in plain
        pages_match='the default is 5 pages' in plain
        version_match=re.search(r'dnsenum VERSION:([^\s]+)',plain)
        result['binary_reported_version']=version_match.group(1) if version_match else None
        result['documented_default_discrepancies']={'enum':{'manual':'--threads 5 -s 20 -w','installed_help':'--threads 5 -s 15 -w','observed_in_help':enum_match},
            'pages':{'manual':20,'installed_help':5,'observed_in_help':pages_match},'query_behavior_tested':False}
        result['passed']=passed=passed and enum_match and pages_match and bool(version_match)
    if args.record:
        for path in [ROOT/'evidence'/(tool+'-help-tests.json'),ROOT/'vault/99-Assets/evidence'/(tool+'-help-tests.json')]:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False,indent=2))
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
