#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Strict, non-executing roff-man subset converter; unknown requests fail closed."""
import re
import shlex

BT=chr(96)
REQUESTS={'TH','SH','SS','PP','TP','IP','sp','B','I','RI','BR','IR','nf','fi','EQ','EN','TS','TE'}

def parse_roff(source):
    lines=source.splitlines(keepends=True)
    units=[]
    index=0
    while index<len(lines):
        line=lines[index]
        first=index+1
        if line.startswith(('.\\"',"'\\\"")):
            units.append({'kind':'comment','raw':line,'first_line':first})
        elif line.startswith('.'):
            match=re.fullmatch(r'\.([A-Za-z]+)(?:[ \t]+(.*))?\r?\n?',line)
            if not match or match.group(1) not in REQUESTS:
                raise ValueError('Unsupported roff request at line '+str(first))
            request,args=match.group(1),match.group(2) or ''
            if '\\' in args and request!='IP':
                raise ValueError('Unsupported escape in roff macro arguments at line '+str(first))
            if request in {'nf','EQ','TS'}:
                closing={'nf':'fi','EQ':'EN','TS':'TE'}[request]
                body=[]
                raw=[line]
                index+=1
                while index<len(lines) and lines[index].strip()!='.'+closing:
                    if lines[index].startswith('.'):
                        raise ValueError('Unexpected request inside literal block at line '+str(index+1))
                    body.append(lines[index]); raw.append(lines[index]); index+=1
                if index==len(lines):
                    raise ValueError('Unclosed .'+request+' block')
                raw.append(lines[index])
                units.append({'kind':{'nf':'literal-block','EQ':'equation','TS':'table'}[request],
                              'body':''.join(body),'raw':''.join(raw),'first_line':first})
            elif request in {'fi','EN','TE'}:
                raise ValueError('Unexpected closing roff request: .'+request)
            else:
                units.append({'kind':request,'args':[args] if request=='IP' else shlex.split(args),'raw':line,'first_line':first})
        elif line.startswith("'"):
            raise ValueError('Unsupported alternate roff control line at '+str(first))
        else:
            units.append({'kind':'text','text':line.rstrip('\r\n'),'raw':line,'first_line':first})
        index+=1
    assert ''.join(x['raw'] for x in units)==source
    return units

def decode_roff(text):
    text=text.replace(r'\-', '-')
    text=re.sub(r'\\f[BI]([^\\]+)\\f[PR]',lambda m:BT+m.group(1)+BT,text)
    if '\\' in text:
        raise ValueError('Unsupported roff escape in prose: '+text)
    return text

def inline_style(unit):
    args=unit['args']
    if unit['kind'] in {'B','I'}:
        value=' '.join(args)
        if value.startswith(('https://','http://')):
            return '<'+value+'>'
        return BT+value+BT
    # Alternating font macros concatenate arguments without implicit spaces.
    result=[]
    for index,value in enumerate(args):
        result.append(BT+value+BT if index%2==0 and re.search(r'\w',value) else value)
    return ''.join(result)

def prepare_roff_manual(source,tool):
    units=parse_roff(source)
    titles=[x for x in units if x['kind']=='TH']
    if len(titles)!=1 or len(titles[0]['args'])<3:
        raise ValueError('Expected one .TH title with section and date')
    name=titles[0]['args'][0].lower()
    out=['# '+name+'\n\n']
    paragraph=[]
    section=None
    term=False
    literal_blocks=[]
    options=[]
    sections=[]
    def flush():
        if paragraph:
            out.append(' '.join(paragraph)+'\n\n')
            paragraph.clear()
    index=0
    while index<len(units):
        unit=units[index]
        kind=unit['kind']
        if kind in {'comment','TH'}:
            index+=1; continue
        if kind=='SH':
            flush()
            section=' '.join(unit['args'])
            sections.append(section)
            out.append('## '+section+'\n\n')
            index+=1
            if section=='SYNOPSIS':
                syntax=[]
                first=index
                while index<len(units) and units[index]['kind'] not in {'PP','SH'}:
                    current=units[index]
                    if current['kind'] in {'B','I'}:
                        syntax.append(' '.join(current['args']))
                    elif current['kind'] in {'RI','BR','IR'}:
                        syntax.append(''.join(current['args']))
                    elif current['kind']=='text' and not current['text'].strip():
                        pass
                    else:
                        raise ValueError('Unsupported synopsis structure')
                    index+=1
                body=' '.join(syntax)+'\n'
                out.append(BT*3+'text\n'+body+BT*3+'\n\n')
                literal_blocks.append({'first_line':units[first]['first_line'],'body':body,'origin':'rendered roff synopsis'})
            continue
        if kind in {'PP','TP'}:
            flush()
            term=kind=='TP'
        elif kind=='literal-block':
            flush()
            body=unit['body']
            if not body.endswith('\n') or BT*3 in body:
                raise ValueError('Unsupported literal block termination or fence collision')
            out.append(BT*3+'text\n'+body+BT*3+'\n\n')
            literal_blocks.append({'first_line':unit['first_line'],'body':body,'origin':'exact .nf body'})
        elif kind in {'B','I','RI','BR','IR'}:
            value=inline_style(unit)
            if term:
                flush()
                out.append('### '+value+'\n\n')
                if section=='OPTIONS':
                    options.append(' '.join(unit['args']))
                term=False
            else:
                paragraph.append(value)
        elif kind=='text':
            if unit['text'].strip():
                text=decode_roff(unit['text'].strip())
                text=re.sub(r'(?<![\w-])(--[a-z][a-z-]*|-[A-Z])\b',lambda m:BT+m.group()+BT,text)
                paragraph.append(text)
            else:
                flush()
        else:
            raise ValueError('Unconverted roff unit: '+kind)
        index+=1
    flush()
    notice=''.join(x['raw'] for x in units[:units.index(titles[0])] if x['kind']=='comment')
    if not notice:
        raise ValueError('Expected the original file-specific license notice')
    out.append('## Original license notice\n\n'+BT*3+'text\n'+notice+BT*3+'\n')
    literal_blocks.append({'first_line':1,'body':notice,'origin':'exact original copyright and copying notice'})
    evidence={'format':'man-roff-v1','source_lines':len(source.splitlines()),'all_source_text_accounted':True,
              'sections':sections,'option_syntax':options,'literal_blocks':literal_blocks,
              'title':titles[0]['args'],'license_notice':notice,
              'presentation_changes':['Roff requests parsed without executing a formatter or shell',
                                      'Formatting requests mapped to Markdown, with paragraphs joined',
                                      'Synopsis rendered from original B/RI/I tokens',
                                      'Exact .nf examples, output and original license notice fenced unchanged']}
    return ''.join(out),evidence
