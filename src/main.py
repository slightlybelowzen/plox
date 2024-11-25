import sys

from src.scanner.scanner import Scanner


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.get_tokens()


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
    # don't want a massive stack trace vomit when we raise an error
    sys.tracebacklimit = -1
    if args == []:
        run_prompt()
    else:
        with open(args[0]) as f:
            run(f.read())


if __name__ == "__main__":
    main(sys.argv[1:])
