from copy import deepcopy
from itertools import zip_longest
from typing import Optional, Union, List, Callable, Iterable

import langtorch
import numpy as np
import torch
from pyparsing import ParseException
from torch.types import _TensorOrTensors

from .. import utils
from ..api.call import get_embedding
from ..autograd import make_grads
from ..texts import Text
from ..tt.functional import AddTextTensor, MulTextTensor, PermuteTextTensor, FormatTextTensor, JoinTextTensor, \
    ReshapeTextTensor, SplitTextTensor


# Metaclass to combine _TensorMeta and the instance check override for Parameter.
class _ParameterMeta(torch._C._TensorMeta):
    # Make `isinstance(t, Parameter)` return True for custom tensors instances that have the _is_param flag.
    def __instancecheck__(self, instance):
        return super().__instancecheck__(instance) or (
                isinstance(instance, torch.Tensor) and getattr(instance, '_is_param', False))


def chararray_to_TextArray(arr, text_class=Text, shape=None, **kwargs):
    if isinstance(arr, np.ndarray):
        try:
            if all([isinstance(a, text_class) for a in arr.flat]):
                return arr
        except:
            pass

    arr = np.array(arr, dtype=object)
    text_arr = [text_class(a, **kwargs) for a in arr.flat]
    text_arr = np.array(text_arr, dtype=object).reshape(arr.shape if shape is None else shape)
    return text_arr


