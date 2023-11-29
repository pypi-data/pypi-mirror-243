from .text import Text


class Chat(Text):
    allowed_keys = ["system", "user", "assistant"]

    @classmethod
    def str_formatter(cls, instance):
        return "\n".join([f"{k}: {cls._concatenate_terminals(v)}" for k, v in instance.items()])


class ChatML(Chat):
    allowed_keys = ["user", "assistant", "system"]

    @classmethod
    def str_formatter(cls, instance):
        if instance.keys()[-1] == "user":
            return "\n".join(
                [f"<|im_start|>{k}\n{v}<|im_end|>" for k, v in instance.items()]) + "\n<|im_start|>assistant"
        else:
            return "\n".join([f"<|im_start|>{k}\n{v}<|im_end|>" for k, v in instance.items()])


class HumanMessage:
    def __new__(cls, content):
        from langtorch.tensors.texttensor import TextTensor, ChatTensor
        if isinstance(content, str):
            return Chat([("user", content)], parse=False)
        elif isinstance(content, TextTensor):
            return ChatTensor(content.set_key("user"), parse=False)
        else:
            raise ValueError("Content must be of type Text or str.")


class AIMessage:
    def __new__(cls, content):
        from langtorch.tensors.texttensor import TextTensor, ChatTensor
        if isinstance(content, str):
            return Chat([("assistant", content)], parse=False)
        elif isinstance(content, TextTensor):
            return ChatTensor(content.set_key("assistant"), parse=False)
        else:
            raise ValueError("Content must be of type Text or str.")


### MESSAGE ALIASES
User, Assistant = HumanMessage, AIMessage
