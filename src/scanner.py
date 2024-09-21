from dataclasses import dataclass

from .token_type import TokenType
from .error import error


@dataclass
class Token:
    lexemme: str
    line: int
    token_type: TokenType = TokenType.EOF
    literal: object | None = None

    def __repr__(self) -> str:
        return f"Token(lexemme='{self.lexemme}', line={self.line}, token_type={self.token_type.name.split(".")[-1]}, literal={self.literal})"


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.source_len = len(source)
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.tokens: list[Token] = []

    def get_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        return self.tokens

    def scan_token(self) -> None:
        c: str = self.advance()
        match c:
            case "(":
                self.add_token(token_type=TokenType.LEFT_PAREN)
            case ")":
                self.add_token(token_type=TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(token_type=TokenType.LEFT_BRACE)
            case "}":
                self.add_token(token_type=TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(token_type=TokenType.COMMA)
            case ".":
                self.add_token(token_type=TokenType.DOT)
            case "-":
                self.add_token(token_type=TokenType.MINUS)
            case "+":
                self.add_token(token_type=TokenType.PLUS)
            case ";":
                self.add_token(token_type=TokenType.SEMICOLON)
            case "*":
                self.add_token(token_type=TokenType.ASTERISK)
            case "!":
                token_type = TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                self.add_token(token_type)
            case "<":
                token_type = TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                self.add_token(token_type)
            case "=":
                token_type = (
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
                self.add_token(token_type)
            case ">":
                token_type = (
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
                self.add_token(token_type)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                ...
            case "\n":
                self.line += 1
            case _:
                error(
                    line=self.line,
                    message="Unexpected character.",
                    loc=self.source[self.start : self.current],
                )

    def add_token(self, token_type: TokenType) -> None:
        self.tokens.append(
            Token(
                lexemme=self.source[self.start : self.current],
                line=self.line,
                token_type=token_type,
                literal=None,
            )
        )

    def match(self, expected_character: str) -> bool:
        if (
            self.current >= self.source_len
            or self.source[self.current] != expected_character
        ):
            return False
        self.current += 1
        return True

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def is_at_end(self) -> bool:
        return self.current >= self.source_len
