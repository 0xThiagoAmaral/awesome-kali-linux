#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Refresh honest coverage, navigation, licensing and reader instructions."""
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/update_documentation_coverage.py')],check=True)
imports=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8'))
sources=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
coverage=json.loads((ROOT/'catalog/documentation-coverage.json').read_text(encoding='utf-8'))
sheet_path=ROOT/'catalog/cheatsheet-provenance.json'
sheets=json.loads(sheet_path.read_text(encoding='utf-8')) if sheet_path.exists() else {}
pub_path=ROOT/'catalog/publication.json'
publication=json.loads(pub_path.read_text(encoding='utf-8')) if pub_path.exists() else {}
publication_status='[Publicado na branch main]('+publication['repository']+') — marco verificado em '+publication['verified_date'] if publication.get('published') else 'Pendente de autenticação e envio'
documents=[d for x in imports.values() for d in x['documents']]
native=sum(d.get('translation_method')=='upstream-portuguese' for d in documents)
machine=len(documents)-native
blocks=sum(d['source_fenced_blocks'] for d in documents)

def put(path,text):
    p=ROOT/path
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes((text.strip()+'\n').encode('utf-8'))

cc=ROOT/'LICENSES/CC-BY-SA-4.0.txt'
if cc.exists():
    (ROOT/'LICENSE').write_bytes(cc.read_bytes())
mit="""MIT License

Copyright (c) 2026 Awesome Kali Linux contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
put(pathlib.Path('LICENSES/MIT.txt'),mit)
put(pathlib.Path('LICENSE-POLICY.md'),"""# Licenças

- Curadoria, guias, templates e textos autorais do projeto: CC BY-SA 4.0.
- Scripts autorais em scripts/: MIT.
- Documentação, traduções e assets upstream: licença de sua fonte, registrada por nota e no catálogo.

A licença geral não substitui licenças de terceiros. Os originais e avisos estão em sources/upstream/
e vault/99-Assets/upstream/. Traduções de material upstream preservam as condições e atribuições da fonte.
Não se atribui automaticamente CC BY-SA a arquivos MIT, Apache ou AGPL de terceiros.

O corpus oficial Kali continua com redistribuição integral não confirmada; não está sendo republicado
sob uma licença inventada. O registro source-registry documenta somente fontes verificadas.

[CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) · [MIT dos scripts](LICENSES/MIT.txt) ·
[Atribuições de terceiros](THIRD_PARTY.md).""")
put(pathlib.Path('THIRD_PARTY.md'),"""# Fontes e atribuições

O repositório contém notas autorais e documentação upstream licenciada. Cada importação registra
repositório, commit, URL, hash de origem, licença, método de tradução e modificações de apresentação.
Original e tradução são arquivos distintos; código e saídas literais não são traduzidos silenciosamente.

- catalog/source-registry.json: direitos e arquivos adquiridos.
- catalog/imported-documentation.json: notas realmente geradas, hashes e integridade.
- sources/upstream/: originais preservados e avisos de licença.
- vault/99-Assets/upstream/: imagens licenciadas e textos de licença necessários à leitura.

Traduções automáticas são identificadas e continuam aguardando revisão humana. O arquivo oficial
em português é identificado separadamente quando o próprio upstream o disponibiliza.
A existência de README adquirido não comprova cobertura integral de wiki, manual ou site externo.

Dependências e modelo de tradução ficam fora do repositório publicável. Nenhum executável das
ferramentas Kali ou modelo de tradução é redistribuído neste pacote.""")
lines=['---','title: "Documentação offline — acervo"','type: "moc"','status: "source-checked"',
       'reviewed: "2026-10-26"','tags: ["documentation", "offline"]','---','',
       '# Documentação offline — acervo','',
       f'**{len(imports)} ferramentas com notas importadas; {len(documents)} documentos disponíveis.**',
       f'{machine} traduções automáticas e {native} fonte(s) oficial(is) em português. Revisão humana completa: pendente.',
       '',
       'Estas páginas preservam a documentação adquirida, não substituem manuais não incluídos. O catálogo completo tem 820 registros.',
       '',
       '| Ferramenta | Documentos locais | Consulta rápida | Licença da fonte | Situação |','|---|---|---|---|---|']
for tool,record in sorted(imports.items()):
    links=[]
    for doc in record['documents']:
        rel=pathlib.Path(doc['note']).relative_to('vault').as_posix()
        links.append('['+doc['source_path']+'](../'+rel+')')
    sheet='[Comandos essenciais](../'+pathlib.Path(sheets[tool]['note']).relative_to('vault').as_posix()+')' if tool in sheets else 'Pendente'
    lines.append('| '+tool+' | '+' · '.join(links)+' | '+sheet+' | '+record['license_spdx']+' | Revisão pendente |')
put(pathlib.Path('vault/01-Maps/documentacao-offline.md'),'\n'.join(lines))
home=ROOT/'vault/00-Home.md'
text=home.read_text(encoding='utf-8')
if '(01-Maps/documentacao-offline.md)' not in text:
    text+='\n## Documentação upstream offline\n\n[Consultar o acervo importado](01-Maps/documentacao-offline.md).\n'
home.write_bytes(text.encode('utf-8'))
put(pathlib.Path('docs/COBERTURA.md'),f"""# Cobertura real

