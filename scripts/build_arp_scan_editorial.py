#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reproduce the complete editorial PT-BR manual from source-bound translated segments."""
import argparse,hashlib,json,pathlib,re
from roff_extended_manual import prepare_extended_roff
from import_translate_docs import translate_body,code_bodies

ROOT=pathlib.Path(__file__).resolve().parents[1]
BT=chr(96)

def needs_translation(value):
    text=re.sub(BT+r'[^'+BT+r']*'+BT,'',value)
    text=re.sub(r'https?://[^\s<>]+','',text)
    return bool(re.search(r'[A-Za-z]{2,}',text))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',help='Verify the frozen translation without rewriting files')
    args=parser.parse_args()
    source=(ROOT/'sources/upstream/arp-scan/arp-scan.1.dist.source').read_bytes()
    path=ROOT/'catalog/editorial-segments/arp-scan-main.pt-br.json'
    segments=json.loads(path.read_text(encoding='utf-8'))
    assert hashlib.sha256(source).hexdigest()==segments['source_sha256']
    prepared,structure=prepare_extended_roff(source.decode(),'arp-scan')
    assert hashlib.sha256(prepared.encode()).hexdigest()==segments['prepared_sha256']
    mapping={s['source']:s for s in segments['segments']}
    assert len(mapping)==len(segments['segments'])
    used=set()
    class Translator:
        def text(self,value):
            if not needs_translation(value):
                return value
            if value not in mapping:
                raise ValueError('Missing editorial segment: '+value)
            item=mapping[value]; assert item['translation'].strip()
            used.add(item['id'])
            return item['translation']
    translated=translate_body(prepared,Translator())
    assert used=={s['id'] for s in segments['segments']}
    assert code_bodies(translated)==code_bodies(prepared)
    prefix='<!-- SPDX-License-Identifier: LicenseRef-ARP-Scan-Manpage -->\n<!-- Complete AI-assistant translation; independent human review pending. -->\n'
    data=(prefix+translated).encode()
    dest=ROOT/'translations/pt-BR/arp-scan/arp-scan-1-dist.md'
    manifest_path=ROOT/'catalog/editorial-translations.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    entry={
        'source_sha256':segments['source_sha256'],'translation_file':dest.relative_to(ROOT).as_posix(),
        'translation_sha256':hashlib.sha256(data).hexdigest(),'translation_method':'assistant-translated',
        'review_scope':'All 143 translatable segments; 8 sections, 42 options, 13 subsections, 6 tables and formula represented; original literals preserved',
        'human_review':'pending','license_spdx':'LicenseRef-ARP-Scan-Manpage',
        'segment_file':path.relative_to(ROOT).as_posix(),'segment_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if args.check:
        assert dest.read_bytes()==data,'Frozen editorial translation differs from source-bound segments'
        assert manifest['arp-scan']['arp-scan.1.dist']==entry,'Editorial metadata differs'
    else:
        dest.write_bytes(data)
        manifest.setdefault('arp-scan',{})['arp-scan.1.dist']=entry
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'segments_used':len(used),'main_manual_translation_verified':True,'written':not args.check,
                      'exact_literal_blocks':len(code_bodies(translated)),'human_review':'pending','check_only':args.check}))

if __name__=='__main__':
    main()
