from .text import Text


class String(Text):
    allowed_keys = [""]

    @classmethod
    def str_formatter(cls, instance):
        return instance.values()[0] if len(instance.values()) > 0 else ""

    @classmethod
    def constructors(*args, parse=False):
        return [("", "".join(args))]
