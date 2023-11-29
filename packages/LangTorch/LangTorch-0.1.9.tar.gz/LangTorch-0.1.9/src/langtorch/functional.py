"""Semantic Algebra Functional interface"""
from typing import List, Optional, Union
from .decorators import set_defaults_from_ctx
from .session import ctx
import langtorch

from .session import Session

TextTensor = langtorch.TextTensor
Text = langtorch.Text

@set_defaults_from_ctx
def mean(input: TextTensor,
         method="Look at the following texts entries. Construct one 'mean' texts that averages their content into one semantically-rich texts of a similar length and style to individual entries:\n\n",
         dim: Optional[Union[int, List[int]]] = None, keepdim: bool = False, dtype: Optional = Text,
         model='default') -> TextTensor:
    input = input.join("\n---\n", dim=dim)
    if keepdim:
        input = input.unsqueeze(dim)
    input = method * input
    if model == 'default':
        output = langtorch.tt.Activation('gpt3.5-turbo')(input)
    else:
        output = langtorch.tt.Activation(model=model)(input)
    return output
