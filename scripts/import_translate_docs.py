#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Import licensed documentation faithfully; preserve code and track incomplete coverage."""
import argparse
import hashlib
import json
import os
import pathlib
import posixpath
import re
import shutil
import time
import unicodedata
import urllib.parse
from translation_engine import LocalTranslator
from enrich_local_assets import resolve_reference
from plain_manual import prepare_manual

ROOT=pathlib.Path(__file__).resolve().parents[1]
BT=chr(96)
FENCE=re.compile(r'^(\s*)('+BT+r'{3,}|~{3,})(.*)$')
PIPELINE_VERSION='0.6-tables-images-and-source-link-corrections'

def save_json(path,value):
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    temp.replace(path)

def note_name(tool,doc):
    if doc.get('language','en').startswith('pt'):
        return tool+'-documentacao-pt-br-oficial'
    return tool+'-documentacao' if doc['path'].lower()=='readme.md' else tool+'-'+re.sub(r'[^a-z0-9]+','-',doc['path'].lower()).strip('-')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def code_bodies(text):
    out=[]
    active=None
    buf=[]
    for line in text.splitlines(keepends=True):
        m=FENCE.match(line)
        if active is None and m:
            active=(m.group(2)[0],len(m.group(2)))
            buf=[]
        elif active and m and m.group(2)[0]==active[0] and len(m.group(2))>=active[1]:
            out.append(''.join(buf))
            active=None
        elif active:
            buf.append(line)
    return out

def slug(value):
    value=re.sub(r'<[^>]*>','',value).replace(BT,'').strip().lower()
    value=re.sub(r'!?\[([^\]]+)\]\([^)]+\)',r'\1',value)
    value=re.sub(r'[^\w -]','',value,flags=re.U)
    return value.replace(' ','-')

def outside_code(text,callback):
    result=[]
    plain=[]
    active=None
    for line in text.splitlines(keepends=True):
        m=FENCE.match(line)
        if active:
            result.append(line)
            if m and m.group(2)[0]==active[0] and len(m.group(2))>=active[1]:
                active=None
        elif m:
            result.append(callback(''.join(plain)))
            plain=[]
            result.append(line)
            active=(m.group(2)[0],len(m.group(2)))
        else:
            plain.append(line)
    result.append(callback(''.join(plain)))
    return ''.join(result)

def markdown_headings(text):
    headings=[]
    def collect(part):
        headings.extend((len(m.group(1)),m.group(2)) for m in re.finditer(r'^(#{1,6})\s+(.+)$',part,re.M))
        return part
    outside_code(normalize_legacy_headings(text),collect)
    return headings

def normalize_legacy_headings(text):
    """Present legacy GitHub headings consistently, without touching fenced examples."""
    def convert(part):
        return re.sub(r'^(#{1,6})(?=[A-Za-z])(.+)$',
                      lambda m:m.group(1)+' '+m.group(2).rstrip('#').rstrip(),part,flags=re.M)
    return outside_code(text,convert)

def preserve_heading_anchors(source,translated):
    """Retain original source heading IDs so cross-document links survive translation."""
    old=markdown_headings(source)
    new=markdown_headings(translated)
    assert len(old)==len(new),'Translation changed the heading count'
    counts={}
    ids=[]
    for _,value in old:
        base=slug(value)
        occurrence=counts.get(base,0)
        counts[base]=occurrence+1
        ids.append(base+('-'+str(occurrence) if occurrence else ''))
    existing=set(re.findall(r'\b(?:id|name)=["\x27]([^"\x27]+)',translated))
    index=0
    changes=[]
    def convert(part):
        nonlocal index
        def heading(match):
            nonlocal index
            alias=ids[index]
            index+=1
            if alias and alias!=slug(match.group(2)) and alias not in existing:
                existing.add(alias)
                changes.append({'kind':'original-heading-id-preserved','anchor':alias})
                return '<a id="'+alias+'"></a>\n'+match.group()
            return match.group()
        return re.sub(r'^(#{1,6})[ \t]+(.+)$',heading,part,flags=re.M)
    return outside_code(translated,convert),changes

