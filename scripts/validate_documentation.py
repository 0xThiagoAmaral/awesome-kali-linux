#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Audit acquired documentation against exact source bytes and literal-code preservation."""
import hashlib
import json
import pathlib
import os
import re
from import_translate_docs import code_bodies,outside_code
from plain_manual import prepare_manual
from roff_manual import prepare_roff_manual
from roff_extended_manual import prepare_extended_roff

ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest_path=ROOT/'catalog/imported-documentation.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
checks=[]
def add(label,passed,detail=None):
    checks.append({'check':label,'pass':bool(passed),'detail':detail})
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for tool,record in manifest.items():
    source_record=registry[tool]
    asset_root=ROOT/'vault/99-Assets/upstream'/tool
    license_file=asset_root/'LICENSE.txt'
    add(tool+' retained source license hash',license_file.exists() and digest(license_file)==source_record['license_sha256'])
    for asset in source_record['assets']:
        path=asset_root/asset['path']
        add(tool+' retained asset hash: '+asset['path'],path.exists() and digest(path)==asset['sha256'])
    for doc in record['documents']:
        note=ROOT/doc['note']
        original=ROOT/doc['original']
        label=tool+':'+doc['source_path']
        add(label+' original hash',original.exists() and digest(original)==doc['source_sha256'])
        add(label+' translation hash',note.exists() and digest(note)==doc['translation_sha256'])
        if not note.exists() or not original.exists():
            continue
        source=original.read_bytes().decode('utf-8')
        source_row=next(x for x in source_record['documents'] if x['path']==doc['source_path'])
        add(label+' source-registry binding',source_row['sha256']==doc['source_sha256'])
        if doc.get('source_format') in {'sectioned-plain-text-v1','man-roff-v1','man-roff-extended-v1'}:
            prepare={'sectioned-plain-text-v1':prepare_manual,'man-roff-v1':prepare_roff_manual,
                     'man-roff-extended-v1':prepare_extended_roff}[doc['source_format']]
            source,manual=prepare(original.read_bytes().decode('utf-8'),tool)
            prepared=ROOT/doc['prepared_source']
            add(label+' prepared-source hash',prepared.exists() and digest(prepared)==doc['prepared_source_sha256'])
            add(label+' deterministic format conversion',prepared.exists() and prepared.read_bytes()==source.encode('utf-8'))
            add(label+' all original manual text accounted',manual['all_source_text_accounted'])
            add(label+' manual-structure manifest',manual==doc['manual_structure'])
        translated=note.read_bytes().decode('utf-8')
        expected_license=source_row.get('license_spdx',source_record['license_spdx'])
        add(label+' document-specific license field','license_spdx: '+json.dumps(expected_license) in translated)
        license_path=asset_root/source_row.get('license_asset','LICENSE.txt')
        license_link=pathlib.Path(os.path.relpath(license_path,note.parent)).as_posix()
        add(label+' document-specific license link',license_path.exists() and ']('+license_link+')' in translated)
        if doc.get('source_format') in {'man-roff-v1','man-roff-extended-v1'}:
            add(label+' exact original file-specific notice',license_path.read_bytes()==manual['license_notice'].encode('utf-8'))
        if doc.get('editorial_translation'):
            editorial=doc['editorial_translation']
            p=ROOT/editorial['translation_file']
            add(label+' editorial translation hash',p.exists() and digest(p)==editorial['translation_sha256'])
            add(label+' editorial source binding',editorial['source_sha256']==doc['source_sha256'])
            add(label+' editorial not mislabeled human-reviewed',editorial['human_review']=='pending' and doc['translation_method']=='assistant-translated')
            if editorial.get('segment_file'):
                segment_file=ROOT/editorial['segment_file']
                add(label+' editorial segment file hash',segment_file.exists() and digest(segment_file)==editorial['segment_sha256'])
        if doc.get('runtime_compatibility'):
            compatibility=doc['runtime_compatibility']
            path=ROOT/compatibility['evidence']
            add(label+' recorded runtime evidence hash',path.exists() and digest(path)==compatibility['sha256'])
            if path.exists():
                runtime=json.loads(path.read_text(encoding='utf-8'))
                add(label+' runtime evidence source binding',runtime['source_manual_sha256']==doc['source_sha256'])
                script=(ROOT/compatibility.get('test_script','scripts/test_'+tool+'.py')).resolve()
                add(label+' runtime evidence script hash',script.is_relative_to(ROOT) and script.exists() and digest(script)==runtime['test_script_sha256'])
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
(ROOT/'evidence/documentation-integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}|{'failed':[x for x in checks if not x['pass']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if result['passed'] else 1)
