import sys

sys.path.append("../src")
from langtorch import TextTensor, TextModule
from langtorch import Session
import langtorch.tt as tt
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


import torch
import torch.nn as nn
import numpy as np
from typing import Tuple


def unfold(array, dimension, size, step):
    # This function will unfold along a specified dimension with a given size and step (stride)

    # Compute the shape of the resulting "unfolded" array
    new_shape = list(array.shape)
    num_blocks = (new_shape[dimension] - size) // step + 1
    new_shape[dimension] = num_blocks
    new_shape.insert(dimension + 1, size)

    # Initialize the output array with None objects, update the shape accordingly
    unfolded_array = np.full(new_shape, None, dtype=object)

    # Fill the unfolded array with windows of the original array
    for i in range(num_blocks):
        start_idx = i * step
        end_idx = start_idx + size
        unfolded_array[..., i, :] = array.take(indices=range(start_idx, end_idx), axis=dimension)

    return unfolded_array


class ManualConvolution(nn.Module):
    def __init__(self,
                 content: TextTensor,
                 in_channels: int,
                 out_channels: int,
                 kernel_size: Tuple[int, ...],
                 stride: Tuple[int, ...],
                 padding: Tuple[int, ...],
                 dilation: Tuple[int, ...],
                 transposed: bool,
                 output_padding: Tuple[int, ...],
                 groups: int,
                 bias: bool,
                 padding_mode: str):
        super(ManualConvolution, self).__init__()
        # Store all parameters, even though not all are used
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.transposed = transposed
        self.output_padding = output_padding
        self.groups = groups
        self.bias = bias
        self.padding_mode = padding_mode

    def forward(self, x):

        # Ensure that x is a float tensors for unfold to work properly
        # Check if we need to apply padding
        if self.padding != (0,) * len(self.padding):
            x = tt.functional.Pad.apply(x, self.padding, self.padding_mode, self.value)

        x = x.content
        # Use unfold to create the windows
        # Note: unfold only accepts int, convert stride and kernel_size to int if they are tuples
        windows = unfold(x, dimension=2, size=self.kernel_size[0], step=self.stride[0])

        for i in range(1, len(self.stride)):
            windows = unfold(windows, dimension=i + 2, size=self.kernel_size[i], step=self.stride[i])
        print((windows).shape)


        return (windows)


# Example usage (assuming you're working with a 2D input):
conv_module = ManualConvolution(
    content=TextTensor([str(m) for m in range(9)]).reshape(3,3),
    in_channels=1,
    out_channels=1,
    kernel_size=(3, 3),
    stride=(3, 3),
    padding=(0, 0),
    dilation=(1, 1),
    transposed=False,
    output_padding=(0, 0),
    groups=1,
    bias=False,
    padding_mode='zeros'
)

# Create a dummy input NumPy array (e.g., a 2D image with shape 1x10x10)
input_array = TextTensor(np.random.rand(1, 10, 10))

# Call the forward method to get the windows
windows = conv_module.forward(input_array)

print((TextTensor([[1,2,3],[4,5,6],[7,8,9]]).reshape(3,3) @ TextTensor(windows).reshape(10,3,3)))