def translate_body(source,tr):
    out=[]
    active=None
    heading_map={}
    for line in normalize_legacy_headings(source).splitlines(keepends=True):
        end='\n' if line.endswith('\n') else ''
        stripped=line.rstrip('\r\n')
        m=FENCE.match(stripped)
        if active:
            out.append(line)
            if m and m.group(2)[0]==active[0] and len(m.group(2))>=active[1]:
                active=None
            continue
        if m:
            active=(m.group(2)[0],len(m.group(2)))
            out.append(stripped+('text' if not m.group(3).strip() else '')+end)
            continue
        if stripped.lstrip().startswith('<') and re.search(r'>[^<\s][^<]+<',stripped):
            out.append(tr.text(stripped)+end)
            continue
        if not stripped.strip() or stripped.lstrip().startswith(('<','<!--','[![')) or stripped.startswith(('    ','\t')):
            out.append(line)
            continue
        h=re.match(r'^(#{1,6}\s+)(.*)$',stripped)
        if h:
            translated=h.group(2) if h.group(1)=='# ' else tr.text(h.group(2))
            heading_map[slug(h.group(2))]=slug(translated)
            out.append(h.group(1)+translated+end)
            continue
        if re.fullmatch(r'\s*[| :\-]+\s*',stripped):
            out.append(line)
            continue
        if stripped.lstrip().startswith('|'):
            out.append('|'.join(tr.text(x.strip()) if x.strip() else '' for x in re.split(r'(?<!\\)\|',stripped))+end)
            continue
        prefix=re.match(r'^(\s*(?:[-*+]|\d+\.)\s+(?:\[[ xX]\]\s+)?)(.*)$',stripped)
        if prefix:
            out.append(prefix.group(1)+tr.text(prefix.group(2))+end)
        else:
            out.append(tr.text(stripped)+end)
    result=''.join(out)
    for before,after in heading_map.items():
        result=result.replace('](#'+before+')','](#'+after+')')
    assert code_bodies(result)==code_bodies(source),'Literal fenced code changed'
    return result

def mirror_images(text,record,asset_root,note,doc_path='README.md'):
    modifications=[]
    available={x['path']:asset_root/pathlib.Path(x['path']) for x in record['assets']}
    def resolve(url):
        path=resolve_reference(url,doc_path,record['repository'])
        target=available.get(path)
        if target and target.exists():
            return pathlib.Path(os.path.relpath(target,note.parent)).as_posix()
        return None
    def markdown(match):
        alt,url=match.group(1),match.group(2)
        local=resolve(url)
        if local:
            return '!['+alt+']('+local+')'
        modifications.append({'kind':'remote-image-to-reference-link','url':url})
        if match.start()>0 and match.string[match.start()-1]=='[':
            return alt or 'Recurso externo'
        return '[Imagem/recurso externo: '+(alt or 'referência')+']('+url+')'
    def html(match):
        tag=match.group()
        m=re.search(r'src=["\']([^"\']+)["\']',tag)
        if not m:
            return tag
        local=resolve(m.group(1))
        if local:
            return tag.replace(m.group(1),local)
        modifications.append({'kind':'remote-html-image-removed','url':m.group(1)})
        return ''
    def convert(part):
        part=re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',markdown,part)
        return re.sub(r'<img\b[^>]*>',html,part,flags=re.I)
    return outside_code(text,convert),modifications

