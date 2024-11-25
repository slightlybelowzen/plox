from src.scanner.keywords import KEYWORDS
from src.common.token_type import TokenType
from src.common.error import error
from src.common.token import Token


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
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    error(
                        line=self.line,
                        message="Unexpected character.",
                        loc=self.source[self.start : self.current],
                    )

    def identifier(self) -> None:
        while self.peek().isalpha():
            self.advance()

        text = self.source[self.start : self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        self.add_token(token_type)

    def number(self) -> None:
        type = "integer"
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek_next().isdigit():
            # if we encounter a digit after a decimal point, we know it's a float
            type = "float"
            self.advance()
            while self.peek().isdigit():
                self.advance()
        number_type = int if type == "integer" else float
        self.add_token(TokenType.NUMBER, number_type(self.source[self.start : self.current]))

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            """
            For a case like this: `print "hello, world`
            We want to report the error before the newline not after processing it
            Right now we get this error:
            Error: Unterminated string.
                2 | "hello, world
                                
                                ˄-- Here.
            Instead, we want this no matter how many newlines are present after the unterminated string:
            Error: Unterminated string.
                2 | "hello, world
                                ˄-- Here.
            """
            error(
                self.line,
                "Unterminated string.",
                self.source[self.start : self.current],
            )
            return
        self.advance()

        string_literal = self.source[self.start + 1 : self.current - 1]
        self.add_token(token_type=TokenType.STRING, literal=string_literal)

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        self.tokens.append(
            Token(
                lexemme=self.source[self.start : self.current],
                line=self.line,
                token_type=token_type,
                literal=literal,
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

    def peek_next(self) -> str:
        if self.current + 1 >= self.source_len:
            return "\0"
        return self.source[self.current + 1]

    def is_at_end(self) -> bool:
        return self.current >= self.source_len
