#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Format-conversion fixtures, including byte-preservation and unsupported input."""
import unittest
from plain_manual import parse_manual,prepare_manual,protect_prose

BT=chr(96)

class PlainManualTests(unittest.TestCase):
    def test_every_source_line_is_accounted(self):
        source='NAME\r\n axel - example\r\n\r\nSYNOPSIS\r\n axel [OPTIONS] url\r\n'
        units=parse_manual(source)
        self.assertEqual(''.join(x['raw'] for x in units),source)
        self.assertEqual(prepare_manual(source,'axel')[1]['literal_blocks'][0]['body'],' axel [OPTIONS] url\r\n')

    def test_numeric_flags_and_single_space_description(self):
        source='OPTIONS\n --ipv6, -6  Use IPv6.\n\n --no-clobber, -c Skip existing files.\n'
        _,record=prepare_manual(source,'axel')
        self.assertEqual(record['option_syntax'],['--ipv6, -6','--no-clobber, -c'])

    def test_adjacent_options_are_not_merged(self):
        source='OPTIONS\n --progress, -p  Percentages.\n --header=x, -H x  Header description.\n'
        _,record=prepare_manual(source,'axel')
        self.assertEqual(len(record['option_syntax']),2)

    def test_unknown_section_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'Unsupported manual section'):
            parse_manual('UNKNOWN SECTION\n data\n')

    def test_unknown_option_grammar_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'Unrecognized option syntax'):
            parse_manual('OPTIONS\n --bad@syntax description\n')

    def test_prose_wrapping_does_not_drop_words(self):
        source='DESCRIPTION\n First part\n second part.\n'
        units=parse_manual(source)
        self.assertEqual(units[1]['text'],'First part second part.')

    def test_url_is_not_corrupted_by_path_protection(self):
        url='https://github.com/axel-download-accelerator/axel'
        self.assertEqual(protect_prose('<'+url+'>'),'<'+url+'>')
        self.assertIn(BT+'/etc/axelrc'+BT,protect_prose('Read /etc/axelrc now.'))

    def test_prompt_and_trailing_spaces_remain_exact(self):
        body='    $ axel https://example.com/file  \r\n'
        _,record=prepare_manual('EXAMPLES\r\n'+body,'axel')
        self.assertEqual(record['literal_blocks'][0]['body'],body)

    def test_io_abbreviation_is_not_misread_as_an_absolute_path(self):
        self.assertEqual(protect_prose('Set I/O timeout.'),'Set I/O timeout.')

if __name__=='__main__':
    unittest.main()
