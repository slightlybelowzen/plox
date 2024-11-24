def error(line: int, message: str, loc: str) -> None:
    report_error(line=line, message=message, loc=loc)


def report_error(line: int, loc: str, message: str) -> None:
    # TODO: crash program if error is reported
    # TODO: make sure this string formatting is robust for other kinds of errors
    print(f"Error: {message}")
    print(f"  {line} | {loc}")
    print(f"{"˄-- Here.".rjust(15 + len(loc))}")
