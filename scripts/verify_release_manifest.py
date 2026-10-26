#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify packaged file bytes offline; does not execute documented commands."""
import hashlib
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    errors=[]
    checked=0
    for line in (ROOT/'manifest.sha256').read_text(encoding='utf-8').splitlines():
        expected,name=line.split('  ',1)
        path=(ROOT/name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            errors.append({'file':name,'reason':'missing or escaping file'})
            continue
        checked+=1
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=expected:
            errors.append({'file':name,'expected':expected,'actual':actual})
    print(json.dumps({'passed':not errors,'files_checked':checked,'errors':errors}))
    return 1 if errors else 0

if __name__=='__main__':
    raise SystemExit(main())
