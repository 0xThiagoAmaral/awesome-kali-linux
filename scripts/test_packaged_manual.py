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
from package_layout_repairs import repair_arping_layout,ARPING_SHA
from package_layout_repairs import prepare_dns_package_layout,DNSENUM_SHA,DNSRECON_SHA
from package_layout_repairs import prepare_fping_layout,FPING_SHA,FPING6_SHA
from test_dns_help import extract_help_flags
from import_translate_docs import code_bodies
import hashlib
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

class ArpingLayoutTests(unittest.TestCase):
    def setUp(self):
        self.root=pathlib.Path(__file__).resolve().parents[1]
        self.raw=(self.root/'sources/upstream/arping/arping.8.source').read_bytes()
        self.source=self.raw.decode('utf-8')
    def test_source_identity_and_no_text_edits(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),ARPING_SHA)
        adjusted,repairs=repair_arping_layout(self.source)
        self.assertEqual(len(repairs),6)
        lines=lambda text:[x for x in text.splitlines(keepends=True) if not x.startswith('.')]
        self.assertEqual(lines(adjusted),lines(self.source))
    def test_changed_source_requires_new_review(self):
        with self.assertRaises(ValueError): repair_arping_layout(self.source+'\n')
    def test_options_do_not_disappear_into_unclosed_nf(self):
        rendered,info=prepare_packaged_manual(self.source,'arping')
        self.assertEqual(len(info['sections']),8)
        self.assertEqual(len(info['option_syntax']),34)
        self.assertIn('-u',info['option_syntax'])
        self.assertIn('-Z',info['option_syntax'])
        self.assertEqual(len(code_bodies(rendered)),6)
        self.assertNotIn('Show index',''.join(code_bodies(rendered)))
        self.assertIn('Example: To check the address of MAC-A',rendered)
    def test_transcript_glyphs_and_commands_preserved(self):
        rendered,_=prepare_packaged_manual(self.source,'arping')
        self.assertIn('60 bytes from 00:11:85:4c:01:01 (88.1.180.225): index=0 time=13.910 msec',rendered)
        self.assertIn('$ arping -S <IP-B> -s <MAC-B> -p <MAC-A>',rendered)
        self.assertIn('git clone http://github.com/ThomasHabets/arping.git',rendered)
    def test_native_snapshot(self):
        record=json.loads((self.root/'catalog/source-registry.json').read_text(encoding='utf-8'))['arping']
        self.assertTrue(validate_package_source(record,self.root/'vault/99-Assets/upstream/arping'))

class NbtscanManualTests(unittest.TestCase):
    def setUp(self):
        self.root=pathlib.Path(__file__).resolve().parents[1]
        self.source=(self.root/'sources/upstream/nbtscan/nbtscan.1.source').read_text(encoding='utf-8')
        self.rendered,self.info=prepare_packaged_manual(self.source,'nbtscan')
    def test_all_sections_and_argument_forms(self):
        self.assertEqual(len(self.info['sections']),8)
        self.assertEqual(len(self.info['option_syntax']),16)
        self.assertIn('-h',self.info['option_syntax'])
        self.assertIn('xxx.xxx.xxx.xxx-xxx',self.info['option_syntax'])
    def test_reference_table_all_rows(self):
        table=self.info['reference_tables'][0]
        self.assertEqual(len(table['rows'])-1,29)
        self.assertEqual(table['rows'][-1],['<IS~computer name>','00','U','IIS'])
        self.assertIn('<\\--__MSBROWSE__>',self.rendered)
    def test_literal_output_stays_original(self):
        bodies=code_bodies(self.rendered)
        self.assertEqual(len(bodies),9)
        self.assertIn('192.168.0.1:NT_SERVER:00U',''.join(bodies))
        self.assertIn('INet~Services',''.join(bodies))
        self.assertIn('nbtscan -v -s : 192.168.1.0/24',''.join(bodies))
    def test_timeout_source_not_silently_corrected(self):
        self.assertIn('Wait timeout seconds for response. Default 1.',self.rendered)
    def test_known_escapes(self):
        self.assertEqual(decode(r'\.\.\.'),'...')
        self.assertEqual(decode(r'\\--__MSBROWSE__'),r'\--__MSBROWSE__')
    def test_native_snapshot(self):
        record=json.loads((self.root/'catalog/source-registry.json').read_text(encoding='utf-8'))['nbtscan']
        self.assertTrue(validate_package_source(record,self.root/'vault/99-Assets/upstream/nbtscan'))

