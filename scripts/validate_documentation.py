#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Audit acquired documentation against exact source bytes and literal-code preservation."""
import hashlib
import json
import pathlib
import re
from import_translate_docs import code_bodies,outside_code

ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest_path=ROOT/'catalog/imported-documentation.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
checks=[]
def add(label,passed,detail=None):
    checks.append({'check':label,'pass':bool(passed),'detail':detail})
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for tool,record in manifest.items():
    for doc in record['documents']:
        note=ROOT/doc['note']
        original=ROOT/doc['original']
        label=tool+':'+doc['source_path']
        add(label+' original hash',original.exists() and digest(original)==doc['source_sha256'])
        add(label+' translation hash',note.exists() and digest(note)==doc['translation_sha256'])
        if not note.exists() or not original.exists():
            continue
        source=original.read_bytes().decode('utf-8')
        translated=note.read_bytes().decode('utf-8')
        add(label+' exact fenced-code bodies',code_bodies(source)==code_bodies(translated),len(code_bodies(source)))
        source_inline=[]
        translated_inline=[]
        tick=chr(96)
        def collector(dest):
            def collect(part):
                def label(m):
                    title=m.group(1)
                    def prose(code):
                        value=code.group(1)
                        return code.group() if value.startswith('-') or '/' in value or re.search(r'\d+\.\d+|\.[a-z]{2,}',value) else value
                    title=re.sub(tick+'([^'+tick+']+)'+tick,prose,title)
                    return '['+title+']('+m.group(2)+')'
                normalized=re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',label,part)
                dest.extend(re.findall(tick+'([^'+tick+'\n]+)'+tick,normalized))
                return part
            return collect
        outside_code(source,collector(source_inline))
        without_front=re.sub(r'^---\n.*?\n---\n','',translated,flags=re.S)
        outside_code(without_front,collector(translated_inline))
        add(label+' inline literals retained',all(x in translated_inline for x in source_inline),
            {'source':len(source_inline),'translation':len(translated_inline)})
        add(label+' no tokenizer/placeholder leaks',chr(9601) not in without_front and not re.search(r'ZXQ\d+QXZ',without_front))
        images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',without_front)
        images+=re.findall(r'<img\b[^>]*src=["\']([^"\']+)["\']',without_front,re.I)
        missing=[u for u in images if u.startswith(('http:','https:')) or not (note.parent/u).resolve().is_file()]
        add(label+' displayed images offline',not missing,missing)
        add(label+' review status honest','human_review: "pending"' in translated)
result={'passed':all(x['pass'] for x in checks),'tools':len(manifest),
        'documents':sum(len(x['documents']) for x in manifest.values()),
        'code_blocks':sum(x['source_fenced_blocks'] for r in manifest.values() for x in r['documents']),
        'checks':checks,'goal_complete':False,
        'limits':['This checks source/literal integrity and assets, not semantic translation quality or complete tool-manual coverage.',
                  'Human technical review and full Kali corpus coverage remain separate acceptance gates.']}
(ROOT/'evidence/documentation-integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}|{'failed':[x for x in checks if not x['pass']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if result['passed'] else 1)
