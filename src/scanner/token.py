from dataclasses import dataclass

from src.scanner.token_type import TokenType


@dataclass
class Token:
    lexemme: str
    line: int
    token_type: TokenType = TokenType.EOF
    literal: str | float | int | None = None

    def __repr__(self) -> str:
        return f"Token(lexemme='{self.lexemme}', line={self.line}, token_type={self.token_type.name.split(".")[-1]}, literal={self.literal})"
