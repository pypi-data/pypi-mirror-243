import random
import string
from typing import Optional, Union


class OneTimeTokenManager:
    def __init__(self, token_size = 6, symbols: Optional[str] = None) -> None:
        self.tokens = {}
        self.token_size = token_size
        self.symbols = symbols or f"{string.ascii_letters}{string.digits}"

    def _generate(self, size):
        return ''.join(random.choices(self.symbols, k=size))
    
    def create(self, email: str):
        token = self._generate(self.token_size)
        self.tokens[token] = email 
        return token

    def release(self, token: str) -> Union[str, None]:
        try:
            return self.tokens.pop(token)
        except KeyError:
            pass