| Critério | Estado observado |
|---|---|
| Catálogo oficial | 820 registros; 806 com metadado everything |
| Fontes upstream licenciadas adquiridas | {len(sources)} ferramentas |
| Notas de documentação disponíveis | {len(documents)} documentos em {len(imports)} ferramentas |
| Traduções automáticas | {machine} documentos, ainda sem revisão humana integral |
| Português oficial upstream | {native} documento(s) |
| Blocos de código preservados | {blocks}, sujeitos à conferência de integridade atual |
| Folhas de comandos upstream | {len(sheets)} folhas; {sum(len(x['recipes']) for x in sheets.values())} exemplos literais, não executados |
| Ferramentas com documentação integral e revisão concluídas | 0 |
| Todo o Kali full/everything concluído | Não |
| Publicação GitHub | {publication_status} |

O acervo está em expansão. README, notas-piloto, links e pastas não são contados como manual completo.
As pendências individuais e critérios de aceite estão em catalog/documentation-coverage.json.
O trabalho continua mirando todo o catálogo, com metadados everything separados, sem reduzir a meta.
""")
readme=ROOT/'README.md'
text=readme.read_text(encoding='utf-8')
marker='\n## Documentação offline — andamento\n'
text=text.split(marker)[0].rstrip()
text=text.replace('A licença do projeto permanece uma decisão explícita antes da publicação; licenças de terceiros são independentes.',
                  'Curadoria e notas autorais: CC BY-SA 4.0; scripts: MIT. Conteúdos upstream mantêm suas próprias licenças e avisos.')
text+=marker+f"""

Já há **{len(documents)} documentos de {len(imports)} ferramentas** no
[acervo offline](vault/01-Maps/documentacao-offline.md), com originais, licenças e hashes.
São traduções automáticas ou português fornecido upstream, devidamente identificados.
O acervo também inclui **{len(sheets)} folhas de comandos** com exemplos oficiais e procedência verificável.
Isso **não** significa documentação integral das 820 ferramentas nem revisão humana concluída.

[Cobertura por ferramenta](catalog/documentation-coverage.csv) ·
[Metodologia e direitos](THIRD_PARTY.md) · [Licenças](LICENSE-POLICY.md).
"""
readme.write_bytes((text.rstrip()+'\n').encode('utf-8'))
for p in (ROOT/'scripts').glob('*.py'):
    t=p.read_text(encoding='utf-8')
    if 'SPDX-License-Identifier:' not in t[:200]:
        if t.startswith('#!'):
            first,rest=t.split('\n',1)
            t=first+'\n# SPDX-License-Identifier: MIT\n'+rest
        else:
            t='# SPDX-License-Identifier: MIT\n'+t
        p.write_bytes(t.encode('utf-8'))
ignore=ROOT/'.gitignore'
t=ignore.read_text(encoding='utf-8')
for value in ['*.tmp','evidence/*-job.json']:
    if value not in t:
        t+='\n'+value+'\n'
ignore.write_bytes(t.encode('utf-8'))
attrs=ROOT/'.gitattributes'
t=attrs.read_text(encoding='utf-8')
for value in ['sources/upstream/** -text -diff','vault/02-Tools/*/*documentacao*.md -text whitespace=-blank-at-eol,-space-before-tab',
              '# Preserve literal upstream code whitespace and verbatim license endings.',
              'vault/02-Tools/*/*-docs-*.md -text whitespace=-blank-at-eol',
              'vault/02-Tools/*/*-cheatsheet-upstream.md -text whitespace=-blank-at-eol',
              'vault/99-Assets/upstream/** -text whitespace=-blank-at-eof',
              'LICENSE whitespace=-blank-at-eof','LICENSES/*.txt whitespace=-blank-at-eof']:
    if value not in t:
        t+='\n'+value+'\n'
attrs.write_bytes(t.encode('utf-8'))
workflow=ROOT/'.github/workflows/validate.yml'
t=workflow.read_text(encoding='utf-8')
if 'validate_documentation.py' not in t:
    t+='      - name: Validate imported documentation integrity\n        run: python3 scripts/validate_documentation.py\n'
if 'validate_cheatsheets.py' not in t:
    t+='      - name: Validate exact quick-reference examples\n        run: python3 scripts/validate_cheatsheets.py\n'
if 'test_documentation_pipeline.py' not in t:
    t+='      - name: Test documentation transformation fixtures\n        run: python3 scripts/test_documentation_pipeline.py\n'
if 'audit_offline_anchors.py' not in t:
    t+='      - name: Audit local document fragments\n        run: python3 scripts/audit_offline_anchors.py\n'
if 'verify_release_manifest.py' not in t:
    t=t.replace('      - name: Validate local notes and links',
                '      - name: Verify byte-exact release files\n        run: python3 scripts/verify_release_manifest.py\n      - name: Validate local notes and links')
workflow.write_bytes(t.encode('utf-8'))
put(pathlib.Path('requirements-translation.txt'),'ctranslate2==4.8.4\nsentencepiece==0.2.1')
print(json.dumps({'documents':len(documents),'tools':len(imports),'machine':machine,'official_portuguese':native,
                  'full_goal_complete':False,'licensing':'Own text CC-BY-SA-4.0; own scripts MIT; upstream licenses retained'},ensure_ascii=False,indent=2))
