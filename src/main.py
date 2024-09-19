import sys

from .scanner import Scanner


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.get_tokens()
    print(tokens)


def run_prompt() -> None:
    inp = input(":> ")
    while inp:
        run(inp)
        inp = input(":> ")


def error(line: int, message: str) -> None:
    report_error(line, "", message)


def report_error(line: int, where: str, message: str) -> None:
    # TODO: crash program if error is reported
    sys.stderr.write(f"[line {line}] Error {where} : {message}")


def main(args: list[str]) -> None:
    if args == []:
        run_prompt()
    else:
        with open(args[0]) as f:
            run(f.read())


if __name__ == "__main__":
    main(sys.argv[1:])
