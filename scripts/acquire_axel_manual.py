#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Acquire the complete Axel text manual from its already pinned licensed archive."""
import argparse
import hashlib
import json
import pathlib
import zipfile
from plain_manual import prepare_manual

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache',type=pathlib.Path,required=True)
    args=parser.parse_args()
    path=ROOT/'catalog/source-registry.json'
    registry=json.loads(path.read_text(encoding='utf-8'))
    record=registry['axel']
    assert record['license_spdx']=='GPL-2.0'
    cache=args.cache/'axel'
    archive=cache/(record['commit']+'.zip')
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==record['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        name=next(n for n in names if n.endswith('/doc/axel.txt'))
        prefix=name.rsplit('/',1)[0]+'/'
        nested=[n for n in names if n.startswith(prefix) and '/' not in n[len(prefix):] and pathlib.PurePosixPath(n).name.upper().startswith(('LICENSE','COPYING'))]
        assert not nested,'A nested documentation license needs separate review'
        data=z.read(name)
    markdown,evidence=prepare_manual(data.decode('utf-8'),'axel')
    assert evidence['all_source_text_accounted']
    assert evidence['sections']==['NAME','SYNOPSIS','DESCRIPTION','OPTIONS','NOTE','RETURN VALUE','EXAMPLES','FILES','COPYRIGHT','HELP THIS PROJECT']
    assert len(evidence['option_syntax'])==22 and len(evidence['literal_blocks'])==5
    dest=cache/'docs/doc/axel.txt'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(data)
    doc={'path':'doc/axel.txt','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
         'source_url':record['repository']+'/blob/'+record['commit']+'/doc/axel.txt',
         'language':'en','source_format':'sectioned-plain-text-v1','license_spdx':record['license_spdx']}
    record['documents']=[x for x in record['documents'] if x['path']!=doc['path']]+[doc]
    record['source_scope']='Pinned root README plus the complete doc/axel.txt reference manual; external sites and all other sources still require separate coverage review'
    (cache/'source.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (ROOT/'evidence/axel-manual-acquisition.json').write_text(json.dumps({
        'commit':record['commit'],'source_sha256':doc['sha256'],'license_spdx':record['license_spdx'],
        'nested_license_overrides':nested,'sections':evidence['sections'],'options':len(evidence['option_syntax']),
        'literal_blocks':len(evidence['literal_blocks']),'all_source_text_accounted':True},indent=2)+'\n',
        encoding='utf-8',newline='\n')
    print(json.dumps({'tool':'axel','complete_reference_manual_acquired':True,'sections':10,'options':22,'literal_blocks':5}))

if __name__=='__main__':
    main()