def resolve_relative_links(text,record,doc_path,note,asset_root,heading_map):
    changes=[]
    correction_file=ROOT/'catalog/source-link-corrections.json'
    corrections=json.loads(correction_file.read_text(encoding='utf-8')).get(record['tool'],{}) if correction_file.exists() else {}
    def link(match):
        label,url=match.group(1),match.group(2)
        if url in corrections:
            replacement=corrections[url]
            changes.append({'kind':'source-link-correction','from':url,'to':replacement})
            if replacement=='@retained-license':
                target=pathlib.Path(os.path.relpath(asset_root/'LICENSE.txt',note.parent)).as_posix()
                return '['+label+']('+target+')'
            url=replacement
        parsed=urllib.parse.urlsplit(url)
        own_page=url.split('#')[0].rstrip('/') in [record['repository'].rstrip('/'),record['repository']+'/blob/'+record['commit']+'/'+doc_path]
        if parsed.fragment and (own_page or not parsed.path and not parsed.scheme):
            return '['+label+'](#'+heading_map.get(parsed.fragment,parsed.fragment)+')'
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match.group()
        if pathlib.PurePosixPath(parsed.path).name.upper().startswith(('LICENSE','COPYING')):
            local=pathlib.Path(os.path.relpath(asset_root/'LICENSE.txt',note.parent)).as_posix()
            return '['+label+']('+local+')'
        # References outside the acquired corpus are explicit pinned source links, not broken local files.
        base=pathlib.PurePosixPath(doc_path).parent
        joined=posixpath.normpath(str(base/pathlib.PurePosixPath(parsed.path)))
        acquired=next((x for x in record['documents'] if x['path']==joined),None)
        if acquired:
            target=note_name(record['tool'],acquired)+'.md'
            if parsed.fragment:
                target+='#'+parsed.fragment
            return '['+label+']('+target+')'
        target=record['repository']+'/blob/'+record['commit']+'/'+joined
        if parsed.fragment:
            target+='#'+parsed.fragment
        changes.append({'kind':'unacquired-relative-reference-pinned-online','source_path':joined})
        return '['+label+']('+target+')'
    def convert(part):
        # Linked images must be protected before matching their enclosing text link.
        images=[]
        def hide_image(match):
            token='AKLIMAGE'+str(len(images))+'TOKEN'
            images.append(match.group())
            return token
        part=re.sub(r'!\[[^\]]*\]\([^)]+\)',hide_image,part)
        part=re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',link,part)
        for index,image in enumerate(images):
            part=part.replace('AKLIMAGE'+str(index)+'TOKEN',image)
        for before,after in corrections.items():
            if after=='@retained-license':
                after=pathlib.Path(os.path.relpath(asset_root/'LICENSE.txt',note.parent)).as_posix()
            elif after.startswith('#'):
                after='#'+heading_map.get(after[1:],after[1:])
            for quote in ['"',chr(39)]:
                needle='href='+quote+before+quote
                if needle in part:
                    part=part.replace(needle,'href='+quote+after+quote)
                    changes.append({'kind':'source-html-link-correction','from':before,'to':after})
        for before,after in heading_map.items():
            part=part.replace('href="#'+before+'"','href="#'+after+'"')
        return part
    return outside_code(text,convert),changes

