#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build editorially selected quick references from exact licensed source blocks."""
import hashlib
import json
import pathlib
from import_translate_docs import FENCE, code_bodies

ROOT=pathlib.Path(__file__).resolve().parents[1]
BT=chr(96)

def fenced_blocks(text):
    active=None
    result=[]
    buf=[]
    language='text'
    for line in text.splitlines(keepends=True):
        match=FENCE.match(line)
        if active is None and match:
            active=(match.group(2)[0],len(match.group(2)))
            language=match.group(3).strip() or 'text'
            buf=[]
        elif active and match and match.group(2)[0]==active[0] and len(match.group(2))>=active[1]:
            result.append({'language':language,'body':''.join(buf)})
            active=None
        elif active:
            buf.append(line)
    return result

def main():
    imports=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
    registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
    specs=json.loads((ROOT/'catalog/cheatsheet-recipes.json').read_text(encoding='utf-8'))
    manifest={}
    for tool,spec in specs.items():
        record=imports[tool]
        doc=next(x for x in record['documents'] if x['source_path']==spec['source_path'])
        original=(ROOT/doc['original']).read_bytes()
        assert hashlib.sha256(original).hexdigest()==doc['source_sha256']
        blocks=fenced_blocks(original.decode('utf-8'))
        props={'title':tool+' — comandos essenciais upstream','type':'cheatsheet','tool':tool,
               'status':'source-checked','reviewed':'2026-10-26','language':'pt-BR',
               'tags':['cheatsheet','tool/'+tool],'cssclasses':['fieldbook'],
               'source_commit':record['commit'],'license_spdx':record['license_spdx'],
               'test_status':'not-executed','source_scope':'Selected exact upstream examples; not full documentation'}
        text='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in props.items())+'\n---\n\n'
        text+='# '+tool+' — comandos essenciais\n\n'
        text+='Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. '
        text+='Os blocos são transcritos sem alterações; títulos e organização são autorais em português. '
        text+='Esta folha complementa a documentação e não a substitui.\n\n'
        text+='> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. '
        text+='Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.\n\n'
        text+='## Navegação\n\n'
        text+='[Documentação offline]('+pathlib.PurePosixPath(doc['note']).name+') · [Acervo](../../01-Maps/documentacao-offline.md).\n\n'
        selected=[]
        for recipe in spec['recipes']:
            item=blocks[recipe['block']]
            body=item['body']
            assert body.endswith('\n'),'Non-terminated source code needs explicit handling'
            text+='## '+recipe['title']+'\n\n'+BT*3+item['language']+'\n'+body+BT*3+'\n\n'
            selected.append({'block':recipe['block'],'title':recipe['title'],
                             'sha256':hashlib.sha256(body.encode()).hexdigest()})
        text+='## Procedência\n\n'
        license_path='../../99-Assets/upstream/'+tool+'/LICENSE.txt'
        text+='- [Fonte oficial]('+next(x['source_url'] for x in registry[tool]['documents'] if x['path']==spec['source_path'])+').\n'
        text+='- [Licença da fonte: '+record['license_spdx']+']('+license_path+'). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.\n'
        text+='- Commit: '+BT+record['commit']+BT+'.\n'
        text+='- SHA-256 do documento original: '+BT+doc['source_sha256']+BT+'.\n'
        path=ROOT/'vault/02-Tools'/tool/(tool+'-cheatsheet-upstream.md')
        data=text.encode('utf-8')
        path.write_bytes(data)
        assert code_bodies(text)==[blocks[r['block']]['body'] for r in spec['recipes']]
        manifest[tool]={'note':path.relative_to(ROOT).as_posix(),'original':doc['original'],
                        'source_sha256':doc['source_sha256'],'note_sha256':hashlib.sha256(data).hexdigest(),
                        'recipes':selected,'command_execution_tested':False}
    (ROOT/'catalog/cheatsheet-provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    print(json.dumps({'cheatsheets':len(manifest),'exact_source_examples':sum(len(x['recipes']) for x in manifest.values()),
                      'examples_executed':False}))

if __name__=='__main__':
    main()
