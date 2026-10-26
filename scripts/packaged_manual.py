#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Non-executing man(7) subset for package sources. Unknown syntax fails closed."""
import re
import shlex
from package_layout_repairs import repair_arping_layout,prepare_dns_package_layout

BT=chr(96)
STYLES={'B','I','BR','BI','RB','RI','IR','IB'}
ALLOWED=STYLES|{'TH','SH','SS','P','PP','TP','IP','nf','fi','fam','in','sp','RS','RE','IX'}

def arguments(value):
    lexer=shlex.shlex(value,posix=True)
    lexer.whitespace_split=True
    lexer.commenters=''
    lexer.escape=''
    return list(lexer)

def decode(value):
    if '\ue000' in value: raise ValueError('Reserved decoder sentinel in source')
    value=value.replace(r'\\','\ue000').replace(r'\.','.')
    value=value.replace(r'\-', '-').replace(r'\&','').replace(r'\~',' ').replace(r'\:','').replace(r'\(cq',"'").replace(r'\(dq','"').replace(r'\(bu','•')
    value=re.sub(r'\\f(?:[BIRP]|\([A-Z]{2})','',value)
    if '\\' in value:
        raise ValueError('Unknown package-manual escape: '+value)
    return value.replace('\ue000','\\')

def styled(kind,args,literal=False):
    values=[decode(x) for x in args]
    if literal:
        return ' '.join(values) if kind in {'B','I'} else ''.join(values)
    if kind in {'B','I'}:
        return BT+' '.join(values)+BT if values else ''
    result=''.join(BT+x+BT if kind[i%2]!='R' and re.search(r'\w',x) else x for i,x in enumerate(values))
    plain=''.join(values)
    return plain if re.fullmatch(r'<https?://[^ >]+>',plain) else result.replace(BT*2,'')

def prepare_packaged_manual(source,tool):
    if tool in {'dnsenum','dnsrecon'}:
        original=source
        source,provenance=prepare_dns_package_layout(source,tool)
        rendered,evidence=_prepare_packaged_manual(source,tool)
        evidence.update(source_lines=len(original.splitlines()),layout_adjusted_lines=len(source.splitlines()),
            source_layout_adapter=provenance,line_number_basis='Layout-adjusted source; exact original retained')
        evidence['presentation_changes']+=provenance['changes']
        return rendered,evidence
    if tool=='arping':
        original=source
        source,repairs=repair_arping_layout(source)
        rendered,evidence=_prepare_packaged_manual(source,tool)
        evidence.update(source_lines=len(original.splitlines()),layout_adjusted_lines=len(source.splitlines()),
            layout_repairs=repairs,line_number_basis='Layout-adjusted source; exact original is retained separately')
        evidence['presentation_changes'].append('Six exact-source-bound layout repairs recorded explicitly; all non-request text lines unchanged')
        return rendered,evidence
    return _prepare_packaged_manual(source,tool)

