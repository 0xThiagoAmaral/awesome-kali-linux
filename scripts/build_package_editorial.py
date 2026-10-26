#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reproduce full package-manual translations from exact, source-bound segments."""
import argparse,hashlib,json,pathlib
from packaged_manual import prepare_packaged_manual
from import_translate_docs import translate_body,code_bodies
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(data): return hashlib.sha256(data).hexdigest()

def build_one(record,doc,tool,check):
    raw=(ROOT/'sources/upstream'/tool/(doc['path']+'.source')).read_bytes()
    path=ROOT/doc.get('editorial_segment_file','catalog/editorial-segments/'+tool+'.pt-br.json')
    segments=json.loads(path.read_text(encoding='utf-8'))
    assert sha(raw)==segments['source_sha256']==doc['sha256']
    prepared,structure=prepare_packaged_manual(raw.decode('utf-8'),tool)
    assert sha(prepared.encode())==segments['prepared_sha256']
    mapping={s['source']:s for s in segments['segments']}
    assert len(mapping)==len(segments['segments'])
    used=set()
    class Translator:
        def text(self,value):
            assert value in mapping,'Missing source segment: '+value
            item=mapping[value]
            assert item['translation'].strip()
            used.add(item['id'])
            return item['translation']
    translated=translate_body(prepared,Translator())
    assert used=={s['id'] for s in segments['segments']}
    assert code_bodies(translated)==code_bodies(prepared)
    prefix='<!-- SPDX-License-Identifier: '+record['license_spdx']+' -->\n'
    if record.get('required_acknowledgement'):
        prefix+='> **Reconhecimento da licença:** '+record['required_acknowledgement']+'\n\n'
    data=(prefix+translated.rstrip()+'\n').encode()
    dest=ROOT/'translations/pt-BR'/tool/(doc['path']+'.md')
    manifest_path=ROOT/'catalog/editorial-translations.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    entry={'source_sha256':doc['sha256'],'translation_file':dest.relative_to(ROOT).as_posix(),
        'translation_sha256':sha(data),'translation_method':'assistant-translated','human_review':'pending',
        'license_spdx':record['license_spdx'],'segment_file':path.relative_to(ROOT).as_posix(),
        'segment_sha256':sha(path.read_bytes()),
        'review_scope':'All '+str(len(used))+' source-bound segments; '+str(len(structure['sections']))+' sections and '+str(len(structure['option_syntax']))+' option headings. Original syntax retained. Historical claims preserved as source statements; independent human review pending.'}
    if check:
        assert dest.read_bytes()==data
        assert manifest[tool][doc['path']]==entry
    else:
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
        manifest.setdefault(tool,{})[doc['path']]=entry
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'tool':tool,'segments':len(used),'sections':len(structure['sections']),
        'source_path':doc['path'],'option_headings':len(structure['option_syntax']),'check_only':check,'human_review':'pending'}))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--tool',required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
    record=registry[args.tool]
    assert record['source_kind']=='installed-kali-package'
    assert record['documents'],'No package source documents'
    for doc in record['documents']:
        if len(record['documents'])>1:
            assert doc.get('editorial_segment_file'),'Multi-document package requires explicit per-file segment map'
        build_one(record,doc,args.tool,args.check)

if __name__=='__main__': main()
