import logging
import sys


sys.path.append("../src")
from langtorch import Text, TextTensor, TextModule
from langtorch import Session
import unittest
import numpy as np
import torch
import json
from typing import Any, List, Tuple, Union
import pypandoc
#
# class TestMarkupLanguages(unittest.TestCase):
#
#     def setUp(self):
#         # This setup could include common initializations for all tests
#         pass
#
#     def test_markdown(self):
#         input_text = "# My Markdown Heading\n\nSome paragraph texts.\n\n- numbered list item 1\n- numbered list item 2\n- numbered list item 3"
#         expected_output = input_text
#         output = pypandoc.convert_text(input_text, 'json', format='md')
#         text_obj = Text.from_pandoc_json(output)
#         assert output is None, str(output)+str(text_obj.items())
#         self.assertEqual(text_obj.keys(), ['header_h1', 'p'])
#
#     def test_html(self):
#         input_text = "<h1>My HTML Heading</h1><p>Some paragraph texts.</p>"
#         expected_output = input_text
#         output = pypandoc.convert_text(input_text, 'json', format='html')
#         text_obj = Text.from_pandoc_json(output)
#         assert output is None, str(output)+str(text_obj.items())
#         self.assertEqual(text_obj.keys(), ['header_h1', 'p'])
#         self.assertEqual(str(text_obj), expected_output)
#
#     # Add more tests for each markup language...
#
#     def test_latex(self):
#         input_text = "\\section{My LaTeX Heading}\n\nSome paragraph texts."
#         expected_output = input_text
#         output = pypandoc.convert_text(input_text, 'json', format='tex')
#         text_obj = Text.from_pandoc_json(output)
#         self.assertEqual(str(text_obj), expected_output)

import unittest
from langtorch.grammars.pandoc import convert_to_pandoc_ast  # Replace with your actual import

class TestPandocJsonParsing(unittest.TestCase):

    def test_markdown_parsing(self):
        md_input = "# Header\n\nParagraph with **bold** text."
        ast_json = convert_to_pandoc_ast(md_input, "markdown")
        text_obj = Text.from_pandoc_json(ast_json)
        expected_items = [('header_h1', 'Header'), ('p', 'Paragraph with **bold** text.')]
        self.assertEqual(text_obj.items(), expected_items)

    def test_html_parsing(self):
        html_input = "<h1>Header</h1><p>Paragraph with <strong>bold</strong> text.</p>"
        ast_json = convert_to_pandoc_ast(html_input, "html")
        text_obj = Text.from_pandoc_json(ast_json)
        # Update the expected items to reflect the actual behavior
        expected_items = [('header_h1', 'Header'), ('p', 'Paragraph with <strong>bold</strong> text.')]
        self.assertEqual(text_obj.items(), expected_items)

    def test_latex_parsing(self):
        latex_input = "\\section{Header}\n\nParagraph with \\textbf{bold} text."
        ast_json = convert_to_pandoc_ast(latex_input, "latex")
        text_obj = Text.from_pandoc_json(ast_json)
        expected_items = [('header_h1', 'Header'), ('p', 'Paragraph with bold text.')]
        self.assertEqual(text_obj.items(), expected_items)

    # Test for reStructuredText
    def test_rst_parsing(self):
        rst_input = """
.. _my-reference-label:

Section Header
==============

Some introductory text.

.. contents::
   :local:

.. section-numbering::

Subsection Header
-----------------

Subsection text.
"""
        ast_json = convert_to_pandoc_ast(rst_input, "rst")
        text_obj = Text.from_pandoc_json(ast_json)
        expected_items = [
            ('header_h1', 'Section Header'),  # Level 1 header
            ('p', 'Some introductory text.'),  # Paragraph
            # Assuming the 'contents' and 'section-numbering' directives are not parsed as visible text
            ('header_h2', 'Subsection Header'),  # Level 2 header
            ('p', 'Subsection text.')  # Paragraph
        ]
        self.assertEqual(text_obj.items(), expected_items)

    # Test for MediaWiki Markup
    def test_mediawiki_parsing(self):
        mediawiki_input = """
== Section Header ==

Introductory text.

=== Subsection Header ===

Subsection text.
"""
        ast_json = convert_to_pandoc_ast(mediawiki_input, "mediawiki")
        text_obj = Text.from_pandoc_json(ast_json)
        expected_items = [
            ('header_h2', 'Section Header'),  # Level 2 header
            ('p', 'Introductory text.'),  # Paragraph
            ('header_h3', 'Subsection Header'),  # Level 3 header
            ('p', 'Subsection text.')  # Paragraph
        ]

        self.assertEqual(text_obj.items(), expected_items)

    # Test for Textile Markup
    def test_textile_parsing(self):
        textile_input = """
h1. Header

Paragraph with "link":http://example.com.
"""
        ast_json = convert_to_pandoc_ast(textile_input, "textile")
        text_obj = Text.from_pandoc_json(ast_json)
        expected_items = [
            ('header_h1', 'Header'),  # Level 1 header
            ('p', 'Paragraph with link.')  # Paragraph with a link (assuming 'link' is treated as plain text)
        ]

        self.assertEqual(text_obj.items(), expected_items)

    # Add more tests for other markup languages as needed

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
