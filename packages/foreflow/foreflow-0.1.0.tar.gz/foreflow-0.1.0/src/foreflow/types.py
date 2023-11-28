from __future__ import annotations

from typing import Annotated
from typing import Any
from typing import Literal

import pydantic

from . import util


class StateTask(util.pydantic.PascalModel):
    type: Literal["Task"]
    resource: str
    parameters: dict[str, Any] | None = None

    result_path: str | None = ""

    next: str


class StateSucceed(util.pydantic.PascalModel):
    type: Literal["Succeed"]


State = Annotated[StateTask | StateSucceed, pydantic.Field(discriminator="type")]


class StateMachine(util.pydantic.PascalModel):
    start_at: str
    states: dict[str, State]
