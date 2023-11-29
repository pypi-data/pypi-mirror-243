import json
import logging
import re
from typing import List, Any, Tuple, Union

import numpy as np
import torch
from pyparsing import *

from ..grammars.langtorch_default_grammar import LangTorchGrammarParser


class Text(str):
    parsers = {"langtorch-f-string": LangTorchGrammarParser}
    language = "langtorch-f-string"
    allowed_keys = None

    @classmethod
    def parse(cls, arg):
        parsed_result = cls.parsers[cls.language].parseString(arg)
        arg = [(res.key if "key" in res else "", res.value if "value" in res else "") if isinstance(res,
                ParseResults) else res for res in parsed_result]
        return arg

    def __new__(cls, *substrings, parse: Union[str, bool] = "langtorch-f-string", **named_substrings):
        """
        Construct a new Text instance. Allows for various input formats.

        Args:
            *substrings (Union[str,Tuple[str, str], List[str]): Flexible input data. Can be a parsable string, string sequences, key-value pairs, dicts...
                                    If None is passed, it will be replaced with a Text instance with empty content.
            parse (Union[bool, str], optional): Enable/disable or specify langauge for parsing of input content.
                                        The default behavior is splits strings with an f-string-like syntax.
                                        You can pass a name of a markup languag to parse it with pandoc.
                                        Set to False to disable parsing. You can load a text file with
                                        "file::path/to/file.txt" or "file::path/to/file.txt::lang" to specify
                                        the language.
            **named_substrings (str): Additional named textual data entries.

        Returns:
            (Text): A structured textual instance.

        Raises:
            ParseException: If automatic parsing fails. Consider disabling parsing if this occurs.
            ValueError: When an unsupported input format is provided e.g. a TextTensor is passed.
        """
        if len(substrings) == 0 or (len(substrings) == 1 and substrings[0] is None):
            instance = super().__new__(cls, "")
            instance._content = tuple()
            return instance
        content = [c if c is not None else cls.identity for c in (list(substrings) + list(named_substrings.items()))]
        # cast TextTensors to strings
        for i in range(len(content)):
            if isinstance(content[i], torch.Tensor) and hasattr(content[i], "content"):
                content[i] = content[i].sum().item()
                assert isinstance(content[i], str) or (0 < len(content[i]) <= 2)
        # returns the final content tuple
        if len(content) == 1 and cls._is_valid_tree(content, is_tuple=True):
            content = content[0]
        else:
            content = cls.to_ast(*content, parse=parse, is_tuple=True)

        assert cls._is_valid_tree(content, is_tuple=True), f"Invalid tree: {content}"

        instance = super().__new__(cls, cls._concatenate_terminals(content))
        instance._content = content
        instance.parse = parse
        # if instance.allowed_keys is not None and any([k not in instance.allowed_keys for k in instance.keys()]):
        #     raise ValueError(f"Invalid key found in {instance.keys()}. Only {instance.allowed_keys} keys are allowed.")
        return instance

    @classmethod
    def to_ast(cls, *args, parse="f-string", is_tuple=False):
        """Reformats a wide array of construtor patterns into a unified AST-like format"""
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        if len(args) == 1 and ((isinstance(args[0], tuple) and len(args[0]) > 2) or isinstance(args[0], list)):
            # List or tuple of strings / named strings
            args = args[0]
        elif isinstance(args[0], dict):
            # Dictionary of named strings
            args = args[0].items()
        elif isinstance(args[0], Text) and len(args) == 1:
            # Passing cls instance to itself
            args = args[0].content
        elif all([isinstance(arg, str) for arg in args]):
            if parse:
                try:
                    result = []
                    for arg in args:
                        arg = cls.parse(arg)
                        result += arg
                    args = result
                except ParseException as E:
                    print(f"Last parsed string: {arg}")
                    raise ParseException(str(E) + "\nYou may want to disable string parsing, with parse = False")
            else:
                pass
        if any([isinstance(arg, torch.Tensor) for arg in args]):
            raise ValueError(
                "You cannot initialise Text from a TextTensor. Use tensors.item() or otherwise transform the tensors to a string, list or dictionary.")

        def simplify(arg, parse=False):
            if isinstance(arg, tuple) and len(arg) == 2 and not (isinstance(arg[0], str) and isinstance(arg[1], str)):
                # Fix tuple types
                return (str(arg[0]), simplify(arg[1]))
            elif isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], str) and isinstance(arg[1], str):
                # CORRECT
                return arg
            elif isinstance(arg, tuple) and len(arg) == 1:
                # CORRECT though should be avoided
                return arg[0]
            elif isinstance(arg, tuple) and len(arg) > 2:
                # Assume a tuple of length != 2 was supposed to be a list
                logging.debug(
                    f"Tuples of length 2 represent (key, value) in Text objects. When parsing a Text entry was a tuple of length {len(arg)},\nit was converted to a list and may lead to errors.")
                arg = list(arg)

            # Not a named string
            if isinstance(arg, list) and len(arg) == 1:
                return arg[0]
            elif isinstance(arg, (list, np.ndarray, torch.Tensor)):
                return [simplify(element, parse=parse) for element in arg]
            elif isinstance(arg, Text):
                if len(arg.items()) == 1:
                    return Text.to_ast(arg.items()[0], parse=parse)
                else:
                    return Text.to_ast(arg.items(), parse=parse)
            elif hasattr(arg, 'items'):
                return Text.to_ast(list(arg.items()), parse=parse)
            elif isinstance(arg, str):
                # CORRECT
                return arg
            else:  # Cast to string
                return str(arg)
            # Maybe consider: raise ParseException(f"Could not parse {arg} of type {type(arg).__name__}")

        content = [simplify(arg, parse=parse) for arg in args]

        if not is_tuple:  # Recursive case: In these cases we are returning a node or tree with a single root node
            return content[0] if isinstance(content, list) and len(content) == 1 else content
        else:  # Base case: In these cases we are returning a tuple of nodes for the ._content attribute
            def check_for_lists(tree):  # A basic check for lists in the tree
                if isinstance(tree, list):
                    # Prune single-element lists
                    if len(tree) == 1:
                        raise ValueError(f"single-element list {tree}")
                    else:
                        return [check_for_lists(element) for element in tree]
                elif isinstance(tree, tuple) and len(tree) == 2:
                    key, value = tree
                    return key, check_for_lists(value)
                return tree

            content = tuple(check_for_lists(arg) for arg in content)

            return content

    @classmethod
    def is_terminal_node(cls, entry):
        if isinstance(entry, str) and not isinstance(entry, Text):
            return True
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and isinstance(entry[1], str):
            return True
        return False

    @classmethod
    def _is_valid_tree(cls, entry, is_tuple=False):
        """
        Checks if an entry is a valid tree for a Text instance.

        """
        if isinstance(entry, cls):
            entry = entry.items()
        elif isinstance(entry, tuple) and is_tuple:
            if len(entry) == 0:
                return True
            entry = list(entry) if len(entry) > 1 else entry[0]
        # Base cases
        if cls.is_terminal_node(entry):
            return True

        # Recursive cases
        if isinstance(entry, tuple) and len(entry) != 2:
            return False
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and (
                isinstance(entry[1], list) or isinstance(entry[1], tuple)):
            return all(cls._is_valid_tree(child) for child in entry[1])
        if isinstance(entry, list) and len(entry) > 1:
            return all(cls._is_valid_tree(child) for child in entry)
        if isinstance(entry, list) and len(entry) <= 1:
            return False  # Single-element lists are not valid

        # If none of the above cases match, it's not valid
        return False

    @classmethod
    def str_formatter(cls, instance) -> str:
        """
        Formats the human-readable string of a Text instance. Subclasses of Text can reimplement this method!

        Args:
            instance (Text): An instance of the Text class.

        Returns:
            (str): A string representation of the instance.
        """
        return cls._concatenate_terminals(instance.items())

    @classmethod
    def _concatenate_terminals(cls, entry) -> str:
        result = ""

        # Base cases
        if cls.is_terminal_node(entry):
            return entry if isinstance(entry, str) else entry[1]

        # Recursive cases
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and (
                isinstance(entry[1], list) or isinstance(entry[1], tuple)):
            return ''.join(cls._concatenate_terminals(child) for child in entry[1])
        if isinstance(entry, list):
            return ''.join(cls._concatenate_terminals(child) for child in entry)

        return result

    def __str__(self):
        return self.__class__.str_formatter(self)

    @classmethod
    def from_messages(cls, *messages):
        """Text from a list of dicts with keys 'role' and 'content'"""
        if isinstance(messages[0], list):
            messages = messages[0]
        text = []
        for m in messages:
            if isinstance(m, list):
                for mm in m:
                    text.append(mm["role"], m["content"])
            else:
                text.append((m["role"], m["content"]))
        return cls(*text)

    @classmethod
    def from_api_response(cls, *response_dicts):
        """Text from a list of dicts with keys 'role' and 'content'"""
        if isinstance(messages[0], list):
            messages = messages[0]
        text = []
        for m in messages:
            if isinstance(m, list):
                for mm in m:
                    text.append(mm["role"], m["content"])
            else:
                text.append((m["role"], m["content"]))
        return cls(*text)

    def keyed_print(self):
        """
        Prints the Text instance with keys aligned over their corresponding values.
        """
        # Extract the key-value pairs from the _content attribute
        key_value_pairs = [pair if isinstance(pair, tuple) else ('', pair) for pair in self.items()]

        # Find the longest key and value for formatting purposes
        longest_key = max(len(key) for key, _ in key_value_pairs)
        longest_value = max(len(value) for _, value in key_value_pairs)

        # Create the top and bottom lines for the keys and values
        top_line = ""
        bottom_line = ""
        for key, value in key_value_pairs:
            # Calculate padding to center the key
            total_padding = longest_key - len(key)
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding

            # Add the formatted key and value to the respective lines
            top_line += f"{' ' * left_padding}{key}{' ' * right_padding}|"
            bottom_line += f"{value.ljust(longest_value)}|"

        # Remove the trailing '|' character
        top_line = top_line.rstrip('|')
        bottom_line = bottom_line.rstrip('|')

        # Print the formatted lines
        print(top_line)
        print(bottom_line)

    def __repr__(self):
        return self.__str__()

    def to_tensor(self):
        from langtorch import TextTensor
        return TextTensor(self.content)

    @property
    def identity(self):
        return self.__class__()

    @property
    def content(self):
        return [self.__class__(m, parse=False) for m in self._content]

    @content.setter
    def content(self, content):
        if isinstance(content, tuple) and len(content) == 2 and (
                isinstance(content[0], str) and isinstance(content[1], str)):
            AttributeError(
                f"When setting the .content attribute, passing a tuple of strings is ambiguous. Pass either a list with a (key, value) tuple or a list with two strings."
            )

        if isinstance(content, list):
            content = tuple(content)
        assert isinstance(content, tuple)
        self._content = self.to_ast(content, parse=False, is_tuple=True)

    def items(self):
        """
        Retrieves key-value pairs from the Text object, allowing for structured data extraction
        and further processing.

        Returns:
            (List[Tuple[str, Union[str, Tuple[...]]]]): A list of key-value pairs representing the Text's content.
        """
        return [(arg[0], arg[1]) if isinstance(arg, tuple) else ('', arg) for arg in self._content]
        # return [(arg[0], str(self.__class__(arg[1])))) if isinstance(arg, tuple) else ('', str(self.__class__(arg))) for arg in self._content]

    def keys(self):
        return [s[0] for s in self.items()]

    def values(self):
        return [s[1] for s in self.items()]

    def set_key(self, key, inplace=False):
        """
        Override keys for the textual entries, used for restructuring the content.
        Useful for substituting the key right before passing TextTensor to a Module.

        Args:
            key (Union[Text, str, List[str]]): The new key or keys to apply
            inplace bool: .

        Returns:
            (Text): A new Text instance with updated keys.
        """
        # The use of Text.str_formatter(t) instead of str(t) here and elsewhere is for subclasses of Text to reimplement __str__
        if isinstance(key, Text):
            key = key.values()
            if len(key) == 1:
                key = key[0]

        if isinstance(key, list):
            assert len(key) == len(
                self.values()), f"Number of keys ({len(key)}) must match number of values ({len(self.values())})"
            content = tuple((k, v) for k, v in zip(key, self.values()))
        elif isinstance(key, str):
            content = ((key, Text.str_formatter(self)),)
        if inplace:
            self.content = content
            return self
        else:
            return self.__class__(*content)

    def set_key_(self, keys):
        self.set_key(keys, inplace=True)

    def add_key(self, key, inplace=False):
        """
        Add a top-level  key, placing the items of the original as a value under the new key.
        Useful for working with nested keys like in Chat prompts.

        Args:
            key (Union[Text, str, List[str]]): The new key to add
            inplace bool: .

        Returns:
            (Text): A new Text instance with updated keys.
        """
        # The use of Text.str_formatter(t) instead of str(t) here and elsewhere is for subclasses of Text to reimplement __str__
        if isinstance(key, Text):
            key = key.values()
            if len(key) == 1:
                key = key[0]

        if isinstance(key, list) and len(key) > 1:
            assert len(key) == len(
                self.content), f"Number of keys ({len(key)}) must match number of entries ({len(self.content)})"
            content = tuple((k, v) for k, v in zip(key, self.content))
        elif isinstance(key, str):
            content = ((key, self.to_ast(self.items())),)

        if inplace:
            self.content = content
            return self
        else:
            return self.__class__(*content)

    def add_key_(self, keys):
        return self.add_key(keys, inplace=True)

    @property
    def iloc(self):
        """
        Order-based indexing. e.g. .loc[2:5]
        """

        class IlocIndexer:
            def __init__(self, text_items, text_class):
                self.text_items = text_items
                self.text_class = text_class

            def __getitem__(self, index):
                # Handle single integer index
                if isinstance(index, int):
                    try:
                        return self.text_class(self.text_items[index], parse=False)
                    except IndexError:
                        raise IndexError("Index out of range")

                # Handle slices
                elif isinstance(index, slice):
                    return self.text_class(self.text_items[index], parse=False)

                # Handle a list of indices
                elif isinstance(index, list):
                    # Check if all elements in the list are integers
                    if not all(isinstance(idx, int) for idx in index):
                        raise IndexError("All indices must be integers")
                    try:
                        return self.text_class([self.text_items[idx] for idx in index], parse=False)
                    except IndexError:
                        raise IndexError("List index out of range")

                else:
                    raise TypeError("Invalid index type")

            # TODO implement __setitem__ for iloc

        # Assuming self._content stores the structured content in a list or tuple format
        if isinstance(self._content, (list, tuple)):
            items = self._content
        else:
            raise TypeError("Content type unsupported for iloc indexing.")

        return IlocIndexer(items, self.__class__)

    @property
    def loc(self):
        """
        Key-based indexing. You can access entries with nested keys using dot notation, e.g. .loc["key1.key2"]
        """

        class LocIndexer:
            def __init__(self, text_instance):
                self.text_instance = text_instance
                self.text_class = text_instance.__class__

            def __getitem__(self, key):
                # Function to recursively get sub-items

                def get_subitems(items, keys):
                    if keys and isinstance(items, list):
                        next_key = keys.pop(0)
                        sub_items = [v for k, v in items if k == next_key]
                        if not keys:  # No more subkeys, return what we have found
                            return sub_items
                        else:  # We have more keys to search for
                            nested_items = []
                            for _, v in sub_items:
                                # Assuming v is a list of tuples as per Text structure
                                nested_items.extend(get_subitems(v, keys.copy()))
                            return nested_items
                    if isinstance(items, list):
                        return items
                    else:
                        return [items]

                if isinstance(key, str):
                    # Handle key with dot notation for nested access
                    if '.' in key:
                        keys = key.split('.')
                        return self.text_class(get_subitems(self.text_instance.items(), keys), parse=False)
                    # Single key, simple lookup
                    return self.text_class([v for k, v in self.text_instance.items() if k == key], parse=False)

                # If the key is a list, return a subset with keys preserved.
                elif isinstance(key, list):
                    return self.text_class([(k, v) for k, v in self.text_instance.items() if k in key], parse=False)

                else:
                    raise KeyError(f"Invalid key type: {type(key)}")

            def __setitem__(self, key, value):
                def set_items_in_tuple(tup, keys, value, replace=True):
                    value = self.text_instance.to_ast(value)  # format value

                    if isinstance(keys, str):
                        keys = [keys]
                        replace = False

                    # Reconstruct the tuple with replacements
                    rebuilt = []
                    for item in tup:
                        k, v = item if isinstance(item, tuple) else ('', item)
                        if k in keys:
                            # Replace the entire key-value pair
                            new_item = value if replace else (k, value)
                            rebuilt.append(new_item)
                        else:
                            if replace:
                                raise KeyError(
                                    f"Key {keys} not found in texts items {tup}. If you wanted to use .loc to append with key, use a string key not a list.")
                            else:
                                rebuilt.append(self.text_instance.to_ast(item))
                    return tuple(rebuilt)

                self.text_instance._content = set_items_in_tuple(self.text_instance._content, key, value)

        return LocIndexer(self)

    def split(self, sep=" ", mode="auto"):
        modes = ["auto", "words", "sentances", "paragraphs"]
        assert mode in modes, f"Mode must be one of {modes}"
        from langtorch import TextTensor
        return TextTensor(str(self).split() if sep == "" else str(self).split(sep), parse=False)

    def __getitem__(self, index):
        if isinstance(index, str):
            return self.loc[index]
        return self.iloc[index]

    def __or__(self, other):
        return

    def __len__(self):
        return len(str(self.content))

    def __iter__(self):
        for s in self.content:
            yield s

    def __add__(self, other):
        if isinstance(other, str) and not isinstance(other, Text):
            return self.__class__(*self.content, other, parse=False)
        elif isinstance(other, Text):
            return self.__class__(*self.content, *other.content, parse=False)
        else:
            raise TypeError(f'Cannot add {type(other)}')

    def __mul__(self, other, strict=False):
        # TODO: Add strict mode
        if isinstance(other, str) and not isinstance(other, Text):
            try:
                other = Text(other)
            except ParseException:
                other = Text(other, parse=False)
        content = self.items()
        result = content
        formatted_indices = []
        indices_to_delete = []
        positional_j = 0
        for i, (k, v) in enumerate(content):
            if v == "*":
                logging.debug(f"Wildcard {(k, v)} ::filled with:: {other.items()}")
                if k == "":
                    result = result[:i] + list(other.items()) + result[i + 1:]
                else:
                    result[i] = (k, other.items())
                return self.__class__(*result, parse=False)  # TODO the case of the other having a re-key pattern
        for j, (k_, v_) in enumerate(other.items()):
            # Wildcard case -> Adding a key
            if v_ == "*":
                for i in indices_to_delete:
                    result.pop(i)
                result = [(k_, result)]
                indices_to_delete, formatted_indices = [], []
            elif k_ == "" and j not in formatted_indices:  # Positional arguments
                for i, (k, v) in enumerate(content):
                    if v == str(positional_j):
                        logging.debug(f"Place at numbered spot: {(k, v_)} ::at:: {i}")
                        result[i] = (k, v_)
                        positional_j += 1
                        formatted_indices.append(i)
                        break
                else:
                    for i, (k, v) in enumerate(content):
                        if v == "":
                            logging.debug(f"Place: {(k, v_)} ::at:: {i}")
                            result[i] = (k, v_)
                            formatted_indices.append(i)
                            if v_ == k:
                                indices_to_delete.append(i)
                            break
                    else:
                        logging.debug(f"Append {(k_, v_)} ::to:: {content}")
                        result += [(k_, v_)]
            else:
                for i, (k, v) in enumerate(content):
                    if i not in formatted_indices:
                        if (k, v) == (v_, k_):
                            logging.debug(f"Identity: {(k_, v_)} ::with:: {content[i]}")
                            formatted_indices.append(i)
                            indices_to_delete.append(i)
                            break
                        elif v == k_:
                            logging.debug(f"Replace content: {(k_, v_)} ::with:: {content[i]}")
                            result[i] = (k, v_)
                            formatted_indices.append(i)
                            break
                        elif k == v_:
                            logging.debug(f"Replace key: {(k_, v_)} ::with:: {content[i]}")
                            result[i] = (k_, v)
                            formatted_indices.append(i)
                            break
                        # elif k == k_:  # I DISABLED THIS RULE AS IT DOESNT WORK WELL WITH E.G. CHAT MESSAGES
                        #     logging.debug(f"Concatenate: {(k_,v_)} ::with:: {content[i]}")
                        #     result[i] = (k,v+v_)
                        #     break
                else:
                    logging.debug(f"Append {(k_, v_)} ::to:: {content}")
                    # Append the ones that didn't have a {key}
                    # If you don't want this consider using | operation
                    result += [(k_, v_)]
        for i in indices_to_delete:
            result.pop(i)
        return self.__class__(*result, parse=False)

    def format(self, *args, **kwargs):
        other = Text(*args, parse=False) + Text(kwargs, parse=False)
        available_values = self.values()
        entries_with_corresponding_values = []
        for i, k in enumerate(other.keys()):
            if k in available_values:
                entries_with_corresponding_values.append(i)
                available_values.pop(available_values.index(k))
        return self.__mul__(other, strict=True)

    def inv(self):
        return self.__class__(*[(v, k) for k, v in self.items()], parse=False)

    def __pow__(self, power):
        if power == -1:
            return self.inv()
        else:
            raise ValueError("Can only use power -1")

    def method_apply(self, method: str, *args, to="values", **kwargs):
        assert to in ["values", "keys", "both"]
        if to == "values":
            return self.__class__(*list((k, getattr(v, method)(*args, **kwargs)) for k, v in self.items()), parse=False)
        elif to == "keys":
            return self.__class__(*list((getattr(k, method)(*args, **kwargs), v) for k, v in self.items()), parse=False)
        elif to == "both":
            return self.__class__(*list(
                (getattr(k, method)(*args, **kwargs), getattr(v, method)(*args, **kwargs)) for k, v in self.items()),
                                  parse=False)

    def apply(self, func, *args, to="values", **kwargs):
        assert to in ["values", "keys", "both"]
        if to == "values":
            return self.__class__(*list((k, func(v, *args, **kwargs)) for k, v in self.items()), parse=False)
        elif to == "keys":
            return self.__class__(*list((func(k, *args, **kwargs), v) for k, v in self.items()), parse=False)
        elif to == "both":
            return self.__class__(*list(func((k, v), *args, **kwargs) for k, v in self.items()), parse=False)

    def inspect(self):
        return "|".join(f"{v} " + "{" + k + "}, " for k, v in self.items())

    def upper(self):
        return self.method_apply("upper")

    def lower(self):
        return self.method_apply("lower")


    @classmethod
    def from_pandoc_json(cls, ast_json: str) -> 'Text':
        """
        Creates a Text object from a Pandoc AST JSON string.
        """
        ast = json.loads(ast_json)
        content = cls._parse_elements(ast['blocks'])
        return cls(content)

    @classmethod
    def _parse_elements(cls, elements: List[Any]) -> List[Tuple[str, Any]]:
        """
        Recursively parses Pandoc AST elements into a list of tuples.
        """
        result = []
        for element in elements:
            type_ = element['t']
            if type_ == 'Header':
                level, _, inlines = element['c']
                text_content = cls._join_key_value(cls._parse_elements(inlines))
                result.append((f'header_h{level}', text_content))
            elif type_ == 'Para':
                text_content = cls._join_key_value(cls._parse_elements(element['c']))
                result.append(('p', text_content))
            elif type_ == 'Str':
                result.append(('text', element['c']))
            elif type_ == 'Space':
                result.append(('space', ' '))
            elif type_ == 'Emph':
                emph_text = cls._join_key_value(cls._parse_elements(element['c']))
                result.append(('emph', emph_text))
            elif type_ == 'Strong':
                strong_text = cls._join_key_value(cls._parse_elements(element['c']))
                result.append(('strong', strong_text))
            # ... Add more cases for other types of elements like lists, links, etc.
        return result

    @classmethod
    def _join_key_value(cls, elements: List[Tuple[str, Any]]) -> str:
        """
        Concatenates parsed text elements, handling spaces and formatting.
        """
        text = ''
        for element in elements:
            if element[0] in ['text', 'space']:
                text += element[1]
            else:
                # Add formatting tags or handle other types of elements
                text += f"<{element[0]}>{element[1]}</{element[0]}>"
        return text

    @classmethod
    def dict_to_ast(cls, dicts):
        import ast
        return ast.literal_eval(str(dicts).replace(":", ": ").replace("{", "{ ").replace("}", " }"))

    @classmethod
    def guess_format(cls, text):
        # Patterns for markup languages
        patterns = {
            'html': r'<!DOCTYPE html>|<html>',
            'markdown': r'^# .+|^- |\*\*[^*]+\*\*|__[^\_]+__',
            'latex': r'\\documentclass',
            # Add more patterns for other markup languages
        }

        # Check for markup language patterns
        for format_name, pattern in patterns.items():
            if re.search(pattern, text, re.MULTILINE):
                return format_name

        # Check for custom language
        if Text.detect_custom_language(text):
            return 'custom_language'

        # Default to plain texts if no patterns match
        return 'plain'

    @classmethod
    def detect_custom_language(cls, text):
        named_string_pattern = r'(\w+\{\:\w+\})|(`\w+`\{\:\w+\})|(\{\w+\:\w+\})|(\{\`\w+\`\:\w+\})|(\w+\{\`\`\:\})|(\{\:\w+\})'
        unnamed_string_pattern = r'(\{\w+\[\:\]\})|(\{\`\w+\`\:\})|(\{\`\w+\`\})|(\{\`\w+\`\:\})|\{\}|\`\`'
        full_pattern = fr'({named_string_pattern}|{unnamed_string_pattern})'
        # Match the pattern exactly; ^ and $ are the start and end of the string anchors respectively
        return bool(re.fullmatch(full_pattern, text))

    @classmethod
    def guess_language(cls, text):
        return Text.guess_format(text)


class String(Text):
    allowed_keys = [""]
    language = 'plain'

    @classmethod
    def str_formatter(cls, instance):
        return instance.values()[0] if len(instance.values()) > 0 else ""

    @classmethod
    def to_ast(*args, parse=False, is_tuple=False):
        return (("", "".join(args)),)
