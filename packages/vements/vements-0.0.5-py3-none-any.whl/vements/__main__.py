#!/usr/bin/env python
from typing import Optional

from fire import Fire

from vements.api import API, Output


class CLI(API):
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        super().__init__(api_key=api_key, output=Output.TEXT, verbose=verbose)


if __name__ == "__main__":
    Fire(CLI)
