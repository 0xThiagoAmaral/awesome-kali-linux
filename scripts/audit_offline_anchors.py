#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Audit local Markdown fragments; this is not a substitute for Obsidian rendering."""
import json
import pathlib
import re
import urllib.parse
from import_translate_docs import markdown_headings,outside_code,slug

ROOT=pathlib.Path(__file__).resolve().parents[1]

def anchors(text):
    found=set(re.findall(r'\b(?:id|name)=["\x27]([^"\x27]+)',text))
    counts={}
    for _,heading in markdown_headings(text):
        base=slug(heading)
        count=counts.get(base,0)
        counts[base]=count+1
        found.add(base+('-'+str(count) if count else ''))
    return found

def main():
    notes=sorted((ROOT/'vault').rglob('*.md'))
    content={p.resolve():p.read_text(encoding='utf-8') for p in notes}
    table={p:anchors(text) for p,text in content.items()}
    failures=[]
    checked=0
    for p,text in content.items():
        links=[]
        def collect(part):
            links.extend(re.findall(r'(?<!!)\[[^\]]*\]\(([^)\s]+)\)',part))
            links.extend(re.findall(r'<a\b[^>]*href=["\x27]([^"\x27]+)',part,re.I))
            return part
        outside_code(text,collect)
        for link in links:
            parsed=urllib.parse.urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.fragment:
                continue
            dest=(p.parent/urllib.parse.unquote(parsed.path)).resolve() if parsed.path else p
            if dest not in table:
                continue
            checked+=1
            fragment=urllib.parse.unquote(parsed.fragment)
            if fragment not in table[dest]:
                failures.append({'note':p.relative_to(ROOT).as_posix(),'link':link,'target':dest.relative_to(ROOT).as_posix()})
    result={'passed':not failures,'notes':len(notes),'local_fragments_checked':checked,'failures':failures,
            'limits':['Static heading/HTML-ID audit; native Obsidian rendering and interaction still require a separate visual check.']}
    (ROOT/'evidence/offline-anchors.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not failures else 1

if __name__=='__main__':
    raise SystemExit(main())
