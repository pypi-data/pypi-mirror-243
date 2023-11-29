import re

import logging
import sys


sys.path.append("../src")
from langtorch import TextTensor, TextModule
from langtorch import Session
import unittest
import numpy as np
import torch


class TestInit(unittest.TestCase):
    # def test_content_and_metadata(self):
    #     tensors = TextTensor("Testing embeddings").embed()
    #     self.assertTrue(isinstance(tensors.embedding, torch.Tensor))
    #     # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.


    def join_and_sum(self):
        tensor = TextTensor([str(m) for m in range(16)]).reshape(4,4)
        # print(tensors.join_on("\n---\n", dim =0))
        # print(TextTensor(["1\n2\n3"]*3))
        # self.assertTrue(isinstance(tensors.embedding, torch.Tensor))
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.

    def test_inv(self):
        pass

from langtorch import Text

# Example usage
texts = [
    "<html><body>Hello, world!</body></html>",
    "# My Markdown Heading\n\nSome paragraph texts.",
    "\\documentclass{article}",
    "{value{:key}}",
    "Some plain texts.",
    "this {defo} isn't {python} code",
    "this {:defo} isn't {:python} code",
    "Bad exampled: {a:b:c}",
]

for content in texts:
    text_instance = content
    print(f"Text content: {content}\nGuessed language: {Text.guess_language(text_instance)}\n")