class TextTensor(torch.Tensor, metaclass=_ParameterMeta):
    text_class = Text  # The class of a Tensor entry, replaced in subclasses. May in the future move this logic to the metaclass
    _embedding_module = None  # TextTensor to Tensor with an embedding model
    _tokenizer = None  # TextTensor to Tensor with a transformer tokenizer
    parse = 'auto'

    @classmethod
    def input_formatter(cls, content):
        # Default implementation, to be overridden by subclasses if needed
        return content

    @classmethod
    def linter(cls, tensor):
        # Default implementation, ensures correct class of Tensor content entries
        tensor.content = chararray_to_TextArray(tensor.content, cls.text_class)
        return tensor

    def __new__(cls, content="", embedding: Optional[Union[torch.Tensor, List[float], np.ndarray, bool]] = None,
                metadata=None, key=None, requires_grad: bool = True,
                is_gradient: bool = False, is_param: bool = True, parse=True, **kwargs):
        if metadata is None:
            metadata = dict()
        for attr in ["content", "embedding"]:
            if not attr in metadata:
                metadata[attr] = eval(attr)
        # TODO create from dict of tensors
        # Set content to be an object array with cls.text_class entries
        metadata["content"] = cls.to_array(metadata["content"], parse=parse)
        # Apply input formatter
        metadata["content"] = cls.input_formatter(metadata["content"])
        if embedding == True:
            metadata["embedding"] = get_embedding([str(m) for m in metadata["content"].flat])["embedding"].to_list()

        tensor = super().__new__(cls, torch.arange(metadata["content"].size, dtype=torch.float32).reshape(
            metadata["content"].shape), **kwargs)

        tensor.metadata = metadata
        tensor._is_param = is_param
        tensor._is_gradient = is_gradient
        tensor.requires_grad = requires_grad
        if key is not None:
            tensor.add_key_(key)
        assert tensor._content is not None

        # Apply linter
        tensor = cls.linter(tensor)
        return tensor

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __hash__(self):
        return id(self)

    @classmethod
    def to_array(cls, input, **kwargs):
        return input.content if isinstance(input, cls) \
            else np.array(input, dtype=object) if isinstance(input, Text) \
            else chararray_to_TextArray(input, cls.text_class, **kwargs)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = TextTensor.to_array(content)
        assert self._content is not None

    @property
    def embedding(self):  # TODO re-enable autoembedding or remove it
        # if self._embedding is None and hasattr(self, 'metadata') and self.metadata is not None:
        #     print("Warning: autoembedding ON")
        #
        #     self.embed()
        return self._embedding

    @embedding.setter
    def embedding(self, embedding: Union[torch.Tensor, List[float], np.ndarray, tuple]):
        if embedding is None:
            self._embedding = None
            return
        assert isinstance(embedding, torch.Tensor) or isinstance(embedding, np.ndarray) or isinstance(embedding,
                                                                                                      list) or isinstance(
            embedding, list), "Value of embedding should be a Tensor, array or list"

        self._embedding = embedding if isinstance(embedding, torch.Tensor) else torch.tensor(embedding)
        try:
            self._embedding = self._embedding.reshape(*self.content.shape, -1)
        except ValueError:
            raise ValueError("The shape of the embedding does not match the size of the TextTensor")
        self._metadata["embedding"] = self._embedding

    @property
    def tokens(self):
        if not hasattr(self, "_tokens"):
            if self.tokenizer is not None:
                self._tokens = self.tokenizer(self)
            else:
                raise AttributeError("Tokens unavailable as no tokenizer has been set")
        return self._tokens

    input_ids = tokens

    @tokens.setter
    def tokens(self, tokens):
        self._tokens = tokens

    @property
    def tokenizer(self):
        return self._tokenizer

    @tokenizer.setter
    def tokenizer(self, tokenizer):
        if isinstance(tokenizer, str):
            from transformers import AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self._tokenizer = tokenizer

    def tokenize(self, tokenizer=None, **kwargs):
        if tokenizer is not None:
            self.tokenizer = tokenizer
        assert self.tokenizer is not None
        kwargs_default = {"padding": True, "return_tensors": "pt", "truncation": True}
        for k, v in kwargs_default.items():
            if not k in kwargs:
                kwargs[k] = v
        self.tokens = self.tokenizer(self, **kwargs_default)

    functions_on_embeddings = [torch.mean]
    @classmethod
    def __torch_function__(cls, func: Callable, types: Iterable, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}

        # Handle functions that need custom behavior
        if func in [torch.cosine_similarity, torch.cat, torch.vstack,
                    torch.stack]+cls.functions_on_embeddings:  # list other relevant PyTorch functions
            return cls._handle_function(func, *args, **kwargs)
        # if func in []

        # Default behavior for unhandled functions
        return super().__torch_function__(func, types, args, kwargs)

    @classmethod
    def _handle_function(self, func: Callable, *args, **kwargs):
        # Implement custom behavior for each PyTorch function as needed
        def apply_to_texttensors(func, args, kwargs):
            args2, kwargs2 = [], {}
            for i, arg in enumerate(args):
                if isinstance(arg, TextTensor):
                    args2.append(func(arg))
                else:
                    args.append(arg)
            for k, arg in kwargs.items():
                if isinstance(arg, TextTensor):
                    kwargs2[k] = func(arg)
                else:
                    kwargs2[k] = arg

            return args2, kwargs2

        functions_on_embeddings = self.functions_on_embeddings
        if any([func is f for f in functions_on_embeddings+[torch.cosine_similarity]]):
            def embed(tensor) -> torch.Tensor:
                if tensor.embedding is None:
                    tensor.embed()
                assert isinstance(tensor.embedding, torch.Tensor)
                return tensor.embedding

            args, kwargs = apply_to_texttensors(embed, args, kwargs)

            if func is torch.cosine_similarity:
                kwargs["dim"] = -1
                return torch.cosine_similarity(*args, **kwargs)
            for f in functions_on_embeddings:
                if func is f:
                    return f(*args, **kwargs)
        # if func is torch.stack:

        # ... handle other functions as necessary

        # Fallback if the function is not recognized
        return NotImplemented

    @classmethod
    def from_file(cls, path, encoding="utf-8", **kwargs):
        with open(path, encoding=encoding) as f:
            content = f.read()
        return cls(content, **kwargs)

    @classmethod
    def from_df(cls, df: 'DataFrame', **kwargs) -> 'TextTensor':
        text_list = []
        if not "parse" in kwargs:
            kwargs["parse"] = False

        for row in df.values:
            # Create a Text object with (column_name, value) pairs
            text_content = [(col_name, str(value)) for col_name, value in zip(df.columns, row) if
                            value != np.nan and str(value) != ""]
            text_obj = Text(*text_content, **kwargs)
            text_list.append(text_obj)

        # Convert the list of Text objects to a TextTensor of shape (n, 1)
        text_tensor = cls(text_list, **kwargs).reshape(-1, 1)

        return text_tensor

    def set_key(self, keys=None, inplace=False) -> 'TextTensor':
        assert keys is not None
        if isinstance(keys, (TextTensor, np.ndarray)):
            try:
                reshaped_keys = keys.reshape(self.content.shape)
            except ValueError:
                raise ValueError("Keys must be of the same shape as the TextTensor")
        elif isinstance(keys, str):
            reshaped_keys = utils.str_like(self.content, keys)
        elif isinstance(keys, list):
            reshaped_keys = utils.str_like(self.content, keys[0])
            for k in keys[1:]:
                reshaped_keys += k
        if inplace:
            result = self
        else:
            result = self.copy()

        # Apply set_key to each entry
        for index, text_entry in np.ndenumerate(result.content):
            result.content[index] = text_entry.set_key(reshaped_keys[index].item())

        return result

    def set_key_(self, keys) -> 'TextTensor':
        return self.set_key(keys, inplace=True)

    def add_key(self, keys, inplace=False) -> 'TextTensor':
        reshaped_keys = utils.str_like(self.content, keys)
        if inplace:
            result = self
        else:
            result = self.copy()

        # Apply set_key to each entry
        for index, text_entry in np.ndenumerate(result.content):
            result.content[index] = text_entry.add_key(reshaped_keys[index].item())

        return result

    def add_key_(self, keys) -> 'TextTensor':
        return self.add_key(keys, inplace=True)

    @classmethod
    def str_formatter(cls, array, indent='  '):
        """Formats a TextTensor into a matrix representation with entries padded with spaces to be able to have multi-line entries aligned.
        It would be pretty challenging to replace this in a subclass so rather, replace the Text subclass method."""
        array = array.content if isinstance(array, TextTensor) else array

        def format_entry(entry, max_lines, max_width):
            # Split the entry into lines, pad them to match the max width, and ensure each entry has the same number of lines
            lines = entry.split('\n')
            padded_lines = [str(line).ljust(max_width) for line in lines]
            padded_lines += [' ' * max_width] * (max_lines - len(lines))  # Pad with empty lines if needed
            return padded_lines

        def format_2d(array_2d):
            # Calculate max width for each column
            max_width_per_col = [max(max([len(str(line)) for line in element.split('\n')]) for element in col) for col
                                 in
                                 zip(*array_2d)]

            # Create a list of lists for each formatted line
            formatted_rows = []
            for i, row in enumerate(array_2d):
                # Calculate the max number of lines for this row
                max_lines_in_row = max(element.count('\n') + 1 for element in row)

                # Format each entry in the row with max_lines corresponding to the current row
                formatted_entries = [format_entry(entry, max_lines_in_row, max_width)
                                     for entry, max_width in zip(row, max_width_per_col)]

                # Transpose to turn columns into rows and pad rows to have the same number of lines
                transposed_entries = list(zip_longest(*formatted_entries, fillvalue=' ' * max_width_per_col[0]))

                # Join the transposed lines into formatted strings

                def prefix_suffix_line(line, prefix, suffix):
                    if len(line) == 1:
                        return [prefix + str(line[0]) + suffix]
                    else:
                        return '  '.join(
                            [prefix + str(transposed_line[0])] + [str(m) for m in transposed_line[1:-1]] + [
                                str(transposed_line[-1]) + suffix])

                for j, transposed_line in enumerate(transposed_entries):
                    if j == 0:
                        if len(transposed_entries) == 1:
                            formatted_rows.extend(prefix_suffix_line(transposed_line, "[", "]"))
                        else:
                            formatted_rows.extend(prefix_suffix_line(transposed_line, "[", ""))
                    elif j == len(transposed_entries) - 1:
                        formatted_rows.extend(prefix_suffix_line(transposed_line, " ", "]"))
                    else:
                        formatted_rows.extend(prefix_suffix_line(transposed_line, " ", " "))
            return formatted_rows

        def format_1d(array_1d):
            max_lines = max(element.count('\n') + 1 for element in array_1d)
            max_width = max(max(len(line) for line in element.split('\n')) for element in array_1d)
            formatted_entries = [format_entry(entry, max_lines, max_width) for entry in array_1d]

            # Transpose to align multiline entries
            transposed_entries = list(zip_longest(*formatted_entries, fillvalue=' ' * max_width))
            formatted_rows = ['  '.join(line) for line in transposed_entries]
            return '[\n' + indent + ('\n' + indent).join(formatted_rows) + '\n' + indent[:-2] + ']'

        if array.ndim == 0:
            return str(array.item())
        if array.ndim == 1:
            return format_1d(array)
        elif array.ndim == 2:
            formatted_lines = format_2d(array)
            print(formatted_lines)
            return '[\n' + indent + ('\n' + indent).join(formatted_lines) + '\n' + indent[:-2] + ']'
        else:
            inner_arrays = [cls.str_formatter(sub_array, indent + '  ') for sub_array in array]
            inner_content = (',\n' + indent).join(inner_arrays)
            return '[\n' + indent + inner_content + '\n' + indent[:-2] + ']'

    def apply(self, func):
        """Applies a function: Text -> Text to each entry of self.content"""
        # Ensure the function is callable
        if not callable(func):
            raise ValueError("Provided function is not callable.")

        # Apply the function to each entry
        for index, text_entry in np.ndenumerate(self.content):
            self.content[index] = func(text_entry)

        return self

    def inv(self):
        # Apply inverse operation on each element of the char array
        self.content = np.vectorize(lambda x: x.inv())(self.content)

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        if not hasattr(self, "_metadata"): self._metadata = {}
        # set core attributes
        for attr in ["content", "embedding"]:
            if attr in metadata:
                setattr(self, attr, metadata.pop(attr))

        for attr in ["content", "embedding"]:
            metadata[attr] = getattr(self, "_" + attr)

        self._metadata = metadata

    def metadata_index(self, index):
        """Pick out entries of metadata with the provided index. Usually used to transfer metadata to a sub-tensors."""

        index = utils.positive_indices(index, self.content.shape)
        index = index[0] if len(index) == 1 else index

        if len(self.content.shape) == 0:  # and (index == slice(None, None, None))
            return self.metadata_apply(lambda v: v, lambda v: v, lambda v: v)

        else:
            return self.metadata_apply(lambda v: v[index], lambda v: v[index], lambda v: v)

    def metadata_apply(self, f_tensor=None, f_embedding=None, f_scalar=None, *args, **kwargs):
        """
        Apply a specified function to a copy of metadata elements of the TextTensor.

        Parameters:
        - f_tensor (function, optional): Function to be applied to tensors-shaped metadata attributes.
        - f_embedding (function, optional): Function to be applied to the 'embedding' attribute.
        - f_scalar (function, optional): Function to be applied to scalar metadata attributes.
        - *args: Variable length argument list to be passed to the functions.
        - **kwargs: Arbitrary keyword arguments to be passed to the functions.

        Returns:
        - dict: A dictionary with updated metadata attributes.
        """
        tensor_attributes, scalar_attributes = [], []
        for k, v in self._metadata.items():
            try:
                if tuple(v.shape) == tuple(self.shape):
                    tensor_attributes.append(k)
            except AttributeError:
                if k != "embedding":
                    scalar_attributes.append(k)

        metadata = self._metadata.copy()

        if f_tensor:
            for k in tensor_attributes:
                metadata[k] = f_tensor(metadata[k], *args, **kwargs)

        if f_embedding and metadata["embedding"]:
            metadata["embedding"] = f_embedding(metadata["embedding"], *args, **kwargs)

        if f_scalar:
            for k in scalar_attributes:
                metadata[k] = f_scalar(metadata[k], *args, **kwargs)

        return metadata

    def __repr__(self):
        return str(self.sum().content)

    def __str__(self):
        return self.str_formatter(self)

    def inspect(self):
        details = np.vectorize(lambda x: x.inspect())(self.content)
        return details

    def copy(self):
        new_dict = deepcopy(self.metadata)
        return self.__class__(metadata=new_dict, parse=False)

    def __eq__(self, other):
        return self.content == other.content if isinstance(other, TextTensor) else self.content == other

    def sum(self, dim=None):
        if len(self.shape) == 0:
            return self
        if dim is None:
            result = self
            connecting_char = [" "] + ["\n" * (i + 1) for i in range(len(self.content.shape) - 1)]
            for i, char in enumerate(connecting_char):
                result = result.join_with(char, dim=-1)
            assert len(result.shape) <= 1
        else:
            result = self.join_with("", dim=dim)
        return result

    def join_with(self, delimiter=" ", dim=None):
        return JoinTextTensor.apply(self, delimiter, dim)

    join = join_with  # Alias

    def format(self, **kwargs):
        """
        Return a formatted version of self, using substitutions from kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        return FormatTextTensor.apply(self, kwargs)

    def to_list(self):
        return [self.text_class(m, parse=False) for m in self.content.flat]

    def __pow__(self, power):
        if power == -1:
            self_copy = self.copy()
            self_copy.inv()
        else:
            raise ValueError("Only power of -1 is supported for inversion.")
        return self_copy

    def __add__(self, other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other, parse=False)  # TODO parsing rules
            except ParseException:
                other = TextTensor(other, parse=False)
        return AddTextTensor.apply(self, other)

    def __mul__(self, other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other, parse=False)  # TODO parsing rules
            except ParseException:
                other = TextTensor(other, parse=False)
        return MulTextTensor.apply(self, other)

    def __matmul__(self, other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other)  # To parse or not to parse?
            except ParseException:
                other = TextTensor(other, parse=False)
        result = self.__class__(self.content @ other.content, parse=False)
        return result

    def item(self):
        return next(self.content.flat)

    def items(self):
        """Get (key, value) pairs from all Text entries in tensors"""
        return np.array([{"items": tuple(t.items())} for t in self.content.flat], dtype=object).reshape(
            self.content.shape)

    def __getattr__(self, name):
        try:
            metadata = object.__getattribute__(self, "_metadata")
        except AttributeError:
            raise AttributeError(
                "'TextTensor' object has no attribute 'metadata'. TextTensor was probably initialised outside of langtorch, e.g. when passing TextTensor to a torch function that expects torch.Tensor")
        if name in ["_content", "content"] or name in metadata:
            if name in metadata:
                return metadata[name]
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                return None
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            # Query np.ndarray attrs
            try:
                assert self.content is not None
                return getattr(self._content, name)
            except AttributeError:
                # Query Text attrs

                try:
                    attr = np.array(np.vectorize(lambda obj: getattr(obj, name))(self._content), dtype=object)
                    if callable(attr.flat[0]):
                        return lambda: np.vectorize(lambda x: x())(attr)
                    else:
                        return attr
                except:
                    raise AttributeError(f"Object {self}, Neither TextTensor nor Text has attribute '{name}'")

    def __getitem__(self, index):
        return self.__class__(metadata=self.metadata_index(index), parse=False)

    def __iter__(self):
        return iter(self.content.flat)

    def __contains__(self, item):
        return item in self.content

    @property
    def TT(self):
        from .tt import TextModule
        return TextModule(self.mT)

    @property
    def T(self):  # diff!
        return self.__class__(self.content.T, super().mT, parse=False)

    @property
    def mT(self):  # diff!
        return self.__class__(self.content.T, super().mT, parse=False)

    def embed(self, verbose=False):
        if self.embedding is None:
            self.embedding = get_embedding(self, verbose=verbose)
        # TODO ELSE EMPTY ENTRIES
        return self.embedding

    def apply(self, func):
        """Applies a function to each entry of self.content."""
        # Ensure the function is callable
        if not callable(func):
            raise ValueError("Provided function is not callable.")

        # Apply the function to each entry
        for index, text_entry in np.ndenumerate(self.content):
            self.content[index] = func(text_entry)

        return self

    def reshape(self, *shape):
        return ReshapeTextTensor.apply(self, shape)[0]

    def usqueeze(tensor, dim=0):
        return tensor.reshape(tensor.shape[:dim] + [1] + tensor.shape[dim:])

    def squeeze(tensor, dim=None):
        if dim is None:
            # Remove all dimensions of size 1
            return tensor.view([dim for dim in tensor.shape if dim != 1])
        else:
            if dim < 0:
                # Convert negative dimension to positive
                dim = len(tensor.shape) + dim
            # Remove only the specified dimension if it is of size 1
            if tensor.shape[dim] == 1:
                return tensor.view(tensor.shape[:dim] + tensor.shape[dim + 1:])
            else:
                return tensor

    def expand(tensor, *sizes):
        # Check if the number of dimensions of the tensors is less than the length of the target sizes
        if tensor.dim() < len(sizes):
            # Add singleton dimensions to the front of the tensors
            for _ in range(len(sizes) - tensor.dim()):
                tensor = tensor.unsqueeze(0)

        # Prepare a list to hold the expanded sizes
        expanded_sizes = []

        # Loop over the target sizes from last to first
        for tensor_size, target_size in zip(reversed(tensor.shape), reversed(sizes)):
            if tensor_size == 1:
                # If the size of the tensors in this dimension is 1, it can be expanded
                expanded_sizes.append(target_size)
            elif tensor_size != target_size:
                # If the size of the tensors in this dimension is not equal to the target size,
                # and is not 1, it cannot be expanded
                raise ValueError(f"size mismatch for dimension {len(expanded_sizes)}, {tensor_size} != {target_size}")
            else:
                # If the size of the tensors in this dimension is equal to the target size,
                # it doesn't need to be expanded
                expanded_sizes.append(tensor_size)

        # Reverse the list of expanded sizes to match the original order of dimensions
        expanded_sizes = list(reversed(expanded_sizes))

        # Use the repeat method to create a new tensors that repeats the original tensors along each dimension
        return tensor.repeat(*expanded_sizes)

    def swapaxes(self, axis1: int, axis2: int):
        # Create a list of axes in order
        axes = list(range(len(self.shape)))
        # Swap the specified axes
        axes[axis1], axes[axis2] = axes[axis2], axes[axis1]
        # Return the tensors with axes swapped
        return self.permute(axes)

    def permute(self, axes):
        return PermuteTextTensor.apply(self, axes)

    def view(self, *shape):
        return self.__class__(
            metadata=self.metadata_apply(lambda v: v.reshape(*shape), lambda v: v.reshape(*shape, v.shape[-1])),
            parse=False)

    def repeat(tensor, *sizes):
        # Ensure the number of dimensions of tensors and sizes match
        if len(tensor.shape) != len(sizes):
            raise ValueError("Number of dimensions of tensors and sizes must match")

        # Manually create a repeated tensors
        content = tensor.content
        for dim, size in enumerate(sizes):
            slices = [content] * size
            content = np.concatenate(slices, axis=dim)
        tensor = tensor.__class__(content, parse=False)
        return tensor

    def split(self, sep, dim=0):
        """
        Return a new TextTensor, with an additional first dimension to split everything using sep as the delimiter.

          sep
            The delimiter according which to split the bytearray.
            None (the default value) means split on ASCII whitespace characters
            (space, tab, return, newline, formfeed, vertical tab).
        """
        return SplitTextTensor.apply(self, sep, dim)

    def format(self, **kwargs):
        """
        Return a formatted version of self, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        return FormatTextTensor.apply(self, kwargs)

    def save(self, filename="saved_tensors.pt"):
        torch.save(self, filename)

    def to_csv(self, filename, sep="\t"):
        """
        Save a csv with texts or, if available, with embeddings (flattened shape)
        """
        if self._embedding is None:
            self.save(filename, sep=sep)  # Tab as default, because texts have a lot of commas
        else:
            try:
                with open(filename, 'w', newline='') as f:
                    for row in self._content:
                        # Join the elements in the row with commas
                        line = sep.join(row)
                        # Write the line to the file
                        f.write(line + '\n')
            except Exception as E:
                raise Exception(f"Failed to save with embeddings, {E}")

    def backward(
            tensors: _TensorOrTensors,
            grad_tensors: Optional[_TensorOrTensors] = None,
            retain_graph: Optional[bool] = None,
            create_graph: bool = False,
            grad_variables: Optional[_TensorOrTensors] = None,
            inputs: Optional[_TensorOrTensors] = None,
    ) -> None:
        r"""See. docs"""
        if torch._C._are_functorch_transforms_active():
            raise RuntimeError(
                "backward() called inside a functorch transform. This is not "
                "supported, please use functorch.grad or functorch.vjp instead "
                "or call backward() outside of functorch transforms.")

        if grad_variables is not None:
            if grad_tensors is None:
                grad_tensors = grad_variables
            else:
                raise RuntimeError("'grad_tensors' and 'grad_variables' (deprecated) "
                                   "arguments both passed to backward(). Please only "
                                   "use 'grad_tensors'.")
        if inputs is not None and len(inputs) == 0:
            raise RuntimeError("'inputs' argument to backward() cannot be empty.")

        if grad_tensors is None:
            grad_tensors = utils.zeros_like(tensors).reshape(tensors.shape)
        elif isinstance(grad_tensors, str):
            grad_tensors = (TextTensor(grad_tensors),)

        tensors = (tensors,) if isinstance(tensors, torch.Tensor) else tuple(tensors)
        inputs = (inputs,) if isinstance(inputs, torch.Tensor) else \
            tuple(inputs) if inputs is not None else tuple()
        grad_tensors_ = langtorch.torch_utils.tensor_or_tensors_to_tuple(grad_tensors, len(tensors))
        grad_tensors_ = make_grads(tensors, grad_tensors_, is_grads_batched=False)
        if retain_graph is None:
            retain_graph = create_graph

        # The reason we repeat same the comment below is that
        # some Python versions print out the first line of a multi-line function
        # calls in the traceback and some print out the last line
        langtorch.autograd.run_backward(  # langtorch version of a C++ engine that torch uses to run the backward pass
            tensors, grad_tensors_, retain_graph, create_graph, inputs,
            allow_unreachable=True,
            accumulate_grad=True)  # langtorch version of a C++ engine that torch uses to run the backward pass
