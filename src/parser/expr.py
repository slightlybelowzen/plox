import abc
from dataclasses import dataclass
from src.scanner.token import Token


# since python doesn't have hoisting, boo://
class ExprVisitor(abc): ...


# base class for expression trees
class Expr(abc):
    def accept[T](visitor: ExprVisitor) -> T: ...


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(): ...


@dataclass
class Literal(Expr):
    value: str | float

    def accept(): ...


@dataclass
class Unary(Expr):
    operator: Expr
    right: Expr

    def accept(): ...


class ExprVisitor(abc):
    def visit_binary_expr(self, expr: Binary):
        raise NotImplementedError("Not implemented visit method for binary expression")

    def visit_grouping_expr(self, expr: Grouping):
        raise NotImplementedError("Not implemented visit method for group expression")

    def visit_literal_expr(self, expr: Literal):
        raise NotImplementedError("Not implemented visit method for literal expression")

    def visit_unary_expr(self, expr: Unary):
        raise NotImplementedError("Not implemented visit method for unary expression")
