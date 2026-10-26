#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check quick-reference provenance and exact example preservation, without execution."""
import hashlib
import json
import pathlib
from build_cheatsheets import fenced_blocks
from import_translate_docs import code_bodies

ROOT=pathlib.Path(__file__).resolve().parents[1]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    manifest=json.loads((ROOT/'catalog/cheatsheet-provenance.json').read_text(encoding='utf-8'))
    checks=[]
    for tool,record in manifest.items():
        original=(ROOT/record['original']).read_bytes()
        note=(ROOT/record['note']).read_bytes()
        blocks=fenced_blocks(original.decode('utf-8'))
        expected=[blocks[x['block']]['body'] for x in record['recipes']]
        checks.extend([
            {'tool':tool,'check':'original hash','passed':digest(original)==record['source_sha256']},
            {'tool':tool,'check':'note hash','passed':digest(note)==record['note_sha256']},
            {'tool':tool,'check':'exact examples','passed':code_bodies(note.decode('utf-8'))==expected},
            {'tool':tool,'check':'example hashes','passed':all(digest(body.encode())==r['sha256'] for body,r in zip(expected,record['recipes']))},
            {'tool':tool,'check':'test status honest','passed':not record['command_execution_tested'] and 'test_status: "not-executed"' in note.decode('utf-8')}
        ])
    result={'passed':all(x['passed'] for x in checks),'cheatsheets':len(manifest),
            'source_examples':sum(len(x['recipes']) for x in manifest.values()),
            'examples_executed':False,'checks':checks,
            'limits':['Provenance and literal integrity do not prove command compatibility with every installed Kali version.']}
    (ROOT/'evidence/cheatsheet-integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}|{'failed':[x for x in checks if not x['passed']]},ensure_ascii=False))
    return 0 if result['passed'] else 1

if __name__=='__main__':
    raise SystemExit(main())
