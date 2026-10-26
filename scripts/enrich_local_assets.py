#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Recover documentation-linked images from pinned archives, with scoped-license checks."""
import argparse
import hashlib
import json
import pathlib
import posixpath
import re
import urllib.parse
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
EXTENSIONS={'.png','.jpg','.jpeg','.gif','.svg','.webp'}

def resolve_reference(url,doc_path,repository):
    url=url.strip('<>')
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme or parsed.netloc:
        owner,repo=urllib.parse.urlsplit(repository).path.strip('/').split('/')
        bits=parsed.path.strip('/').split('/')
        if parsed.hostname=='raw.githubusercontent.com' and bits[:2]==[owner,repo] and len(bits)>3:
            path='/'.join(bits[3:])
        elif parsed.hostname=='github.com' and bits[:2]==[owner,repo] and len(bits)>4 and bits[2] in ['raw','blob']:
            path='/'.join(bits[4:])
        else:
            return None
    else:
        path=posixpath.normpath(posixpath.join(posixpath.dirname(doc_path),urllib.parse.unquote(parsed.path))) if not parsed.path.startswith('/') else parsed.path.lstrip('/')
    if path.startswith('../') or path=='..' or pathlib.PurePosixPath(path).suffix.lower() not in EXTENSIONS:
        return None
    return path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache',type=pathlib.Path,required=True)
    args=parser.parse_args()
    registry_path=ROOT/'catalog/source-registry.json'
    registry=json.loads(registry_path.read_text(encoding='utf-8'))
    results=[]
    for tool,record in registry.items():
        if record.get('source_kind')=='installed-kali-package':
            continue  # Native package notices/assets are verified by package_source.py.
        cache=args.cache/tool
        archive=cache/(record['commit']+'.zip')
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==record['archive_sha256']
        acquired={x['path'] for x in record['assets']}
        added=[]
        blocked=[]
        with zipfile.ZipFile(archive) as z:
            names={'/'.join(pathlib.PurePosixPath(x).parts[1:]):x for x in z.namelist() if not x.endswith('/')}
            for doc in record['documents']:
                text=(cache/'docs'/doc['path']).read_bytes().decode('utf-8')
                refs=re.findall(r'!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)',text)
                refs+=re.findall(r'<img\b[^>]*src=["\x27]([^"\x27]+)',text,re.I)
                for ref in refs:
                    path=resolve_reference(ref,doc['path'],record['repository'])
                    if not path or path in acquired or path not in names:
                        continue
                    parts=pathlib.PurePosixPath(path).parts
                    overrides=[]
                    for depth in range(1,len(parts)):
                        prefix='/'.join(parts[:depth])+'/'
                        overrides.extend(n for n in names if n.startswith(prefix) and '/' not in n[len(prefix):] and pathlib.PurePosixPath(n).name.upper().startswith(('LICENSE','COPYING')))
                    if overrides:
                        blocked.append({'path':path,'nested_notices':sorted(set(overrides))})
                        continue
                    data=z.read(names[path])
                    dest=cache/'docs'/path
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes(data)
                    row={'path':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                         'source_url':record['repository']+'/blob/'+record['commit']+'/'+path,
                         'language':'not-applicable'}
                    record['assets'].append(row)
                    acquired.add(path)
                    added.append(path)
        (cache/'source.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
        results.append({'tool':tool,'added_images':added,'license_scope_pending':blocked})
    registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    (ROOT/'evidence/asset-enrichment.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    print(json.dumps({'tools':len(results),'images_added':sum(len(x['added_images']) for x in results),
                      'nested_license_cases':sum(len(x['license_scope_pending']) for x in results)}))

if __name__=='__main__':
    main()
