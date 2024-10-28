from typing import IO

from click import ClickException
from rich.console import Console


class GlbException(ClickException):
    def __init__(self, message):
        super().__init__(message)

    def show(self, file: IO = None):
        if file:
            super().show(file)
            return

        Console().print(self.message)
