#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Explicit source-bound layout repairs, never edits to the preserved original."""
import hashlib
ARPING_SHA='de74f6c4e808c9fb7003e4ad03c1fa0df98cf4c677b9cd4aeb647a3316f444d8'

def repair_arping_layout(source):
    if hashlib.sha256(source.encode()).hexdigest()!=ARPING_SHA:
        raise ValueError('Unreviewed arping manual version; layout rules require exact source identity')
    edits=[
        ('.nf\n.sp\nTo check the address', 'To check the address'),
        ('.PP \n$ arping \\-S', '.PP \n.nf\n$ arping \\-S'),
        ('.IP "\\-u"', '.fi\n.IP "\\-u"'),
        ('.IP "\\-v"', '.fi\n.IP "\\-v"'),
        ('# nice \\-n \\-15 arping foobar\n', '.nf\n# nice \\-n \\-15 arping foobar\n.fi\n'),
        ('git clone http://github\\&.com/ThomasHabets/arping\\&.git\n',
         '.nf\ngit clone http://github\\&.com/ThomasHabets/arping\\&.git\n.fi\n')]
    amended=source
    repairs=[]
    for before,after in edits:
        assert amended.count(before)==1,'Layout repair does not match once: '+before
        amended=amended.replace(before,after)
        repairs.append({'before':before,'after':after,'occurrences':1})
    # Every non-request source line remains byte-for-byte, in order.
    text=lambda s:[line for line in s.splitlines(keepends=True) if not line.startswith('.')]
    assert text(source)==text(amended),'A layout repair changed source text'
    return amended,repairs

DNSENUM_SHA='ef15de4554816ca9298fe894e4b1f2d3a2281ee1a50cad5f25e7e49d0f217800'
DNSRECON_SHA='e57945a2a52ccca3d4200b41cfca13cbfb024ead0413ba373306211e1af00430'

def prepare_dns_package_layout(source,tool):
    expected={'dnsenum':DNSENUM_SHA,'dnsrecon':DNSRECON_SHA}[tool]
    if hashlib.sha256(source.encode()).hexdigest()!=expected:
        raise ValueError('Unreviewed '+tool+' manual source; new layout review required')
    if tool=='dnsenum':
        marker='.TH DNSENUM 1 '
        assert source.count(marker)==1
        offset=source.index(marker)
        preamble=source[:offset]
        body=source[offset:]
        assert body.count('.if n .ad l\n')==1 and body.count('.nh\n')==1
        body=body.replace('.if n .ad l\n','').replace('.nh\n','').replace('.Sp\n','.sp\n')
        return body,{'source_sha256':expected,'original_preamble':preamble,
            'preamble_sha256':hashlib.sha256(preamble.encode()).hexdigest(),
            'changes':['Exact Pod::Man generated preamble retained here and in raw source, not executed',
                       'Two exact justification/hyphenation requests omitted from Markdown layout',
                       'Pod::Man Sp mapped to sp; IX index markers retained as metadata, never executed']}
    before='.TP\n.B attempts a zone transfer (AXFR) on the zonetransfer.me domain\ndnsrecon -t axfr -d zonetransfer.me\n'
    after='.PP\nattempts a zone transfer (AXFR) on the zonetransfer.me domain\n.nf\ndnsrecon -t axfr -d zonetransfer.me\n.fi\n'
    assert source.count(before)==1
    return source.replace(before,after),{'source_sha256':expected,'changes':[
        'Example prose made translatable instead of treating its bold explanatory sentence as an option identifier',
        'Exact example command fenced; no command executed; missing manual date remains null'],
        'replacement':{'before':before,'after':after,'occurrences':1}}

FPING_SHA='3a8c8083d52de352e65c96e6b267c61806666b3dd387c5f1146b496037bb6995'
FPING6_SHA='51970fc71574ef3e370041c2660df7e720a2607d95a1aec7ed83ac7b52987271'
def prepare_fping_layout(source):
    digest=hashlib.sha256(source.encode()).hexdigest()
    names={FPING_SHA:'fping',FPING6_SHA:'fping6'}
    if digest not in names:
        raise ValueError('Unreviewed fping package manual; source-specific Pod layout review required')
    binary=names[digest]
    marker='.TH '+binary.upper()+' 8 '
    assert source.count(marker)==1
    offset=source.index(marker)
    preamble=source[:offset];body=source[offset:]
    assert body.count('.if n .ad l\n')==1 and body.count('.nh\n')==1
    body=body.replace('.if n .ad l\n','').replace('.nh\n','').replace('.Sp\n','.sp\n')
    return body,binary,{'source_sha256':digest,'original_preamble':preamble,
        'preamble_sha256':hashlib.sha256(preamble.encode()).hexdigest(),
        'changes':['Exact generated Pod::Man preamble retained as data, never executed',
                   'Only exact source-bound justification/hyphenation/Sp layout mappings applied',
                   'Vb/Ve verbatim blocks and known font/size/quote escapes rendered without macro execution']}

TCPDUMP_SHA='a683c08e923292a49006a2efe59eddddb64616bf684c55f56eb5c1a4c0bd3a91'
def prepare_tcpdump_layout(source):
    if hashlib.sha256(source.encode()).hexdigest()!=TCPDUMP_SHA:
        raise ValueError('Unreviewed tcpdump manual; source-specific macro review required')
    definition='.de HD\n.sp 1.5\n.B\n..\n'
    assert source.count(definition)==1 and source.count('\n.HD\n')==1
    body=source.replace(definition,'').replace('\n.HD\n','\n.sp 1.5\n.B\n')
    text=lambda s:[x for x in s.splitlines(keepends=True) if not x.startswith('.')]
    assert text(body)==text(source),'Macro-layout mapping changed source text'
    return body,{'source_sha256':TCPDUMP_SHA,'original_macro_definition':definition,
        'changes':['Exact HD macro definition retained as provenance, not executed',
                   'Its single call mapped explicitly to spacing/bold requests',
                   'All non-request source lines unchanged; protocol sections and literal examples retained']}
