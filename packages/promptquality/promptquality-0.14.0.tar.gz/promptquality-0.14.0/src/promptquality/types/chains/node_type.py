from enum import Enum


class ChainNodeType(str, Enum):
    chain = "chain"
    chat = "chat"
    llm = "llm"
