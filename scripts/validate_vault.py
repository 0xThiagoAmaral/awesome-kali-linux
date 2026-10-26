#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline structural checks using only Python's standard library."""
import json
import pathlib
import re
import urllib.parse

ROOT=pathlib.Path(__file__).resolve().parents[1]
VAULT=ROOT/'vault'
errors=[]
notes=list(VAULT.rglob('*.md'))
links_checked=0
for p in notes:
    text=p.read_text(encoding='utf-8')
    front=re.match(r'^---\n(.*?)\n---\n',text,re.S)
    if not front:
        errors.append(str(p.relative_to(ROOT))+': missing frontmatter')
        continue
    props={}
    for line in front.group(1).splitlines():
        key,raw=line.split(':',1)
        props[key]=json.loads(raw.strip())
    for key in ['title','type','status','reviewed','tags']:
        if key not in props:
            errors.append(str(p.relative_to(ROOT))+': missing '+key)
    if props.get('status') not in ['draft','source-checked','tested-local','community-reviewed','translated-machine','official-translation']:
        errors.append(str(p.relative_to(ROOT))+': invalid status')
    body=text[front.end():]
    without_code=re.sub(r'```.*?```','',body,flags=re.S)
    h1_count=len(re.findall(r'^# ',without_code,re.M))
    if h1_count<1 or (props.get('type')!='official-documentation' and h1_count!=1):
        errors.append(str(p.relative_to(ROOT))+': expected one H1')
    if len(re.findall(r'^```',body,re.M))%2:
        errors.append(str(p.relative_to(ROOT))+': unbalanced code fences')
    if re.search(r'^```\s*\n(?!\n)',body,re.M):
        # Closing fences are excluded by explicit block scanning below.
        pass
    if re.search(r'!\[[^\]]*\]\(https?://',body):
        errors.append(str(p.relative_to(ROOT))+': remote image breaks offline assets policy')
    for match in re.finditer(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',without_code):
        dest=match.group(1)
        u=urllib.parse.urlsplit(dest)
        if u.scheme or u.netloc or not u.path:
            continue
        target=(p.parent/urllib.parse.unquote(u.path)).resolve()
        links_checked+=1
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(str(p.relative_to(ROOT))+': broken/escaping link '+dest)
    fence_open=False
    for line in body.splitlines():
        if line.startswith('```'):
            if not fence_open and not line[3:].strip():
                errors.append(str(p.relative_to(ROOT))+': code block without language')
            fence_open=not fence_open

for p in ROOT.rglob('*.md'):
    if p.is_relative_to(VAULT):
        continue
    body=re.sub(r'\x60\x60\x60.*?\x60\x60\x60','',p.read_text(encoding='utf-8'),flags=re.S)
    for match in re.finditer(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',body):
        dest=match.group(1)
        u=urllib.parse.urlsplit(dest)
        if u.scheme or u.netloc or not u.path:
            continue
        target=(p.parent/urllib.parse.unquote(u.path)).resolve()
        links_checked+=1
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(str(p.relative_to(ROOT))+': broken/escaping link '+dest)

for tool in ['nmap','ffuf']:
    for kind in ['guia','cheatsheet','troubleshooting','fontes']:
        if not (VAULT/'02-Tools'/tool/(tool+'-'+kind+'.md')).is_file():
            errors.append(tool+': incomplete module')
for p in ROOT.rglob('*.json'):
    if '__pycache__' not in p.parts:
        json.loads(p.read_text(encoding='utf-8'))
all_text='\n'.join(p.read_text(encoding='utf-8') for p in ROOT.rglob('*') if p.is_file() and p.suffix in ['.md','.json','.csv','.txt'])
for pattern in [re.escape('C:'+chr(92)+'Users'+chr(92)),r'/mnt/[a-z]/Users/[^/\s]+',r'C:/Users/[^/\s]+',re.escape('/home/kali/'),r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----',r'ghp_[A-Za-z0-9]{30,}']:
    if re.search(pattern,all_text):
        errors.append('Personal-path/secret pattern found: '+pattern)
result={'passed':not errors,'markdown_notes':len(notes),'local_links_checked':links_checked,'errors':errors,
        'limits':['Pattern checks are not a complete secret-scanning audit.','No external URL fetch or Obsidian visual test performed.']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/structure-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
