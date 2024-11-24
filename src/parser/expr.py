from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self
from src.common.token import Token

class ExprVisitor[T](ABC): 
    @abstractmethod
    def visit_binary_expr(self, expr: 'BinaryExpr') -> T:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: 'GroupingExpr') -> T:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: 'UnaryExpr') -> T:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: 'LiteralExpr') -> T:
        pass

class Expr(ABC):
    @abstractmethod
    def accept[T](self, visitor: ExprVisitor[T]) -> T:
        pass

@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_binary_expr(self)
    
@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept[T](self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_grouping_expr(self)


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def accept[T](self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_unary_expr(self)


@dataclass
class LiteralExpr(Expr):
    literal: str | float | None
    
    def accept[T](self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_literal_expr(self)
    
    @classmethod
    def create(cls, literal: str | float | None) -> Self:
        return cls(literal)

class ASTPrettyPrinter(ExprVisitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return f"({expr.operator.lexemme} {self.print(expr.left)} {self.print(expr.right)})" 
    
    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return f"({self.print(expr.expression)})"
    
    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return f"({expr.operator.lexemme} {self.print(expr.right)})"
    
    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.literal is None:
            return "None"
        return str(expr.literal)


class RPNPrettyPrinter(ExprVisitor[str]):
    def __init__(self) -> None:
        self.stack: list[str] = []

    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return f"{self.print(expr.left)} {self.print(expr.right)} {expr.operator.lexemme}"
         
    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return f"{self.print(expr.expression)}"
    
    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return f"{expr.operator.lexemme} {self.print(expr.right)}"
    
    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        return str(expr.literal) if expr.literal is not None else "None"
