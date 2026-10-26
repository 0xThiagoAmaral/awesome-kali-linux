#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Retain original copyright/license/NOTICE files from already acquired archives."""
import argparse
import hashlib
import json
import pathlib
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--cache',type=pathlib.Path,required=True)
args=parser.parse_args()
registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
result=[]
for tool,record in registry.items():
    cached=args.cache/tool
    archive=cached/(record['commit']+'.zip')
    notices=[]
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            parts=pathlib.PurePosixPath(info.filename).parts[1:]
            if len(parts)==1 and parts[0].upper().startswith(('LICENSE','COPYING','NOTICE','COPYRIGHT')):
                data=z.read(info)
                dest=ROOT/'sources/upstream'/tool/(parts[0]+'.txt')
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(data)
                notices.append({'path':dest.relative_to(ROOT).as_posix(),'source_path':parts[0],
                                'sha256':hashlib.sha256(data).hexdigest()})
    record['retained_notices']=notices
    (cached/'source.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result.append({'tool':tool,'license':record['license_spdx'],'notices':len(notices)})
(ROOT/'catalog/source-registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'evidence/source-notices.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
