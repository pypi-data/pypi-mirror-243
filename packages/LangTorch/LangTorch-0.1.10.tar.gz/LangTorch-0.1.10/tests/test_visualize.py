from graphviz import Digraph
from torch.autograd import Variable
import torch

import logging
import sys


sys.path.append("../src")
import os
os.environ["PATH"] += os.pathsep +(r"C:\Program Files\Graphviz\bin")
from langtorch import TextTensor, TextModule
from langtorch import Session
import langtorch
import unittest
import numpy as np
import torch
from langtorch.methods import CoT
# import nnviz


class CustomModule(TextModule):
    def __init__(self):
        super(CustomModule, self).__init__()
        # parent init sets the .content attribute
        self.content2 = TextModule(TextTensor("2"))
        self.content3 = TextModule(TextTensor("3"))
        self.content3 = TextModule(TextTensor("3"))
        self.content4 = CoT
        self.api_call = langtorch.tt.activation.OpenAI()

    def forward(self, x):
        return self.content4(self.content3(self.content2(self.content * x)))



torch.Tensor.__torch_function__
x = TextTensor(torch.randn(1, 3))
batch_size = 2
# device='meta' -> no memory is consumed for visualization


