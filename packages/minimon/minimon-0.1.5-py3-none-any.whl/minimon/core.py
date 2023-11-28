#!/usr/bin/env python3
#            _       _
#  _ __ ___ (_)_ __ (_)_ __ ___   ___  _ __
# | '_ ` _ \| | '_ \| | '_ ` _ \ / _ \| '_ \
# | | | | | | | | | | | | | | | | (_) | | | |
# |_| |_| |_|_|_| |_|_|_| |_| |_|\___/|_| |_|
#
# minimon - a minimal monitor
# Copyright (C) 2023 - Frans Fürst
#
# minimon is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# minimon is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for machine learning. If you're using any content of this
# repository to train any sort of machine learned model (e.g. LLMs), you agree to make the whole
# model trained with this repository and all data needed to train (i.e. reproduce) the model
# publicly and freely available (i.e. free of charge and with no obligation to register to any
# service) and make sure to inform the author (me, frans.fuerst@protonmail.com) via email how to
# get and use that model and any sources needed to train it.

# pylint: disable=too-few-public-methods

"""The core stuff"""

from collections.abc import AsyncIterator, Iterable
from datetime import datetime
from typing import TypeAlias

from apparat import PipedValue, PipeError, Pipeline

# Don't use `Sequence[str]` since `str` is an instance of `Sequence[str]`, see
# - https://stackoverflow.com/questions/44912374
# - https://github.com/python/typing/issues/256
# - https://github.com/python/mypy/issues/1965
StrSeq: TypeAlias = list[str] | tuple[str]
# same here, but I don't have a solution yet
StrIter: TypeAlias = Iterable[str]


__all__ = [
    "Pipeline",
    "PipeError",
    "PipedValue",
    "Insight",
    "Insights",
    "AInsights",
    "StrSeq",
    "StrIter",
    "CheckResult",
    "CheckEvent",
    "CheckMetric",
]


class Insight:
    """A named check result with severity"""

    key: str
    timestamp: None | datetime

    def __init__(self, key: str, timestamp: None | datetime):
        self.key = key
        self.timestamp = timestamp


class CheckResult(Insight):
    """A named check result with severity"""

    level: str
    message: str

    def __init__(
        self, key: str, message: str, level: str = "info", timestamp: None | datetime = None
    ):
        super().__init__(key, timestamp)
        self.level = level
        self.message = message

    def __str__(self) -> str:
        return f"CheckResult(key={self.key!r}, level={self.level}, message={self.message!r})"


class CheckEvent(Insight):
    """Something that happend with severity"""

    level: str
    message: str

    def __init__(
        self, key: str, message: str, level: str = "info", timestamp: None | datetime = None
    ):
        super().__init__(key, timestamp)
        self.level = level
        self.message = message

    def __str__(self) -> str:
        return f"CheckEvent(key={self.key!r}, level={self.level}, message={self.message!r})"


class CheckMetric(Insight):
    """A named key and value"""

    value: float

    def __init__(self, key: str, value: float, timestamp: None | datetime = None):
        super().__init__(key, timestamp)
        self.value = value

    def __str__(self) -> str:
        return f"CheckMetric(key={self.key!r}, value={self.value!r})"


Insights: TypeAlias = Iterable[Insight]
AInsights: TypeAlias = AsyncIterator[PipedValue[Insight]]
