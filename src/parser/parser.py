from src.common.error import parse_error
from src.common.token_type import TokenType
from src.parser.expr import BinaryExpr, Expr, GroupingExpr, LiteralExpr, UnaryExpr
from src.common.token import Token


class ParseError(Exception): ...


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current: int = 0

    def synchronize(self) -> None:
        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return
            match self.peek().token_type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.PRINT
                    | TokenType.RETURN
                    | TokenType.VAR
                    | TokenType.WHILE
                    | TokenType.FOR
                    | TokenType.IF
                ):
                    return
        self.advance()

    def parse(self) -> Expr:
        try:
            return self.expression()
        except ParseError as _:
            return None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.ASTERISK):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return LiteralExpr(False)
        if self.match(TokenType.TRUE):
            return LiteralExpr(True)
        if self.match(TokenType.NIL):
            return LiteralExpr(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)
        parse_error(self.peek(), "Expect expression.")

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseError:
        parse_error(token, message)
        return ParseError()

    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)

    def peek(self) -> Token:
        return self.tokens[self.current]
