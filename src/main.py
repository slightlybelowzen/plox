import pprint
import sys

from src.parser.expr import ASTPrettyPrinter
from src.parser.parser import Parser
from src.scanner.scanner import Scanner


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.get_tokens()
    pprint.pprint(tokens)
    parser = Parser(tokens)
    expr = parser.parse()
    if expr is not None:
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
