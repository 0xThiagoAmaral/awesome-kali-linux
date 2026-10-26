#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tests for non-executing package manual rendering and native provenance."""
import unittest
import copy
import json
import pathlib
import shutil
import tempfile
from package_source import validate_package_source,package_fields
from packaged_manual import prepare_packaged_manual,arguments,decode

HEADER='.TH "WHOIS" "1" "2019-12-30"\n'
class PackageManualTests(unittest.TestCase):
    def render(self,body):
        return prepare_packaged_manual(HEADER+body,'whois')
    def test_backslashes_preserved_in_arguments(self):
        self.assertEqual(arguments(r'"\-h" HOST'),[r'\-h','HOST'])
    def test_escape_decoding(self):
        self.assertEqual(decode(r'\fBa\-b\fP\&\~\(cq\:d'),"a-b 'd")
    def test_unknown_escape(self):
        with self.assertRaises(ValueError): decode(r'\*[shell]')
    def test_executable_requests_rejected(self):
        for line in ['.sy touch owned\n','.so /etc/passwd\n','.de malicious\n',".TS\n"]:
            with self.subTest(line=line),self.assertRaises(ValueError): self.render(line)
    def test_unknown_control_in_literal_rejected(self):
        with self.assertRaises(ValueError): self.render('.nf\n.sy touch owned\n.fi\n')
    def test_synopsis_macro_wrapping(self):
        text,info=self.render('.SH SYNOPSIS\n.B whois\n.B \\-q\n.I KEYWORD\n\n.B whois \\-\\-help\n')
        self.assertIn('whois -q KEYWORD\n\nwhois --help\n',text)
        self.assertTrue(info['all_source_text_accounted'])
    def test_option_parameters_not_lost(self):
        text,info=self.render('.SH OPTIONS\n.TP 8\n.B \\-h\n.IR HOST ,\n.BI \\-\\-host= HOST\nConnect.\n')
        self.assertIn('### '+chr(96)+'-h'+chr(96),text)
        self.assertEqual(info['option_syntax'],['-h HOST, --host=HOST'])
        self.assertNotIn(chr(96)*2,text)
    def test_literal_layout_and_duplicate_fi(self):
        text,info=self.render('.SH EXAMPLES\n.nf\n.fam C\nhello\\&.world\n.fam T\n.fi\n.fi\n')
        self.assertIn('hello.world\n',text)
        self.assertEqual(len(info['layout_requests']),5)
    def test_comments_retained_in_metadata(self):
        _,info=self.render('.SH AUTHOR\nOriginal author.\n.\\" SPDX-License-Identifier: GPL-2.0-or-later\n')
        self.assertIn('SPDX',info['source_comments'][0]['raw'])
    def test_wrong_title_rejected(self):
        with self.assertRaises(ValueError): prepare_packaged_manual(HEADER,'nbtscan')
    def test_unclosed_quote_rejected(self):
        with self.assertRaises(ValueError): self.render('.SH "BAD\n')

class NativeSourceTests(unittest.TestCase):
    def setUp(self):
        self.root=pathlib.Path(__file__).resolve().parents[1]
        self.record=json.loads((self.root/'catalog/source-registry.json').read_text(encoding='utf-8'))['whois']
        self.temp=tempfile.TemporaryDirectory(prefix='native-fixture-',dir=self.root/'evidence')
        self.addCleanup(self.temp.cleanup)
        self.assets=pathlib.Path(self.temp.name)/'assets'
        shutil.copytree(self.root/'vault/99-Assets/upstream/whois',self.assets)
    def test_real_snapshot(self):
        self.assertTrue(validate_package_source(self.record,self.assets))
        self.assertNotIn('source_commit',package_fields(self.record))
    def test_invented_git_commit_rejected(self):
        record=copy.deepcopy(self.record); record['commit']='f'*40
        with self.assertRaises(AssertionError): validate_package_source(record,self.assets)
    def test_version_drift_rejected(self):
        record=copy.deepcopy(self.record); record['binary_version']='999'
        with self.assertRaises(AssertionError): validate_package_source(record,self.assets)
    def test_copyright_tamper_rejected(self):
        (self.assets/'COPYRIGHT.package.txt').write_bytes(b'changed')
        with self.assertRaises(AssertionError): validate_package_source(self.record,self.assets)
    def test_gzip_tamper_rejected(self):
        (self.assets/'originals/whois.1.gz').write_bytes(b'changed')
        with self.assertRaises(AssertionError): validate_package_source(self.record,self.assets)
if __name__=='__main__':
    unittest.main()
