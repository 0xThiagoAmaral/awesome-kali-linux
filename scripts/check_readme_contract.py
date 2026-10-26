#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import argparse,json,pathlib,re
p=argparse.ArgumentParser()
p.add_argument('file',type=pathlib.Path)
a=p.parse_args()
text=a.file.read_text(encoding='utf-8')
first=next((x[2:] for x in text.splitlines() if x.startswith('# ')),'')
result={'title':first,'format':'awesome' if first=='Awesome Kali Linux' else 'prototype',
        'curated_entries':sum(line.startswith('- [') and '](http' in line for line in text.splitlines()),
        'has_offline_vault':'vault/' in text,'has_coverage': 'docs/COBERTURA.md' in text}
print(json.dumps(result,ensure_ascii=False,sort_keys=True))
raise SystemExit(0 if first and result['has_offline_vault'] else 1)