class DnsManualTests(unittest.TestCase):
    def setUp(self):
        self.root=pathlib.Path(__file__).resolve().parents[1]
    def source(self,tool):
        return (self.root/'sources/upstream'/tool/(tool+'.1.source')).read_text(encoding='utf-8')
    def test_pod_preamble_is_data_not_executed(self):
        rendered,info=prepare_packaged_manual(self.source('dnsenum'),'dnsenum')
        adapter=info['source_layout_adapter']
        self.assertIn('.de Vb',adapter['original_preamble'])
        self.assertIn('tm Index:',adapter['original_preamble'])
        self.assertNotIn('.de Vb',rendered)
        self.assertEqual(hashlib.sha256(self.source('dnsenum').encode()).hexdigest(),DNSENUM_SHA)
    def test_pod_sections_options_and_bullets(self):
        rendered,info=prepare_packaged_manual(self.source('dnsenum'),'dnsenum')
        self.assertEqual(len(info['sections']),12)
        self.assertEqual(len(info['option_syntax']),18)
        self.assertIn('- 1) Get the host',rendered)
        self.assertIn('## COPYRIGHT',rendered)
        self.assertEqual(len(code_bodies(rendered)),1)
    def test_unreviewed_dns_sources_fail_closed(self):
        for tool in ['dnsenum','dnsrecon']:
            with self.subTest(tool=tool),self.assertRaises(ValueError):
                prepare_packaged_manual(self.source(tool)+'\n',tool)
    def test_missing_date_not_fabricated(self):
        _,info=prepare_packaged_manual(self.source('dnsrecon'),'dnsrecon')
        self.assertEqual(info['title'],['DNSRECON','1'])
    def test_dnsrecon_types_and_original_command(self):
        rendered,info=prepare_packaged_manual(self.source('dnsrecon'),'dnsrecon')
        self.assertEqual(len(info['sections']),5)
        self.assertEqual(len(info['option_syntax']),26)
        self.assertIn('--disable_check_bindversion',rendered)
        self.assertIn('- zonewalk:',rendered)
        self.assertEqual(code_bodies(rendered)[-1],'dnsrecon -t axfr -d zonetransfer.me\n')
        self.assertNotIn('attempts a zone transfer',''.join(code_bodies(rendered)))
    def test_flag_extraction_preserves_multichar_and_underscores(self):
        text='  -iL INPUT_LIST, --input-list INPUT_LIST  explanation\n  --disable_check_nxdomain\nDescription: query -www site:domain\n'
        self.assertEqual(extract_help_flags(text),['--disable_check_nxdomain','--input-list','-iL'])
    def test_distinct_package_license_choices(self):
        registry=json.loads((self.root/'catalog/source-registry.json').read_text(encoding='utf-8'))
        for tool,expected in [('dnsenum','GPL-2.0-or-later'),('dnsrecon','GPL-2.0-only')]:
            self.assertEqual(registry[tool]['license_spdx'],expected)
            self.assertTrue(validate_package_source(registry[tool],self.root/'vault/99-Assets/upstream'/tool))

class NetdiscoverFpingTests(unittest.TestCase):
    def setUp(self):
        self.root=pathlib.Path(__file__).resolve().parents[1]
        self.registry=json.loads((self.root/'catalog/source-registry.json').read_text(encoding='utf-8'))
    def source(self,name):
        package='fping' if name.startswith('fping') else 'netdiscover'
        return (self.root/'sources/upstream'/package/(name+'.source')).read_text(encoding='utf-8')
    def test_netdiscover_keyboard_reference_tables(self):
        rendered,info=prepare_packaged_manual(self.source('netdiscover.8'),'netdiscover')
        self.assertEqual(len(info['sections']),8)
        self.assertEqual(len(info['option_syntax']),16)
        self.assertEqual(len(info['reference_tables']),2)
        self.assertEqual([r[0] for r in info['reference_tables'][0]['rows']],list('hjk.,q'))
        self.assertEqual([r[0] for r in info['reference_tables'][1]['rows']],list('aru'))
        self.assertEqual(len(code_bodies(rendered)),9)
    def test_inconsistent_fast_defaults_preserved(self):
        rendered,_=prepare_packaged_manual(self.source('netdiscover.8'),'netdiscover')
        self.assertIn('.1, .100 and .254',rendered)
        self.assertIn('(1,100,154)',rendered)
    def test_fping_full_structure_and_exact_example(self):
        rendered,info=prepare_packaged_manual(self.source('fping.8'),'fping')
        self.assertEqual(len(info['sections']),9)
        self.assertEqual(len(info['option_syntax']),36)
        self.assertEqual(len(code_bodies(rendered)),6)
        self.assertIn(' $ fping --quiet --interval=1 --vcount=20 --period=50 127.0.0.1 127.0.0.2\n',''.join(code_bodies(rendered)))
    def test_compatibility_page_is_separate_not_include(self):
        rendered,info=prepare_packaged_manual(self.source('fping6.8'),'fping')
        self.assertEqual(info['title'][0],'FPING6')
        self.assertEqual(len(info['sections']),5)
        self.assertEqual(info['option_syntax'],[])
        self.assertIn('backwards-compatibility symbolic link',rendered)
    def test_unknown_fping_source_rejected(self):
        with self.assertRaises(ValueError):prepare_fping_layout(self.source('fping.8')+'\n')
    def test_pod_preambles_retained_without_execution(self):
        for name,digest in [('fping.8',FPING_SHA),('fping6.8',FPING6_SHA)]:
            source=self.source(name)
            self.assertEqual(hashlib.sha256(source.encode()).hexdigest(),digest)
            _,_,info=prepare_fping_layout(source)
            self.assertIn('.de Vb',info['original_preamble'])
    def test_pod_escape_glyphs(self):
        self.assertEqual(decode(r'\s-1ICMP\s0'),'ICMP')
        self.assertEqual(decode(r'\*(L"quoted\*(R"'),'"quoted"')
        self.assertEqual(decode(r'^\e'),'^'+chr(92))
    def test_distinct_licenses_and_two_document_snapshot(self):
        self.assertEqual(self.registry['netdiscover']['license_spdx'],'GPL-3.0-or-later')
        record=self.registry['fping']
        self.assertEqual(record['license_spdx'],'LicenseRef-Fping-Stanford-Variant')
        self.assertEqual(len(record['documents']),2)
        self.assertTrue(all(d.get('editorial_segment_file') for d in record['documents']))
        self.assertTrue(validate_package_source(record,self.root/'vault/99-Assets/upstream/fping'))
    def test_required_acknowledgement_cannot_be_removed(self):
        record=copy.deepcopy(self.registry['fping']);record.pop('required_acknowledgement')
        with self.assertRaises(AssertionError):validate_package_source(record,self.root/'vault/99-Assets/upstream/fping')
if __name__=='__main__':
    unittest.main()
