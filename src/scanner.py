from dataclasses import dataclass

from .token_type import TokenType


@dataclass
class Token:
    value: str
    line: int
    token_type: TokenType = TokenType.EOF
    literal: str | None = None


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source

    def get_tokens(self) -> list[Token]:
        return []
