#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only verification of every registered installed-package translation."""
import json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
selected=sorted(t for t,r in registry.items() if r.get('source_kind')=='installed-kali-package')
assert selected,'No native package manuals registered'
for tool in selected:
    subprocess.run([sys.executable,str(ROOT/'scripts/build_package_editorial.py'),'--tool',tool,'--check'],check=True)
print(json.dumps({'native_package_editorials_verified':selected,'check_only':True}))
