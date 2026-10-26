#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Non-executing man/tbl/eqn conversion with preserved raw structures and literals."""
import re
from roff_manual import parse_roff

BT=chr(96)

def decode(text,styled=True):
    out=[]; index=0; font='R'; buf=[]
    def flush():
        if buf:
            value=''.join(buf); buf.clear()
            if not value.strip():
                out.append(value); return
            lead=value[:len(value)-len(value.lstrip())]
            trail=value[len(value.rstrip()):]
            core=value.strip()
            out.append(lead+(BT+core+BT if styled and font in {'B','I'} and core else core)+trail)
    while index<len(text):
        if text[index]!='\\':
            buf.append(text[index]); index+=1; continue
        if text.startswith(r'\\',index):
            buf.append('\\'); index+=2
        elif text.startswith(r'\-',index):
            buf.append('-'); index+=2
        elif text.startswith(r'\f',index) and index+2<len(text) and text[index+2] in 'BIPR':
            flush(); font='R' if text[index+2] in 'PR' else text[index+2]; index+=3
        else:
            raise ValueError('Unsupported roff escape: '+text[index:index+16])
    flush()
    return ''.join(out)

def plain_macro(unit):
    return (' '.join(unit['args']) if unit['kind'] in {'B','I'} else ''.join(unit['args']))

def style_macro(unit):
    if unit['kind'] in {'B','I'}:
        value=' '.join(unit['args'])
        punctuation=re.fullmatch(r'(.+\w)([.,;:])',value)
        if punctuation and not value.startswith(('https://','http://')):
            return BT+punctuation.group(1)+BT+punctuation.group(2)
        return '['+value+']('+value+')' if value.startswith(('https://','http://')) else BT+value+BT
    return ''.join(BT+v+BT if i%2==0 and re.search(r'\w',v) else v for i,v in enumerate(unit['args']))

def table_data(body):
    lines=body.splitlines()
    end=next((i for i,line in enumerate(lines) if line.rstrip().endswith('.')),None)
    if end is None:
        raise ValueError('Unsupported tbl layout')
    layout=lines[:end+1]
    data=[line for line in lines[end+1:] if line.strip() and line.strip() not in {'=','_'}]
    if not data:
        raise ValueError('Empty tbl data')
    rows=[line.split('\t') for line in data]
    widths={len(row) for row in rows}
    return layout,rows,widths

def table_markdown(unit,number):
    layout,rows,widths=table_data(unit['body'])
    result=[]; literal=[]; mode=None
    def code(value):
        return BT+decode(value,False)+BT
    if widths=={1}:
        # Keep original tbl command notation, including its source escapes; do not silently repair it.
        mode='source-command-notation'
        result.append('Original tbl format examples (source notation)\n\n')
        body=''.join(line for line in unit['body'].splitlines(keepends=True)[len(layout):])
        result.append(BT*3+'text\n'+body+BT*3+'\n\n')
        literal.append({'body':body,'origin':'exact original tbl command notation','first_line':unit['first_line']})
    elif widths=={3} and len(rows)==1:
        mode='literal-output-pattern'
        body='\t'.join(rows[0])+'\n'
        result.append(BT*3+'text\n'+body+BT*3+'\n\n')
        literal.append({'body':body,'origin':'original output pattern from tbl','first_line':unit['first_line']})
    elif widths=={3} and all(row[0] in {'MA-L','MA-M','MA-S','IAB'} for row in rows):
        mode='ieee-registry-definitions'
        result.append('| Registry | Prefix size | Description |\n|---|---|---|\n')
        for registry,bits,description in rows:
            result.append('| '+code(registry)+' | '+code(bits)+' | '+decode(description)+' |\n')
        result.append('\n')
    elif 4 in widths and widths.issubset({1,4}):
        mode='packet-fields'
        if len(rows[0])==1:
            result.append(rows.pop(0)[0]+'\n\n')
        if rows[0]!=['Field','Bits','Option','Default']:
            raise ValueError('Unexpected four-column tbl header')
        result.append('| Field | Bits | Option | Default |\n|---|---|---|---|\n')
        prose_defaults={'interface h/w address','interface IPv4 address','target host IPv4 address','interface address','None'}
        for row in rows[1:]:
            if len(row)!=4:
                raise ValueError('Unexpected tbl row width')
            field,bits,option,default=row
            field=code(field) if field.startswith('ar$') else field
            default=default if default in prose_defaults else code(default)
            option=option if option=='None' else code(option)
            result.append('| '+field+' | '+code(bits)+' | '+option+' | '+default+' |\n')
        result.append('\n')
    elif widths=={2}:
        mode='field-definitions' if rows[0][0]=='IP' else 'escape-definitions'
        result.append('| Field | Description |\n|---|---|\n')
        for key,value in rows:
            result.append('| '+code(key)+' | '+decode(value)+' |\n')
        result.append('\n')
    else:
        raise ValueError('Unsupported tbl data shape: '+repr(widths))
    evidence={'number':number,'first_line':unit['first_line'],'raw_body':unit['body'],
              'layout':layout,'rows':rows,'rendering':mode}
    return ''.join(result),evidence,literal

