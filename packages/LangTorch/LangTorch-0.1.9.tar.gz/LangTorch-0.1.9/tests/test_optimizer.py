import logging
import sys


sys.path.append("../src")
from langtorch import TextTensor, TextModule
from langtorch import Session
import unittest
import numpy as np
import torch


class TestOpt(unittest.TestCase):
    # def test_content_and_metadata(self):
    #     tensors = TextTensor("Testing embeddings").embed()
    #     self.assertTrue(isinstance(tensors.embedding, torch.Tensor))
    #     # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.


    def aggregate_grad(self):

        tensor1 = TextTensor("1")
        tensor1.requires_grad = True
        tensor2 = TextTensor("2")
        tensor2.requires_grad = True
        tensor3 = tensor2*tensor1
        tensor4 = (tensor3+tensor2)
        tensor4.backward()
        logging.info(tensor1.grad)
        self.assertTrue((tensor2.grad == tensor1) and (tensor1.grad == tensor2) and tensor3.grad is None)

        tensor = TextTensor([str(m) for m in range(16)]).reshape(4,4)
        # print(tensors.join_on("\n---\n", dim =0))
        # print(TextTensor(["1\n2\n3"]*3))
        # self.assertTrue(isinstance(tensors.embedding, torch.Tensor))
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.



# if __name__ == "__main__":
#     unittest.main()
texts = np.array([["Line1\nLine2\nLine3", "Another line1\nAnother line2\nAnother line3"],
                      ["Short1\nShort2", "Even shorter1\nEven shorter2\nEven shorter3"],
                      ["Single line", "Multiple\nLines\nHere"]])

tensor1 = TextTensor("1")
tensor1.requires_grad = True
tensor2 = TextTensor("2")
tensor2.requires_grad = True
tensor2.retain_grad = True
tensor3 = tensor2*tensor1
tensor4 = (tensor3+tensor2)
tensor4.backward()
logging.info(tensor1.grad)
print((tensor2.grad == tensor1) and (tensor1.grad == tensor2))

tensor = TextTensor([str(m) for m in range(16)]).reshape(4,4)


# print(tensors.join_on("\n---\n", dim =0))
# print(TextTensor(["1\n2\n3"]*3))
# Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.

