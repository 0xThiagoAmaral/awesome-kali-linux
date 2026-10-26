#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Acquire pinned, explicitly licensed upstream documentation; never execute downloads."""
import argparse
import base64
import hashlib
import json
import pathlib
import time
import urllib.error
import urllib.request
import zipfile

REPOS={'ffuf':'ffuf/ffuf','gobuster':'OJ/gobuster','subfinder':'projectdiscovery/subfinder',
       'nuclei':'projectdiscovery/nuclei','katana':'projectdiscovery/katana',
       'naabu':'projectdiscovery/naabu','assetfinder':'tomnomnom/assetfinder',
       'waybackurls':'tomnomnom/waybackurls','feroxbuster':'epi052/feroxbuster'}
ALLOWED={'MIT','Apache-2.0','GPL-2.0','GPL-3.0','GPL-2.0-only','GPL-3.0-only',
         'GPL-2.0-or-later','GPL-3.0-or-later','AGPL-3.0','AGPL-3.0-only','AGPL-3.0-or-later',
         'BSD-2-Clause','BSD-3-Clause','ISC','MPL-2.0'}
ROOT=pathlib.Path(__file__).resolve().parents[1]

def fetch(url):
    for attempt in range(4):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Awesome-Kali-Linux-documentation-builder/0.1'})
            with urllib.request.urlopen(req,timeout=90) as r:
                return r.read()
        except (urllib.error.URLError,TimeoutError):
            if attempt==3:
                raise
            time.sleep(2**attempt)

def acquire(tool,cache):
    candidates_file=ROOT/'catalog/github-documentation-candidates.json'
    candidates=json.loads(candidates_file.read_text(encoding='utf-8')) if candidates_file.exists() else {}
    repo=REPOS.get(tool) or candidates.get(tool)
    if not repo or not all(x.replace('-','').replace('_','').replace('.','').isalnum() for x in repo.split('/')) or len(repo.split('/'))!=2:
        raise ValueError('Invalid or missing public GitHub repository for '+tool)
    target=cache/tool
    target.mkdir(parents=True,exist_ok=True)
    lock=target/'source.json'
    if lock.exists():
        record=json.loads(lock.read_text(encoding='utf-8'))
        if all((target/'docs'/x['path']).exists() for x in record['documents']):
            return record
    api='https://api.github.com/repos/'+repo
    metadata=json.loads(fetch(api))
    spdx=(metadata.get('license') or {}).get('spdx_id')
    if spdx not in ALLOWED:
        raise ValueError('Explicit documentation-compatible repository license not confirmed: '+repo+' '+str(spdx))
    head=json.loads(fetch(api+'/commits/'+metadata['default_branch']))['sha']
    license_info=json.loads(fetch(api+'/license?ref='+head))
    license_bytes=base64.b64decode(license_info['content'])
    archive=target/(head+'.zip')
    if not archive.exists():
        archive.write_bytes(fetch('https://codeload.github.com/'+repo+'/zip/'+head))
    documents=[]
    assets=[]
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            parts=pathlib.PurePosixPath(info.filename).parts[1:]
            if not parts or '..' in parts or any(x in parts for x in ['vendor','node_modules','.git','test','tests','examples']):
                continue
            relative=pathlib.PurePosixPath(*parts)
            is_root_readme=len(parts)==1 and relative.name.lower() in ['readme.md','readme.markdown','readme.rst','readme.en.md','readme_en.md','readme_pt-br.md','readme_pt_br.md','readme.pt-br.md','readme_pt.md','readme.pt.md']
            is_docs=parts[0].lower() in ['doc','docs','documentation'] and relative.suffix.lower() in ['.md','.markdown','.rst']
            is_asset=relative.suffix.lower() in ['.png','.jpg','.jpeg','.gif','.svg','.webp'] and (parts[0].lower() in ['doc','docs','documentation','_img','.assets','assets','static'] or len(parts)==1)
            if not (is_root_readme or is_docs or is_asset):
                continue
            # A nested license is a separate scope and is not silently inherited.
            overrides=[]
            for depth in range(1,len(parts)):
                prefix='/'.join([info.filename.split('/')[0]]+list(parts[:depth]))+'/'
                overrides.extend(n for n in z.namelist() if n.startswith(prefix) and '/' not in n[len(prefix):] and pathlib.PurePosixPath(n).name.upper().startswith(('LICENSE','COPYING')))
            if overrides:
                continue
            data=z.read(info)
            out=target/'docs'/pathlib.Path(*parts)
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_bytes(data)
            row={'path':relative.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                 'source_url':'https://github.com/'+repo+'/blob/'+head+'/'+relative.as_posix(),
                 'language':'pt-BR' if any(x in relative.name.lower() for x in ['pt-br','pt_br']) else 'pt' if relative.name.lower() in ['readme_pt.md','readme.pt.md'] else 'en'}
            (assets if is_asset else documents).append(row)
    if not documents:
        raise ValueError('No documentation acquired for '+tool)
    (target/'LICENSE.upstream').write_bytes(license_bytes)
    record={'tool':tool,'repository':'https://github.com/'+repo,'commit':head,'license_spdx':spdx,
            'license_url':license_info['html_url'],'license_sha256':hashlib.sha256(license_bytes).hexdigest(),
            'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
            'documents':documents,'assets':assets,'source_scope':'Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage',
            'kali_page_mirrored':False,'translation_status':'pending'}
    lock.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return record

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache',type=pathlib.Path,required=True)
    parser.add_argument('--tool',action='append')
    parser.add_argument('--from-catalog',action='store_true')
    parser.add_argument('--limit',type=int,default=5)
    args=parser.parse_args()
    registry=ROOT/'catalog/source-registry.json'
    current=json.loads(registry.read_text(encoding='utf-8')) if registry.exists() else {}
    blockers_file=ROOT/'catalog/source-blockers.json'
    blockers=json.loads(blockers_file.read_text(encoding='utf-8')) if blockers_file.exists() else {}
    failures=[]
    if args.from_catalog:
        candidates=json.loads((ROOT/'catalog/github-documentation-candidates.json').read_text(encoding='utf-8'))
        selected=[x for x in sorted(candidates) if x not in current and x not in blockers][:args.limit]
    else:
        selected=args.tool or ['ffuf','gobuster','subfinder']
    for tool in selected:
        try:
            record=acquire(tool,args.cache)
            current[tool]=record
            print(json.dumps({'tool':tool,'documents':len(record['documents']),'assets':len(record['assets']),'license':record['license_spdx'],'commit':record['commit']}),flush=True)
        except Exception as e:
            failures.append({'tool':tool,'error':repr(e)})
            blockers[tool]={'error':repr(e),'resolution':'Confirm applicable source license or choose another official documentation source; do not silently mirror unlicensed content'}
            print(json.dumps(failures[-1]),flush=True)
            if isinstance(e,urllib.error.HTTPError) and e.code in [403,429]:
                blockers.pop(tool,None)
                break
        registry.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        blockers_file.write_text(json.dumps(blockers,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result={'acquired_tools':len(current),'documents':sum(len(x['documents']) for x in current.values()),'failures':failures}
    (ROOT/'evidence/source-acquisition.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)
    return 1 if failures else 0

if __name__=='__main__':
    raise SystemExit(main())