def prepare_extended_roff(source,tool):
    units=parse_roff(source)
    titles=[u for u in units if u['kind']=='TH']
    if len(titles)!=1 or len(titles[0]['args'])<3:
        raise ValueError('Expected one dated manpage title')
    out=['# '+titles[0]['args'][0].lower()+'\n\n']
    paragraphs=[]; sections=[]; subsections=[]; options=[]; arguments=[]; literals=[]; tables=[]; equations=[]
    section=None; term=False; index=0; has_subsection=False
    def flush():
        if paragraphs:
            out.append(' '.join(paragraphs)+'\n\n'); paragraphs.clear()
    while index<len(units):
        u=units[index]; kind=u['kind']
        if kind in {'comment','TH'}:
            index+=1; continue
        if kind in {'SH','SS'}:
            flush(); term=False
            value=' '.join(u['args'])
            if kind=='SH':
                section=value; sections.append(value); has_subsection=False
            else:
                subsections.append(value); has_subsection=True
            out.append(('## ' if kind=='SH' else '### ')+value+'\n\n')
            index+=1
            if kind=='SH' and section=='SYNOPSIS':
                parts=[]; first=index
                while index<len(units) and units[index]['kind'] not in {'PP','SH','SS'}:
                    v=units[index]
                    if v['kind'] not in {'B','I','RI','BR','IR'}:
                        raise ValueError('Unsupported main synopsis')
                    parts.append(plain_macro(v)); index+=1
                body=' '.join(parts)+'\n'
                out.append(BT*3+'text\n'+body+BT*3+'\n\n')
                literals.append({'body':body,'first_line':units[first]['first_line'],'origin':'rendered roff synopsis'})
            continue
        if kind in {'PP','sp','TP'}:
            flush(); term=kind=='TP'
        elif kind=='IP':
            flush(); label=decode(u['args'][0],False)
            arguments.append(label)
            out.append('### '+BT+label+BT+'\n\n')
        elif kind in {'table','equation','literal-block'}:
            flush()
            if kind=='table':
                rendered,evidence,blocks=table_markdown(u,len(tables)+1)
                out.append(rendered); tables.append(evidence); literals.extend(blocks)
            else:
                body=u['body']
                if not body.endswith('\n') or BT*3 in body:
                    raise ValueError('Invalid literal termination')
                out.append(BT*3+'text\n'+body+BT*3+'\n\n')
                literals.append({'body':body,'first_line':u['first_line'],'origin':'exact '+kind+' body'})
                if kind=='equation':
                    equations.append({'raw_body':body,'first_line':u['first_line']})
                    if body.strip()=='time = n times i + t + o':
                        out.append('Equivalent mathematical notation: '+BT+'time = n × i + t + o'+BT+'.\n\n')
        elif kind in {'B','I','RI','BR','IR','text'}:
            raw=u['text'] if kind=='text' else plain_macro(u)
            value=decode(raw) if kind=='text' else style_macro(u)
            if term and raw.strip():
                syntax=decode(raw,False)
                heading=BT+syntax+BT if section in {'OPTIONS','FILES'} else value
                out.append(('#### ' if has_subsection else '### ')+heading+'\n\n')
                if section=='OPTIONS':
                    options.append(syntax)
                term=False
            elif raw.strip():
                paragraphs.append(value.strip())
            else:
                flush()
        else:
            raise ValueError('Unconverted main-manual unit: '+kind)
        index+=1
    flush()
    header=units[:units.index(titles[0])]
    comments=[u['raw'] for u in header if u['raw'].startswith('.\\"')]
    notice=''.join(comments)
    if 'Copyright' not in notice or 'Copying and distribution' not in notice:
        raise ValueError('Original copying notice missing')
    out.append('## Original license notice\n\n'+BT*3+'text\n'+notice+BT*3+'\n')
    literals.append({'body':notice,'first_line':2,'origin':'exact original copying notice'})
    evidence={'format':'man-roff-extended-v1','source_lines':len(source.splitlines()),
              'all_source_text_accounted':''.join(u['raw'] for u in units)==source,
              'title':titles[0]['args'],'sections':sections,'subsections':subsections,
              'option_syntax':options,'argument_types':arguments,'literal_blocks':literals,
              'tables':tables,'equations':equations,'license_notice':notice,
              'presentation_changes':['Non-executing parsing of man/tbl/eqn requests',
                                      'Tables rendered with all data cells retained; source tbl structures recorded',
                                      'Ambiguous tbl command examples kept in exact original source notation',
                                      'Original eqn formula retained with equivalent multiplication notation',
                                      'Literal command transcripts and original copying notice preserved']}
    return ''.join(out),evidence
