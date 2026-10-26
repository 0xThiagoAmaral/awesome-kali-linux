#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Roff fixtures verify safety, exact examples, option syntax and copying notices."""
import unittest
from roff_manual import parse_roff,prepare_roff_manual

NOTICE='.\\" Copyright Example\n.\\" Copying permitted with notice.\n'
BASE=NOTICE+'.TH TOOL 1 "January 01, 2023"\n'

class RoffManualTests(unittest.TestCase):
    def test_raw_input_reconstructs_exactly(self):
        source=BASE+'.SH NAME\ntool \\- example\n'
        self.assertEqual(''.join(x['raw'] for x in parse_roff(source)),source)

    def test_shell_and_file_inclusion_requests_fail_closed(self):
        for request in ['.sy whoami\n','.pso echo secret\n','.so /etc/passwd\n']:
            with self.assertRaisesRegex(ValueError,'Unsupported roff request'):
                parse_roff(BASE+request)

    def test_exact_example_body_and_notice(self):
        body='$ tool 192.0.2.1  \noriginal output  \n'
        md,e=prepare_roff_manual(BASE+'.SH EXAMPLES\n.nf\n'+body+'.fi\n','tool')
        self.assertEqual(e['literal_blocks'][0]['body'],body)
        self.assertEqual(e['license_notice'],NOTICE)
        self.assertIn(NOTICE,md)

    def test_synopsis_keeps_original_tokens(self):
        source=BASE+'.SH SYNOPSIS\n.B tool\n.RI [ options ]\n.I target\n.PP\nDescription.\n'
        _,e=prepare_roff_manual(source,'tool')
        self.assertEqual(e['literal_blocks'][0]['body'],'tool [options] target\n')

    def test_unclosed_verbatim_block_fails(self):
        with self.assertRaisesRegex(ValueError,'Unclosed'):
            parse_roff(BASE+'.nf\ncommand\n')

    def test_options_are_not_translated(self):
        source=BASE+'.SH OPTIONS\n.TP\n.B -o <option-string>\nPass options.\n'
        md,e=prepare_roff_manual(source,'tool')
        self.assertEqual(e['option_syntax'],['-o <option-string>'])
        self.assertIn('-o <option-string>',md)

    def test_unknown_escape_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'Unsupported roff escape'):
            prepare_roff_manual(BASE+'.SH NAME\nvalue \\*[unknown]\n','tool')

    def test_macro_argument_escapes_and_alternate_controls_fail(self):
        for line in ['.B bad\\escape\n',"'so /etc/passwd\n"]:
            with self.assertRaises(ValueError):
                parse_roff(BASE+line)

if __name__=='__main__':
    unittest.main()
