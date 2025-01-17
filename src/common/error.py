from src.common.token_type import TokenType
from src.common.token import Token


def error(line: int, message: str, loc: str) -> None:
    report_error(line=line, message=message, loc=loc)


def report_error(line: int, loc: str, message: str) -> None:
    # TODO: make sure this string formatting is robust for other kinds of errors
    # See src.scanner.scanner.string() for an example where this doesn't quite work
    # TODO: make this raise an actual error and not just print a string
    print(f"Error: {message}")
    print(f"  {line} | {loc}")
    print(f"{"˄-- Here.".rjust(15 + len(loc))}")


def parse_error(token: Token, message: str) -> None:
    if token.token_type == TokenType.EOF:
        report_error(line=token.line, loc=" at end", message=message)
    else:
        report_error(line=token.line, loc=f" at '{token.lexemme}'", message=message)
