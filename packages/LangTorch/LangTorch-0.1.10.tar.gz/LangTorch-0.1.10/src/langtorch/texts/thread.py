import ast

from .text import Text
from .chat import Chat


class Thread(Text):
    allowed_keys = ["user", "assistant"]

    @classmethod
    def str_formatter(cls, instance):
        return "\n".join([f"{k}: {cls._concatenate_terminals(v)}" for k, v in instance.items()])


