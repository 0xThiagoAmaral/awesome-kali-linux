#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Account for the entire official catalog; never equate indexes with translated manuals."""
import csv
import io
import json
import pathlib
import urllib.parse

ROOT=pathlib.Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'catalog/kali-official-index.json').read_text(encoding='utf-8'))
sources=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8')) if (ROOT/'catalog/source-registry.json').exists() else {}
imports=json.loads((ROOT/'catalog/imported-documentation.json').read_text(encoding='utf-8')) if (ROOT/'catalog/imported-documentation.json').exists() else {}
coverage=[]
github_candidates={}
for tool in catalog:
    ident=tool['id']
    home=urllib.parse.urlsplit(tool.get('homepage',''))
    parts=[x for x in home.path.split('/') if x]
    if home.hostname in ['github.com','www.github.com'] and len(parts)>=2:
        repo='/'.join(parts[:2]).removesuffix('.git')
        github_candidates[ident]=repo
    source=sources.get(ident)
    imported=imports.get(ident)
    row={'tool':ident,'in_everything':tool['in_everything'],'official_kali_url':tool['kali_url'],
         'official_kali_page_mirrored':False,'official_kali_page_translated':False,
         'upstream_repository':source['repository'] if source else github_candidates.get(ident),
         'license_status':source['license_spdx'] if source else 'not-verified',
         'upstream_acquired_documents':len(source['documents']) if source else 0,
         'upstream_translated_documents':len(imported['documents']) if imported else 0,
         'code_integrity_verified':bool(imported) and all(x['code_blocks_equal'] for x in imported['documents']),
         'human_review_complete':False,'full_tool_documentation_complete':False,
         'next_action':'review-source-coverage-and-translation' if imported else 'translate-acquired-documents' if source else 'identify-licensed-official-documentation'}
    coverage.append(row)
result={'schema_version':1,'scope':'Entire pinned Kali tools catalog, with everything membership reported separately',
        'total_tools':len(coverage),'everything_tools':sum(x['in_everything'] for x in coverage),
        'tools_with_acquired_upstream_docs':sum(x['upstream_acquired_documents']>0 for x in coverage),
        'tools_with_machine_translated_docs':sum(x['upstream_translated_documents']>0 for x in coverage),
        'complete_tools':0,'goal_complete':False,
        'gates':['Source coverage includes required official documentation, not only README if additional manuals exist',
                 'Applicable copying/translation permissions verified with original notices',
                 'Portuguese prose complete and faithful; commands/code/source output preserved',
                 'Human technical review completed and terminology checked',
                 'All necessary assets and navigation available offline',
                 'Cheatsheet is supplementary and does not replace the documentation',
                 'Obsidian rendering and clean offline release validated',
                 'Public GitHub repository/release created and verified'],
        'tools':coverage}
(ROOT/'catalog/documentation-coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
(ROOT/'catalog/github-documentation-candidates.json').write_text(json.dumps(github_candidates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
buf=io.StringIO(newline='')
fields=['tool','in_everything','license_status','upstream_acquired_documents','upstream_translated_documents',
        'code_integrity_verified','human_review_complete','full_tool_documentation_complete','next_action']
w=csv.DictWriter(buf,fieldnames=fields,lineterminator='\n')
w.writeheader()
w.writerows({k:r[k] for k in fields} for r in coverage)
(ROOT/'catalog/documentation-coverage.csv').write_bytes(buf.getvalue().encode('utf-8'))
print(json.dumps({k:v for k,v in result.items() if k not in ['tools','gates']}|{'github_candidates':len(github_candidates)},ensure_ascii=False,indent=2))
