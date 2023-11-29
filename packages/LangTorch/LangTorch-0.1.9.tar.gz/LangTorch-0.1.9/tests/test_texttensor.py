import logging
import sys


sys.path.append("../src")
from langtorch import TextTensor, TextModule
from langtorch import Session
import unittest
import numpy as np
import torch
import unittest
from langtorch.utils import positive_indices
# Test cases for the positive_indices function
import unittest

# Assuming the positive_indices function is as corrected in the previous response.
class TestInit(unittest.TestCase):
    def test_content_and_metadata(self):
        tensor = TextTensor(["Testing embeddings"])
        tensor.embedding = torch.ones([1, 512])

        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.


    def join_and_sum(self):
        tensor = TextTensor([str(m) for m in range(16)]).reshape(4,4)
        # print(tensors.join_on("\n---\n", dim =0))
        # print(TextTensor(["1\n2\n3"]*3))
        # self.assertTrue(isinstance(tensors.embedding, torch.Tensor))
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.

class TestPositiveIndices(unittest.TestCase):

    def test_slice_all_positive(self):
        self.assertEqual(positive_indices((slice(1, 3),), (5,)), (slice(1, 3, None),))

    def test_slice_negative_start(self):
        self.assertEqual(positive_indices((slice(-4, 3),), (5,)), (slice(1, 3, None),))

    def test_slice_negative_stop(self):
        self.assertEqual(positive_indices((slice(1, -1),), (5,)), (slice(1, 4, None),))

    def test_slice_negative_start_and_stop(self):
        self.assertEqual(positive_indices((slice(-4, -1),), (5,)), (slice(1, 4, None),))

    def test_zero_dimensional_tensor(self):
        with self.assertRaises(IndexError):
            positive_indices((1,), ())

    # Additional test cases to verify correct handling of different scenarios
    def test_single_negative_index(self):
        self.assertEqual(positive_indices((-1,), (5,)), (4,))

    def test_mixed_indices(self):
        # The slice should go to the end of the dimension, hence stop is None
        self.assertEqual(positive_indices((slice(-3, None), -1), (5, 5)), (slice(2, None, None), 4))

    def test_newaxis_index(self):
        # When a new axis is specified, it should be included in the result tuple
        self.assertEqual(positive_indices((None, -1), (5,)), (None, 4))
    def test_ellipsis_index(self):
        self.assertEqual(positive_indices((Ellipsis, -1), (5, 5)), (Ellipsis, 4))


class TestInit(unittest.TestCase):
    def test_content_and_metadata(self):
        tensor = TextTensor("Testing embeddings").embed()
        self.assertTrue(isinstance(tensor.embedding, torch.Tensor))
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.


    def join_and_sum(self):
        tensor = TextTensor([str(m) for m in range(16)]).reshape(4,4,1)
        tensor = (tensor.join_with("\n---\n", dim =0))
        self.IsEqual(tensor.shape, (4,1))
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.

    def test_inv(self):


# Run the tests
if __name__ == '__main__':
    unittest.main()


#
# if __name__ == "__main__":
#     # unittest.main()
#     print(TextTensor(["111\n222\n3"]*3))
#     texts = np.array([["Line1\nLine2\nLine3", "Another line1\nAnother line2\nAnother line3"],
#                       ["Short1\nShort2", "Even shorter1\nEven shorter2\nEven shorter3"],
#                       ["Single line", "Multiple\nLines\nHere"]])
#     # texts = TextTensor([str(m) for m in range(16)]).reshape(4,2,2)
#     tensors = TextTensor(texts)
#     print(TextTensor.str_formatter(tensors))
#     TestInit().join_and_sum()