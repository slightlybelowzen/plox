from src.common.token import Token

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current: int = 0
