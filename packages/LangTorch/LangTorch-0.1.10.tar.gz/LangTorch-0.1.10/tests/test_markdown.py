import sys
import re

sys.path.append("../src")
from langtorch import TextModule, TextTensor
from langtorch.tt import ActivationGPT
from langtorch import Text
from langtorch import Markdown
from langtorch.api.call import chat, auth
import torch
import numpy as np

import logging


# You can change this to logging.INFO to disable printing logs about api cal
logging.basicConfig(level=logging.CRITICAL)
from pyparsing import *

auth("D:/Techne/jutro_keys.json")

print(Markdown("""file::../examples/assets/test.md"""))

#OUTPUTS: ('h1', []) instead of ('h1', 'Wow')