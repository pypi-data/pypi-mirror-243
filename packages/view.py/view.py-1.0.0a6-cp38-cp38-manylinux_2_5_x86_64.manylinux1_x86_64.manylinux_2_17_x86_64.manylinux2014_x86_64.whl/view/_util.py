from __future__ import annotations

import getpass
import inspect
import os
import pathlib
import runpy
import socket
import sys
import warnings
import weakref
from collections.abc import Iterable
from pathlib import Path
from types import FrameType as Frame
from types import FunctionType as Function
from typing import Any, Union

from rich.panel import Panel
from rich.syntax import Syntax
from typing_extensions import Annotated, TypeGuard

from ._logging import Internal
from .exceptions import NotLoadedWarning

try:
    from types import UnionType
except ImportError:
    UnionType = None

TypingUnionType = type(Union[str, int])

__all__ = (
    "is_union",
    "LoadChecker",
    "set_load",
    "shell_hint",
    "make_hint",
    "is_annotated",
    "run_path",
)


def is_union(tp: type[Any]) -> bool:
    return tp in {UnionType, TypingUnionType}


AnnotatedType = type(Annotated[str, ""])


def is_annotated(hint: Any) -> TypeGuard[AnnotatedType]:
    return (type(hint) is AnnotatedType) and hasattr(hint, "__metadata__")


class LoadChecker:
    _view_loaded: bool

    def _view_load_check(self) -> None:
        if (not self._view_loaded) and (
            not os.environ.get("_VIEW_CANCEL_FINALIZERS")
        ):
            warnings.warn(f"{self} was never loaded", NotLoadedWarning)

    def __post_init__(self) -> None:
        self._view_loaded = False
        weakref.finalize(self, self._view_load_check)


def set_load(cl: LoadChecker):
    """Let the developer feel that they aren't touching private members."""
    cl._view_loaded = True


def shell_hint(command: str) -> Panel:
    if os.name == "nt":
        shell_prefix = f"{os.getcwd()}>"
    else:
        shell_prefix = (
            f"{getpass.getuser()}@{socket.gethostname()}[bold green]$[/]"
        )
    return Panel.fit(f"{shell_prefix} {command}", title="Terminal")


def make_hint(
    comment: str | None = None,
    caller: Function | None | Iterable[Function] | str = None,
    *,
    line: int | None = None,
    prepend: str = "",
    back_lines: int = 1,
) -> Syntax | str:
    if not isinstance(caller, str):
        frame: Frame | None = inspect.currentframe()

        assert frame, "failed to get frame"

        back: Frame | None = frame.f_back
        assert back, "failed to get f_back"

        code_list = []

        if caller:
            if isinstance(caller, Iterable):
                code_list.extend(caller)
            else:
                code_list.append(caller.__code__)
        else:
            code_list.append(back.f_code)

        while back.f_back:
            back = back.f_back

            if back.f_code in code_list:
                break

        txt = pathlib.Path(back.f_code.co_filename).read_text(
            encoding="utf-8",
        )
        line = line or (back.f_lineno - back_lines)
    else:
        caller_path = pathlib.Path(caller)

        if not caller_path.exists():
            return ""

        txt = caller_path.read_text(encoding="utf-8")
        line = line or 0

    split = txt.split("\n")

    if comment:
        split[line] += f"{prepend}  # {comment}"

    return Syntax(
        "\n".join(split),
        "python",
        line_numbers=True,
        line_range=(line - 10, line + 20),
        highlight_lines={(line + 1) if not line < 0 else len(txt) - line},
    )


def run_path(path: str | Path) -> dict[str, Any]:
    sys.path.append(str(Path(path).parent.absolute()))
    path = str(Path(path).absolute())
    Internal.info(f"running: {path}")
    mod = runpy.run_path(path, run_name="__view__")
    sys.path.pop()
    return mod