def _prepare_packaged_manual(source,tool):
    units=[]
    for number,line in enumerate(source.splitlines(keepends=True),1):
        unit={'raw':line,'first_line':number}
        if line.startswith(('.\\"',"'\\\"")):
            unit['kind']='comment'
        elif line.startswith('.'):
            m=re.fullmatch(r'\.([A-Za-z]+)(?:[ \t]+(.*))?\r?\n?',line)
            if not m or m[1] not in ALLOWED:
                raise ValueError('Unknown package-manual request at line '+str(number))
            unit.update(kind=m[1],args=arguments(m[2] or ''))
        elif line.startswith("'"):
            raise ValueError('Unknown alternate control at line '+str(number))
        else:
            unit.update(kind='text',text=line.rstrip('\r\n'))
        units.append(unit)
    assert ''.join(x['raw'] for x in units)==source
    titles=[x for x in units if x['kind']=='TH']
    if len(titles)!=1 or len(titles[0]['args'])<2:
        raise ValueError('One TH title with name and section required')
    title=titles[0]['args']
    if title[0].lower()!=tool:
        raise ValueError('Package/manual name mismatch')
    out=['# '+tool+'\n\n']
    paragraph=[]; term=[]; literal=[]; blocks=[]; sections=[]; options=[]; layouts=[]; tables=[]
    section=None; nofill=False; in_term=False; first_literal=None; bullet=False
    def flush():
        nonlocal bullet
        if paragraph:
            out.append(('- ' if bullet else '')+' '.join(paragraph)+'\n\n')
            paragraph.clear()
            bullet=False
    def flush_term():
        nonlocal in_term
        if term:
            value=' '.join(term)
            out.append('### '+value+'\n\n')
            if section=='OPTIONS': options.append(value.replace(BT,''))
            term.clear()
        in_term=False
    def flush_literal():
        nonlocal first_literal
        if literal:
            body='\n'.join(literal).strip('\n')+'\n'
            if section=='SYNOPSIS' and not nofill:
                body='\n\n'.join(' '.join(p.splitlines()) for p in body.strip().split('\n\n'))+'\n'
            if BT*3 in body: raise ValueError('Fence collision')
            if tool=='nbtscan' and section=='NETBIOS SUFFIXES':
                rows=[re.split(r'\s{2,}',line.strip()) for line in body.splitlines() if line.strip() and not re.fullmatch(r'[-\s]+',line)]
                assert rows[0]==['Name','Number(h)','Type','Usage'],'Unreviewed NetBIOS reference-table header'
                assert all(len(row)==4 for row in rows),'Unreviewed NetBIOS reference-table columns'
                out.append('| '+' | '.join(rows[0])+' |\n|---|---|---|---|\n')
                for row in rows[1:]:
                    out.append('| '+' | '.join([BT+x+BT for x in row[:3]]+[row[3]])+' |\n')
                out.append('\n')
                tables.append({'first_line':first_literal,'decoded_original_body':body,'rows':rows,'presentation':'First three identifier columns literal; service usage descriptions translatable'})
            else:
                out.append(BT*3+'text\n'+body+BT*3+'\n\n')
                blocks.append({'first_line':first_literal,'body':body,'origin':'decoded non-executing roff presentation'})
            literal.clear()
        first_literal=None
    for unit in units:
        kind=unit['kind']; args=unit.get('args',[])
        if kind in {'comment','TH'}: continue
        if kind=='SH':
            flush_term(); flush(); flush_literal()
            section=decode(' '.join(args)); sections.append(section)
            out.append('## '+section+'\n\n'); nofill=False
        elif kind=='SS':
            flush_term(); flush(); flush_literal()
            out.append('### '+decode(' '.join(args))+'\n\n')
        elif kind in {'P','PP','TP','IP'}:
            flush_term(); flush()
            if nofill or section=='SYNOPSIS': literal.append('')
            elif kind=='TP': in_term=True
            elif kind=='IP':
                if args and decode(args[0])=='•': bullet=True
                elif args:
                    term.append(BT+decode(args[0])+BT)
                    flush_term()
        elif kind in {'nf','fi','fam','in','sp','RS','RE','IX'}:
            layouts.append({'first_line':unit['first_line'],'request':kind,'args':args})
            if kind=='nf':
                flush_term(); flush(); nofill=True
            elif kind=='fi':
                flush_literal(); nofill=False
            elif kind=='sp':
                if nofill: literal.append('')
                else: flush()
        elif kind in STYLES or kind=='text':
            is_literal=nofill or section=='SYNOPSIS'
            value=styled(kind,args,is_literal) if kind in STYLES else decode(unit['text'])
            if is_literal:
                if first_literal is None: first_literal=unit['first_line']
                literal.append(value)
            elif in_term and kind in STYLES:
                if value: term.append(value)
            elif in_term and not term:
                term.append(BT+value+BT)
                flush_term()
            else:
                flush_term()
                if value.startswith('• '):
                    flush(); bullet=True; value=value[2:]
                if value.strip(): paragraph.append(value.strip())
                else: flush()
        else: raise AssertionError(kind)
    flush_term(); flush(); flush_literal()
    return ''.join(out),{
        'format':'packaged-man-roff-v1','title':title,
        'source_lines':len(source.splitlines()),'all_source_text_accounted':True,
        'sections':sections,'option_syntax':options,'literal_blocks':blocks,
        'layout_requests':layouts,
        **({'reference_tables':tables} if tables else {}),
        'source_comments':[x for x in units if x['kind']=='comment'],
        'presentation_changes':[
            'Strict man requests interpreted as data; no external formatter, includes or shell executed',
            'Paragraph lines joined; style macros mapped to inline code',
            'Synopsis/no-fill rendered with explicit font, zero-width and spacing escape decoding',
            'Raw source bytes retained separately; non-content layout requests recorded',
            'Historical statements translated from dated source, not independently retested claims'
        ]}
