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
