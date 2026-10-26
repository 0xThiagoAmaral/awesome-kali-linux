#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fixtures for tables, equations, nested fonts and complete literal transcripts."""
import unittest
from roff_extended_manual import prepare_extended_roff,decode,table_markdown
from roff_manual import parse_roff

BASE='.\\" Copyright Example\n.\\" Copying and distribution permitted.\n.TH TOOL 1 "January 01, 2025"\n'

class ExtendedRoffTests(unittest.TestCase):
    def test_nested_font_option_keeps_syntax(self):
        source=BASE+'.SH OPTIONS\n.SS "General Options"\n.TP\n'+r'\fB--interface\fP=\fI<s>\fP or \fB-I \fI<s>\fR'+'\nDescription.\n'
        _,e=prepare_extended_roff(source,'tool')
        self.assertEqual(e['option_syntax'],['--interface=<s> or -I <s>'])

    def test_whitespace_only_segments_are_not_duplicated(self):
        self.assertEqual(decode(' '),' ')

    def test_ip_argument_type_and_subsection_are_retained(self):
        source=BASE+'.SH OPTIONS\n.IP '+r'\fB<s>\fP'+'\nCharacter string.\n.SS "General Options"\n'
        md,e=prepare_extended_roff(source,'tool')
        self.assertEqual(e['argument_types'],['<s>'])
        self.assertEqual(e['subsections'],['General Options'])
        self.assertIn('Character string.',md)

    def test_original_equation_is_preserved(self):
        source=BASE+'.SH DESCRIPTION\n.EQ\ntime = n times i + t + o\n.EN\n'
        md,e=prepare_extended_roff(source,'tool')
        self.assertEqual(e['equations'][0]['raw_body'],'time = n times i + t + o\n')
        self.assertIn('time = n × i + t + o',md)

    def test_packet_table_keeps_all_data_and_caption(self):
        body='box;\nL L L L.\nPacket Options\n=\nField\tBits\tOption\tDefault\n=\nar$hrd\t16\t--arphrd\t1 (ARPHRD_ETHER)\n'
        md,e,_=table_markdown({'body':body,'first_line':1},1)
        for literal in ['Packet Options','ar$hrd','16','--arphrd','1 (ARPHRD_ETHER)']:
            self.assertIn(literal,md)
        self.assertEqual(e['raw_body'],body)

    def test_original_tbl_command_escapes_are_not_repaired(self):
        body="L .\n--format='${ip}"+chr(92)*2+"t${mac}'"+chr(92)+"n\n"
        _,_,blocks=table_markdown({'body':body,'first_line':1},1)
        self.assertEqual(blocks[0]['body'],body.split('\n',1)[1])

    def test_unknown_or_unclosed_preprocessor_blocks_fail(self):
        for text in ['.EQ\nx\n','.TS\nL .\nx\n']:
            with self.assertRaises(ValueError):
                parse_roff(BASE+text)

    def test_os_definition_heading_remains_translatable_prose(self):
        md,_=prepare_extended_roff(BASE+'.SH DESCRIPTION\n.TP\nBSD and macOS:\nNeeds BPF access.\n','tool')
        self.assertIn('### BSD and macOS:',md)
        self.assertNotIn('### '+chr(96)+'BSD',md)

if __name__=='__main__':
    unittest.main()
