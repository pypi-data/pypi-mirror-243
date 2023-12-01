from typing import Any
from rich.syntax import Syntax
from rich.console import Console

console = Console()


def print_code(
    code: str,
    console_obj: Console = console, 
    language: str = "python", 
    theme: str = "material"
) -> None:
    console_obj.print(Syntax(code, language, theme=theme))


class attrdict(dict):
    def __getattribute__(self, __name: str) -> Any:
        if __name in self:
            return self[__name]
        return super().__getattribute__(__name)
