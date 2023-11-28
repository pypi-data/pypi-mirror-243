from __future__ import annotations

from typing import Any


def set_value_1(source: Any, expr: list[str], value: Any) -> None:
    if len(expr) == 1:
        source[expr[0]] = value
        return

    if expr[0] not in source or not isinstance(source[expr[0]], dict):
        source[expr[0]] = {}

    set_value_1(source[expr[0]], expr[1:], value)


def set_value(source: dict[str, Any], expr: str, value: Any) -> None:
    if expr == "":
        for key in list(source.keys()):
            del source[key]

        if not isinstance(value, dict):
            raise ValueError("Cannot set value to empty string")

        source.update(value)  # type: ignore
        return

    set_value_1(source, expr.split("."), value)
