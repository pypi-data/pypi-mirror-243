import sys

sys.path.append("../src")
from langtorch import TextTensor, TextModule
from langtorch import Session
import unittest
import numpy as np
import torch

#
# class TestMul(unittest.TestCase):
#     def test_mul1(self):
#         tensor1 = TextTensor("1")
#         tensor1.requires_grad = True
#         tensor2 = TextTensor("2")
#         tensor2.requires_grad = True
#         tensor3 = tensor2*tensor1
#         tensor3.backward()
#         self.assertTrue((tensor2.grad == tensor1) and (tensor1.grad == tensor2))
#
#
# if __name__ == "__main__":
#     unittest.main()


from pathlib import Path
from typing import Optional
from langtorch import TextModule, TextTensor, Session
from langtorch.tt import Activation
from langtorch import Text, ctx
from langtorch.api.call import chat, auth
import torch
import numpy as np
from langtorch.texts import Markdown

import logging

# You can change this to logging.INFO to enable printing logs about api calls
logging.basicConfig(level=logging.INFO)

auth("D:/Techne/jutro_keys.json")
class MarkdownTensor(TextTensor):
    text_class = Markdown #replace parser

    def __new__(cls, *args, parse = True, **kwargs):
        if len(args) == 1 and isinstance(args[0], str) and parse:
            # If a single texts entry is given, split it using the items method of the Markdown parser.
            args = [Text((k,v)) for k,v in cls.text_class(args[0]).items()]

        # Creating an instance as per the base class
        instance = super().__new__(cls, args, parse = True, **kwargs)

        # Reshape if the tensors shape's length is less than or equal to 2
        if len(instance.shape) <= 2 and (len(instance.shape)==0 or instance.shape[-1] != 1):
            instance = instance.view(-1, 1)

        return instance


from langtorch.methods.embeddings import apply_rotary_embeddings

md = MarkdownTensor.from_file(Path("../examples/assets/test.md"))
# md = md.headers_to_keys()
# print((md)[:2].embed())
# emb = apply_rotary_embeddings(md.embedding)
import torch
from torch.autograd.function import Function


class SplitTextTensor(Function):
    @staticmethod
    def forward(ctx, input, on, dim=0):
        if not isinstance(input, TextTensor):
            raise TypeError("Input must be a TextTensor")

        # Flatten the input content to apply the split operation
        original_shape = input.shape

        # Perform the split operation
        all_splits = [text.split(on) for text in input.flat]
        max_len = max(len(splits) for splits in all_splits)

        # Normalize split lengths and create a new dimension for the splits
        padded_splits = [splits + [''] * (max_len - len(splits)) for splits in all_splits]
        split_content = TextTensor(padded_splits)

        # Calculate the new shape after split
        new_shape = list(original_shape)
        new_shape.insert(dim, max_len)
        split_content = split_content.reshape(new_shape)

        # Save the tensors for backward pass
        ctx.save_for_backward(input, torch.tensor(original_shape), torch.tensor(dim))

        return split_content

    @staticmethod
    def backward(ctx, grad_output):
        input, original_shape, dim = ctx.saved_tensors
        dim = dim.item()

        # Concatenate the split strings to reverse the split operation
        recombined_texts = [''.join(text) for text in grad_output.transpose(dim, -1).reshape(-1, original_shape[dim])]

        # Restore the original shape
        grad_input = TextTensor(recombined_texts).reshape(original_shape)

        return grad_input, None, None


# Example usage
# input_text = TextTensor(["This is a sentence.", "And another one!"])
# split_texts = SplitTextTensor.apply(input_text, ' ', 1)
# print(split_texts)




######################
# Semantic Algebra
######################
import langtorch.functional as LTF

print(LTF.mean(md, model="gpt3.5-turbo"))