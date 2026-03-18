# -*- coding: utf-8 -*-
from settings import settings


def sep(text: str, *, n: int = 4, char: str = '*') -> None:
    print('\n{0} {1} {0}'.format(n * char, text))


def debug(text: str) -> None:
    if settings.debug:
        print(f'[DEBUG] {text}')
