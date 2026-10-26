#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Resolve the documented AFL++ docs/COPYING delegation without ignoring nested licenses."""
import argparse
import hashlib
import json
import pathlib
import re
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--cache',type=pathlib.Path,required=True)
args=parser.parse_args()
registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
record=registry['aflplusplus']
cache=args.cache/'aflplusplus'
decisions=[]
with zipfile.ZipFile(cache/(record['commit']+'.zip')) as z:
    prefix=z.namelist()[0].split('/')[0]+'/'
    delegation=z.read(prefix+'docs/COPYING')
    decoded=delegation.decode()
    assert 'licensing has moved to the repository root' in decoded
    assert 'GNU AGPL-3.0-or-later' in decoded and 'SPDX-License-Identifier' in decoded
    existing={x['path']:x for x in record['documents']}
    for name in z.namelist():
        rel=name[len(prefix):] if name.startswith(prefix) else ''
        if not rel.startswith('docs/') or pathlib.PurePosixPath(rel).suffix.lower() not in ['.md','.rst']:
            continue
        data=z.read(name)
        text=data.decode('utf-8')
        found=re.search(r'SPDX-License-Identifier:\s*([A-Za-z0-9.-]+)',text[:3000])
        license_id=found.group(1) if found else 'AGPL-3.0-or-later'
        if license_id not in ['Apache-2.0','AGPL-3.0-or-later','AGPL-3.0','MIT']:
            decisions.append({'path':rel,'status':'requires-review','spdx':license_id})
            continue
        out=cache/'docs'/rel
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_bytes(data)
        existing[rel]={'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                       'source_url':record['repository']+'/blob/'+record['commit']+'/'+rel,
                       'language':'en','license_spdx':license_id,
                       'license_basis':'Per-file SPDX when present; otherwise root AGPL license explicitly delegated by docs/COPYING'}
        decisions.append({'path':rel,'status':'included','spdx':license_id,'bytes':len(data)})
    record['documents']=sorted(existing.values(),key=lambda x:x['path'])
    for name in z.namelist():
        rel=name[len(prefix):] if name.startswith(prefix) else ''
        if rel and '/' not in rel and pathlib.PurePosixPath(rel).name.startswith(('LICENSE','COPYING','NOTICE','LICENSING')):
            data=z.read(name)
            target=ROOT/'sources/upstream/aflplusplus'/(rel+'.txt')
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
            asset=ROOT/'vault/99-Assets/upstream/aflplusplus'/(rel+'.txt')
            asset.parent.mkdir(parents=True,exist_ok=True)
            asset.write_bytes(data)
    target=ROOT/'sources/upstream/aflplusplus/docs-COPYING.txt'
    target.write_bytes(delegation)
record['nested_license_resolution']={'path':'docs/COPYING','sha256':hashlib.sha256(delegation).hexdigest(),
                                    'decision':'Explicit delegation to repository root and per-file SPDX retained'}
registry['aflplusplus']=record
(cache/'source.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
(ROOT/'catalog/source-registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
(ROOT/'evidence/afl-documentation-license-scope.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
print(json.dumps({'documents':len(record['documents']),'decisions':decisions},ensure_ascii=False,indent=2))
