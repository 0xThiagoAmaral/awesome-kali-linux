#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Loss-accounted converter for sectioned plain-text manuals, not arbitrary text."""
import re

BT=chr(96)
SECTIONS={'NAME','SYNOPSIS','DESCRIPTION','OPTIONS','NOTE','NOTES','RETURN VALUE',
          'EXAMPLES','FILES','COPYRIGHT','HELP THIS PROJECT','SEE ALSO','AUTHORS'}
OPTION=re.compile(r'^\s+(--[a-z][a-z0-9-]*(?:=[a-z]+|\[[^\]]+\])?(?:,\s+-[A-Za-z0-9](?:\[[^\]]+\]|\s+x)?)?)\s+(.*)$')
FILE=re.compile(r'^\s+((?:/|~/)\S+)\s{2,}(.*)$')

def parse_manual(source):
    lines=source.splitlines(keepends=True)
    result=[]
    section=None
    index=0
    while index<len(lines):
        line=lines[index]
        stripped=line.strip()
        start=index
        if not stripped:
            result.append({'kind':'blank','raw':line,'first_line':index+1})
            index+=1
            continue
        if not line[0].isspace() and re.fullmatch(r'[A-Z][A-Z ]+',stripped):
            if stripped not in SECTIONS:
                raise ValueError('Unsupported manual section: '+stripped)
            section=stripped
            result.append({'kind':'section','text':section,'raw':line,'first_line':index+1})
            index+=1
            continue
        if section is None:
            raise ValueError('Expected a named manual section before prose')
        if section=='SYNOPSIS' or line.startswith('    $ '):
            while index<len(lines) and lines[index].strip():
                if section!='SYNOPSIS' and not (lines[index].startswith(('    $ ','      '))):
                    break
                index+=1
            result.append({'kind':'literal-block','raw':''.join(lines[start:index]),'section':section,'first_line':start+1})
            continue
        match=OPTION.match(line) if section=='OPTIONS' else FILE.match(line) if section=='FILES' else None
        if line.lstrip().startswith('--') and section=='OPTIONS' and not match:
            raise ValueError('Unrecognized option syntax on line '+str(index+1))
        if match:
            syntax,description=match.groups()
            index+=1
            continuation=[]
            while index<len(lines) and lines[index].strip():
                if OPTION.match(lines[index]) or FILE.match(lines[index]) or not lines[index][0].isspace():
                    break
                continuation.append(lines[index].strip())
                index+=1
            result.append({'kind':'option' if section=='OPTIONS' else 'file',
                           'literal':syntax,'text':' '.join([description]+continuation),
                           'raw':''.join(lines[start:index]),'section':section,'first_line':start+1})
            continue
        while index<len(lines) and lines[index].strip():
            candidate=lines[index]
            if index>start and (not candidate[0].isspace() or candidate.startswith('    $ ') or
                               section=='OPTIONS' and OPTION.match(candidate) or section=='FILES' and FILE.match(candidate)):
                break
            index+=1
        result.append({'kind':'paragraph','text':' '.join(x.strip() for x in lines[start:index]),
                       'raw':''.join(lines[start:index]),'section':section,'first_line':start+1})
    assert ''.join(item['raw'] for item in result)==source,'Source bytes were omitted by parser'
    return result

def protect_prose(text):
    pattern=r'--[a-z][a-z0-9-]*|getopt_long|NETRC|AUTHORS|CREDITS|CONTRIBUTING\.md|ftp\(1\)|(?<![\w/])~?/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+/?|(?<!\w)doc/|(?<!\w)\.netrc\b|\b(?:[Aa]xel|FTP|FTPS|HTTP|HTTPS|TLS|SSL|Cookie|Authorization|Proxy-Authorization)\b|"Header: Value"|Wilmer van der Gaast'
    return re.sub(r'https?://[^\s<>]+|(?P<literal>'+pattern+')',
                  lambda m:BT+m.group()+BT if m.lastgroup=='literal' else m.group(),text)

def prepare_manual(source,tool):
    units=parse_manual(source)
    out=['# '+tool+'\n\n']
    for item in units:
        kind=item['kind']
        if kind=='blank':
            continue
        if kind=='section':
            out.append('## '+item['text']+'\n\n')
        elif kind=='literal-block':
            body=item['raw']
            if not body.endswith('\n'):
                raise ValueError('Non-terminated command block requires explicit handling')
            if BT*3 in body:
                raise ValueError('Fence collision in plain-text command block')
            out.append(BT*3+'text\n'+body+BT*3+'\n\n')
        elif kind in ['option','file']:
            out.append('### '+BT+item['literal']+BT+'\n\n'+protect_prose(item['text'])+'\n\n')
        else:
            out.append(protect_prose(item['text'])+'\n\n')
    markdown=''.join(out)
    evidence={'format':'sectioned-plain-text-v1','source_lines':len(source.splitlines()),
              'all_source_text_accounted':''.join(x['raw'] for x in units)==source,
              'sections':[x['text'] for x in units if x['kind']=='section'],
              'literal_blocks':[{'first_line':x['first_line'],'body':x['raw']} for x in units if x['kind']=='literal-block'],
              'option_syntax':[x['literal'] for x in units if x['kind']=='option'],
              'file_paths':[x['literal'] for x in units if x['kind']=='file'],
              'presentation_changes':['Plain manual sections mapped to Markdown headings',
                                      'Wrapped prose lines joined within paragraphs',
                                      'Original synopsis and prompt examples fenced without body changes',
                                      'Option syntax and configuration paths protected as inline literals']}
    return markdown,evidence