def preserve_contributor_anchors(text):
    """Attach all-contributors badge links to the actual matching contributor cell."""
    changes=[]
    def convert(part):
        def cell(match):
            cell_text=match.group()
            aliases=sorted(set(re.findall(r'href=["\x27]#((?:infra|ideas)-[^"\x27]+)',cell_text)))
            prefix=''.join('<a id="'+value+'"></a>' for value in aliases)
            if prefix:
                changes.extend({'kind':'contributor-badge-anchor-preserved','anchor':value,'destination':'matching contributor table cell'} for value in aliases)
                end=cell_text.index('>')+1
                cell_text=cell_text[:end]+prefix+cell_text[end:]
            return cell_text
        return re.sub(r'<td\b[^>]*>.*?</td>',cell,part,flags=re.S|re.I)
    return outside_code(text,convert),changes

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache',type=pathlib.Path,required=True)
    parser.add_argument('--runtime',type=pathlib.Path,required=True)
    parser.add_argument('--tool',action='append')
    parser.add_argument('--force',action='store_true')
    args=parser.parse_args()
    registry=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))
    editorial_file=ROOT/'catalog/editorial-translations.json'
    editorials=json.loads(editorial_file.read_text(encoding='utf-8')) if editorial_file.exists() else {}
    tr=LocalTranslator(args.runtime)
    report_file=ROOT/'catalog/imported-documentation.json'
    report=json.loads(report_file.read_text(encoding='utf-8')) if report_file.exists() else {}
    job_file=ROOT/'evidence/documentation-import-job.json'
    job={'pid':os.getpid(),'status':'running','started_epoch':time.time(),'pipeline_version':PIPELINE_VERSION,
         'selected_tools':args.tool or sorted(registry),'completed_in_this_run':[]}
    save_json(job_file,job)
    for tool in args.tool or sorted(registry):
        record=registry[tool]
        dest=ROOT/'vault/02-Tools'/tool
        dest.mkdir(parents=True,exist_ok=True)
        originals=ROOT/'sources/upstream'/tool
        assets=ROOT/'vault/99-Assets/upstream'/tool
        originals.mkdir(parents=True,exist_ok=True)
        assets.mkdir(parents=True,exist_ok=True)
        license_bytes=(args.cache/tool/'LICENSE.upstream').read_bytes()
        assert sha(license_bytes)==record['license_sha256']
        (assets/'LICENSE.txt').write_bytes(license_bytes)
        for asset in record['assets']:
            src=args.cache/tool/'docs'/asset['path']
            assert sha(src.read_bytes())==asset['sha256']
            target=assets/asset['path']
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(src,target)
        old_documents={x['source_path']:x for x in report.get(tool,{}).get('documents',[])}
        documents=[]
        priority={'README.md':0,'docs/README.md':1,'docs/INSTALL.md':2,'docs/FAQ.md':3,'docs/features.md':4,'docs/Changelog.md':99}
        selected_docs=sorted(record['documents'],key=lambda x:(priority.get(x['path'],10),x['path']))
        for doc in selected_docs:
            old=old_documents.get(doc['path'])
            if old and old.get('pipeline_version')==PIPELINE_VERSION and not args.force:
                existing=ROOT/old['note']
                if existing.exists() and sha(existing.read_bytes())==old['translation_sha256'] and old['source_sha256']==doc['sha256']:
                    documents.append(old)
                    continue
            data=(args.cache/tool/'docs'/doc['path']).read_bytes()
            assert sha(data)==doc['sha256']
            raw=originals/(doc['path']+'.source')
            raw.parent.mkdir(parents=True,exist_ok=True)
            raw.write_bytes(data)
            source=data.decode('utf-8')
            format_info={}
            manual_changes=[]
            if doc.get('source_format')=='sectioned-plain-text-v1':
                source,manual_evidence=prepare_manual(source,tool)
                prepared=originals/(doc['path']+'.presentation.md.source')
                prepared.write_bytes(source.encode('utf-8'))
                format_info={'source_format':doc['source_format'],
                             'prepared_source':prepared.relative_to(ROOT).as_posix(),
                             'prepared_source_sha256':sha(source.encode('utf-8')),
                             'manual_structure':manual_evidence}
                manual_changes=[{'kind':'plain-text-manual-to-markdown','details':manual_evidence['presentation_changes']}]
            name=note_name(tool,doc)
            note=dest/(name+'.md')
            native_portuguese=doc.get('language','en').startswith('pt')
            editorial=editorials.get(tool,{}).get(doc['path'])
            if editorial:
                assert editorial['source_sha256']==sha(data),'Editorial translation source changed'
                editorial_path=(ROOT/editorial['translation_file']).resolve()
                assert editorial_path.is_relative_to(ROOT)
                editorial_bytes=editorial_path.read_bytes()
                assert sha(editorial_bytes)==editorial['translation_sha256']
                translated=editorial_bytes.decode('utf-8')
                assert code_bodies(translated)==code_bodies(source),'Editorial translation changed literal examples'
                format_info['editorial_translation']=editorial
            else:
                translated=source if native_portuguese else translate_body(source,tr)
            old_heads=[value for _,value in markdown_headings(source)]
            new_heads=[value for _,value in markdown_headings(translated)]
            heading_map={slug(a):slug(b) for a,b in zip(old_heads,new_heads)}
            translated,anchor_changes=preserve_heading_anchors(source,translated)
            translated,changes=mirror_images(translated,record,assets,note,doc['path'])
            changes+=anchor_changes
            changes+=manual_changes
            if normalize_legacy_headings(source)!=source:
                changes.append({'kind':'legacy-markdown-heading-spacing-normalized'})
            translated,link_changes=resolve_relative_links(translated,record,doc['path'],note,assets,heading_map)
            changes+=link_changes
            translated,contributor_changes=preserve_contributor_anchors(translated)
            changes+=contributor_changes
            # Add a visible title only if the source did not have a Markdown H1.
            if not any(level==1 for level,_ in markdown_headings(translated)):
                translated='# '+tool+' — documentação oficial\n\n'+translated
            props={'title':tool+' — documentação oficial','type':'official-documentation','tool':tool,
                   'status':'official-translation' if native_portuguese else 'source-checked' if editorial else 'translated-machine','reviewed':'2026-10-26','language':doc.get('language') if native_portuguese else 'pt-BR',
                   'tags':['documentation','tool/'+tool],'cssclasses':['fieldbook'],
                   'source_url':doc['source_url'],'source_commit':record['commit'],
                   'source_sha256':doc['sha256'],'license_spdx':doc.get('license_spdx',record['license_spdx']),
                   'human_review':'pending','source_scope':record['source_scope']}
            compatibility_notice=''
            runtime_path=ROOT/'evidence'/(tool+'-local-tests.json')
            if doc.get('source_format')=='sectioned-plain-text-v1' and runtime_path.exists():
                runtime=json.loads(runtime_path.read_text(encoding='utf-8'))
                if runtime.get('source_manual_sha256')==doc['sha256'] and runtime.get('passed'):
                    evidence_rel='../../99-Assets/evidence/'+runtime_path.name
                    missing=', '.join(BT+x+BT for x in runtime['manual_options_not_listed_by_installed_help'])
                    extra=', '.join(BT+x+BT for x in runtime['installed_help_options_not_in_manual'])
                    compatibility_notice='> **Compatibilidade observada:** '+runtime['installed_version']+'. A ajuda dessa instalação não lista '+missing+'. Ela lista '+extra+', ausente deste manual. A fonte fixada foi mantida sem trocar opções silenciosamente. [Evidência e limites do teste]('+evidence_rel+').\n\n'
                    props['test_status']='partial-local'
                    props['tested_version']=runtime['installed_version']
                    format_info['runtime_compatibility']={'evidence':'evidence/'+runtime_path.name,'sha256':sha(runtime_path.read_bytes())}
            fm='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in props.items())+'\n---\n\n'
            notice=('> Texto em português fornecido pelo próprio projeto upstream e preservado nesta importação. Links e imagens receberam adaptações para navegação local; isso não comprova revisão técnica por este repositório.\n\n' if native_portuguese else '> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.\n\n')
            if editorial:
                notice='> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.\n\n'
            notice+=compatibility_notice
            license_link=pathlib.Path(os.path.relpath(assets/'LICENSE.txt',note.parent)).as_posix()
            attribution='\n\n---\n\n## Procedência desta tradução\n\nFonte: ['+record['repository']+']('+doc['source_url']+'). Licença: ['+doc.get('license_spdx',record['license_spdx'])+']('+license_link+'). Commit: '+record['commit']+'.\n\nO original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.\n'
            final=fm+notice+translated+attribution
            temp_note=note.with_suffix('.md.tmp')
            temp_note.write_bytes(final.encode('utf-8'))
            temp_note.replace(note)
            documents.append({'source_path':doc['path'],'note':note.relative_to(ROOT).as_posix(),
                              'original':raw.relative_to(ROOT).as_posix(),'source_sha256':sha(data),
                              'translation_sha256':sha(final.encode('utf-8')),
                              'source_fenced_blocks':len(code_bodies(source)),
                              'code_blocks_equal':code_bodies(translated)==code_bodies(source),
                              'translation_method':'upstream-portuguese' if native_portuguese else 'assistant-translated' if editorial else 'machine-local',
                              'pipeline_version':PIPELINE_VERSION,
                              'presentation_changes':changes,'human_review':'pending'})
            documents[-1].update(format_info)
            report[tool]={'repository':record['repository'],'commit':record['commit'],'license_spdx':record['license_spdx'],
                          'documents':list(documents),'source_scope':record['source_scope'],'kali_official_page_complete':False,
                          'translation_complete_for_acquired_documents':len(documents)==len(selected_docs),
                          'human_review_complete':False,'model':tr.provenance()}
            save_json(report_file,report)
            job['completed_in_this_run'].append({'tool':tool,'source':doc['path'],'note':note.relative_to(ROOT).as_posix()})
            job['updated_epoch']=time.time()
            save_json(job_file,job)
            tr.flush()
            print(json.dumps({'tool':tool,'note':note.name,'code_blocks_preserved':len(code_bodies(source))}),flush=True)
        report[tool]={'repository':record['repository'],'commit':record['commit'],'license_spdx':record['license_spdx'],
                      'documents':documents,'source_scope':record['source_scope'],
                      'kali_official_page_complete':False,'translation_complete_for_acquired_documents':True,
                      'human_review_complete':False,'model':tr.provenance()}
        save_json(report_file,report)
    tr.flush()
    result={'tools':len(report),'documents':sum(len(x['documents']) for x in report.values()),
            'all_fenced_code_preserved':all(d['code_blocks_equal'] for x in report.values() for d in x['documents']),
            'human_review_complete':False,'full_kali_corpus_complete':False}
    (ROOT/'evidence/documentation-import.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    job['status']='completed'
    job['completed_epoch']=time.time()
    job['result']=result
    save_json(job_file,job)
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    main()
