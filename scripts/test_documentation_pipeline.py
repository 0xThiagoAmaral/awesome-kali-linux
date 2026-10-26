#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Pure fixture tests; downloaded tool code is never executed."""
import unittest
from import_translate_docs import markdown_headings,preserve_heading_anchors,code_bodies,mirror_images
from enrich_local_assets import resolve_reference
from build_cheatsheets import fenced_blocks

BT=chr(96)
F=BT*3

class DocumentationPipelineTests(unittest.TestCase):
    def test_heading_slug_preserves_code_metavariable_text(self):
        from import_translate_docs import slug
        self.assertEqual(slug(BT+'<s>'+BT),'s')
        self.assertEqual(slug('<span>Title</span>'),'title')

    def test_shell_comments_are_not_document_headings(self):
        source=F+'bash\n# apt update\nprintf ok\n'+F+'\n'
        self.assertEqual(markdown_headings(source),[])

    def test_visible_heading_and_exact_crlf_block(self):
        source='# Real title\n\n'+F+'bash\r\n# keep comment\r\nprintf ok  \r\n'+F+'\r\n'
        self.assertEqual(markdown_headings(source),[(1,'Real title')])
        self.assertEqual(code_bodies(source),['# keep comment\r\nprintf ok  \r\n'])
        self.assertEqual(fenced_blocks(source)[0]['body'],code_bodies(source)[0])

    def test_original_heading_alias_survives_translation(self):
        source='# Tool\n\n## Running the program\n'
        translated='# Tool\n\n## Executar o programa\n'
        output,changes=preserve_heading_anchors(source,translated)
        self.assertIn('<a id="running-the-program"></a>',output)
        self.assertEqual(len(changes),1)

    def test_duplicate_heading_aliases_are_unique(self):
        source='## Usage\n\n## Usage\n'
        translated='## Uso\n\n## Uso\n'
        output,_=preserve_heading_anchors(source,translated)
        self.assertIn('id="usage"',output)
        self.assertIn('id="usage-1"',output)

    def test_relative_image_resolution_is_doc_scoped(self):
        self.assertEqual(resolve_reference('../images/logo.png','docs/guide.md','https://github.com/a/b'),'images/logo.png')
        self.assertIsNone(resolve_reference('../../escape.png','guide.md','https://github.com/a/b'))

    def test_external_basename_cannot_impersonate_repository_asset(self):
        self.assertIsNone(resolve_reference('https://example.com/logo.png','README.md','https://github.com/a/b'))
        self.assertEqual(resolve_reference('https://raw.githubusercontent.com/a/b/main/logo.png','README.md','https://github.com/a/b'),'logo.png')

    def test_code_headers_do_not_receive_aliases(self):
        source=F+'bash\n# Source comment\n'+F+'\n## Usage\n'
        translated=F+'bash\n# Source comment\n'+F+'\n## Uso\n'
        output,_=preserve_heading_anchors(source,translated)
        self.assertEqual(code_bodies(source),code_bodies(output))
        self.assertEqual(output.count('<a id='),1)

    def test_legacy_headings_are_counted_without_touching_code(self):
        from import_translate_docs import normalize_legacy_headings
        source='###Dependencies###\n'+F+'bash\n###LeaveCodeAlone###\n'+F+'\n'
        normalized=normalize_legacy_headings(source)
        self.assertEqual(markdown_headings(source),[(3,'Dependencies')])
        self.assertTrue(normalized.startswith('### Dependencies\n'))
        self.assertEqual(code_bodies(normalized),code_bodies(source))

    def test_escaped_table_pipe_keeps_inline_literal(self):
        from import_translate_docs import translate_body
        class IdentityTranslator:
            def text(self,value):
                return value
        literal=BT+'{{arg'+chr(92)+'|default}}'+BT
        source='| '+literal+' | description |\n'
        self.assertIn(literal,translate_body(source,IdentityTranslator()))

    def test_linked_image_stays_local_during_link_rewrite(self):
        import pathlib
        from import_translate_docs import resolve_relative_links
        record={'tool':'fixture','repository':'https://github.com/a/b','commit':'abc','documents':[]}
        note=pathlib.Path('/fixture/vault/02-Tools/tool/tool.md')
        output,_=resolve_relative_links('[![Preview](../../99-Assets/local.gif)](https://example.com)',record,'README.md',note,pathlib.Path('/fixture/assets'),{})
        self.assertIn('![Preview](../../99-Assets/local.gif)',output)
        self.assertNotIn('/blob/abc/../../99-Assets',output)

    def test_contributor_anchor_points_to_actual_profile_cell(self):
        from import_translate_docs import preserve_contributor_anchors
        source='<table><td><a href="https://github.com/test-user">Name</a><a href="#ideas-test-user">Ideas</a></td></table>'
        output,changes=preserve_contributor_anchors(source)
        self.assertIn('<a id="ideas-test-user"></a><a href="https://github.com/test-user">',output)
        self.assertEqual(len(changes),1)

if __name__=='__main__':
    unittest.main()
