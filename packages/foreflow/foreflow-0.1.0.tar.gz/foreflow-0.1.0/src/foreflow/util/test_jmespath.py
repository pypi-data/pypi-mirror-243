from __future__ import annotations

from . import jmespath as jmespath_


class TestMain:
    def test_ab6bd1c4(self) -> None:
        source = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expected = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
        }
        jmespath_.set_value(source, "d", 4)

        assert source == expected

    def test_cba04a4b(self) -> None:
        source = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expected = {
            "a": {
                "a1": True,
            },
            "b": 2,
            "c": 3,
        }
        jmespath_.set_value(source, "a.a1", True)

        assert source == expected

    def test_65d59f74(self) -> None:
        source = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expected = {
            "d": 4,
        }
        jmespath_.set_value(source, "", expected)

        assert source == expected
