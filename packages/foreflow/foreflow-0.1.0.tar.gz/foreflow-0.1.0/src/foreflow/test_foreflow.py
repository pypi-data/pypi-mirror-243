from __future__ import annotations

from typing import Any

import yaml

from . import foreflow
from . import types
from . import util


class Inpt_5cca9516(util.pydantic.PascalModel):
    pass


class Outpt_5cca9516(util.pydantic.PascalModel):
    payload: dict[str, Any]


class Inpt_0d88e907(util.pydantic.PascalModel):
    status: str
    status_name: str


class TestMain:
    def test_5cca9516(self) -> None:
        app = foreflow.Foreflow()

        @app.resource("Foreflow::Callable::Invoke")
        def invoke(inpt: Inpt_5cca9516) -> Outpt_5cca9516:
            return Outpt_5cca9516(
                payload={
                    "Status": "SUCCESS",
                },
            )

        state_machine = """\
StartAt: FirstState
States:
  FirstState:
    Type: Task
    Resource: Foreflow::Callable::Invoke
    Next: End
  End:
    Type: Succeed
"""
        expected = {
            "Payload": {
                "Status": "SUCCESS",
            },
        }

        state_machine = types.StateMachine.model_validate(yaml.safe_load(state_machine))
        ret = app.execute(state_machine, {})

        assert ret.model_dump(mode="json", by_alias=True) == expected

    def test_bd65c858(self) -> None:
        app = foreflow.Foreflow()

        @app.resource("Foreflow::Callable::Invoke")
        def invoke(inpt: Inpt_5cca9516) -> Outpt_5cca9516:
            return Outpt_5cca9516(
                payload={
                    "Status": "SUCCESS",
                },
            )

        state_machine = """\
StartAt: FirstState
States:
  FirstState:
    Type: Task
    Resource: Foreflow::Callable::Invoke
    ResultPath: bd65c858
    Next: End
  End:
    Type: Succeed
"""
        expected = {
            "bd65c858": {
                "Payload": {
                    "Status": "SUCCESS",
                },
            },
        }

        state_machine = types.StateMachine.model_validate(yaml.safe_load(state_machine))
        ret = app.execute(state_machine, {})

        assert ret.model_dump(mode="json", by_alias=True) == expected

    def test_0d88e907(self) -> None:
        app = foreflow.Foreflow()

        @app.resource("Foreflow::Callable::Invoke")
        def invoke(inpt: Inpt_0d88e907) -> Outpt_5cca9516:
            return Outpt_5cca9516(
                payload={
                    "Status": inpt.status,
                    "StatusName": inpt.status_name,
                },
            )

        state_machine = """\
StartAt: FirstState
States:
  FirstState:
    Type: Task
    Resource: Foreflow::Callable::Invoke
    Parameters:
      Status: NG
      StatusName: Not Good
    Next: End
  End:
    Type: Succeed
"""
        expected = {
            "Payload": {
                "Status": "NG",
                "StatusName": "Not Good",
            },
        }

        state_machine = types.StateMachine.model_validate(yaml.safe_load(state_machine))
        ret = app.execute(state_machine, {})

        assert ret.model_dump(mode="json", by_alias=True) == expected

    def test_f286e300(self) -> None:
        app = foreflow.Foreflow()

        @app.resource("Foreflow::Callable::Invoke")
        def invoke(inpt: Inpt_0d88e907) -> Outpt_5cca9516:
            return Outpt_5cca9516(
                payload={
                    "Status": inpt.status,
                    "StatusName": inpt.status_name,
                },
            )

        state_machine = """\
StartAt: FirstState
States:
  FirstState:
    Type: Task
    Resource: Foreflow::Callable::Invoke
    Parameters:
      Status.$: StatusId
      StatusName: Not Good
    Next: End
  End:
    Type: Succeed
"""
        expected = {
            "Payload": {
                "Status": "NG",
                "StatusName": "Not Good",
            },
        }

        state_machine = types.StateMachine.model_validate(yaml.safe_load(state_machine))
        ret = app.execute(state_machine, {"StatusId": "NG"})

        assert ret.model_dump(mode="json", by_alias=True) == expected
