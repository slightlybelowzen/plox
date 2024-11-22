import pprint
import sys

from src.scanner.token_type import TokenType
from src.parser.expr import ASTPrettyPrinter, BinaryExpr, Expr, GroupingExpr, LiteralExpr, UnaryExpr
from src.scanner.scanner import Scanner
from src.scanner.token import Token


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.get_tokens()
    pprint.pprint(tokens)
    expr: Expr = BinaryExpr.create(
        UnaryExpr.create(
            Token(lexemme="-", line=1, token_type=TokenType.MINUS),
            LiteralExpr.create(123),
        ),
        Token(lexemme="*", line=1, token_type=TokenType.ASTERISK),
        GroupingExpr.create(
            LiteralExpr.create(456),
        ),
    ) 
    print(f"AST:\n  {ASTPrettyPrinter().print(expr)}")


def run_prompt() -> None:
    try:
        inp = input(">>> ")
    except (EOFError, KeyboardInterrupt):
        print("\nshutting down repl")
        exit(0)
    while inp:
        run(inp)
        try:
            inp = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nshutting down repl")
            exit(0)


def main(args: list[str]) -> None:
    if args == []:
        run_prompt()
    else:
        with open(args[0]) as f:
            run(f.read())


if __name__ == "__main__":
    main(sys.argv[1:])
