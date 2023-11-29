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

""" Some little helper functions for checks
"""
from collections.abc import Callable, Iterable, Sequence
from datetime import datetime
from typing import TypeAlias

from pydantic import BaseModel

from minimon.builder import Host, Insights, Pipeline, StrSeq, process_stdout_lines
from minimon.core import CheckResult

ParsedType: TypeAlias = Sequence[tuple[str, float, float, str]]


class ParseOptions(BaseModel):
    """Parse options you can provide"""


class CheckOptions(BaseModel):
    """Check options you can provide"""


def generate(host: Host) -> Pipeline[StrSeq]:
    """Convenience shortcut for Pipeline(process_output(...))"""
    return Pipeline(process_stdout_lines(host, "ps ww", when="10"))


def parse(
    options: None | ParseOptions = None,
) -> Callable[[StrSeq], Iterable[ParsedType]]:
    """
    USER  PID %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND
    root    1  0.0  0.0 173724  9996 ?   Ss   Aug13   0:04 /usr/lib/systemd rhgb --deserialize 31
    """

    def _parse(lines: StrSeq, _opts: ParseOptions) -> Iterable[ParsedType]:
        yield [
            (user, cpu, mem, cmd)
            for line in lines[1:]
            for elems in (line.split(maxsplit=10),)
            if len(elems) > 10
            for user, cpu, mem, cmd in ((elems[0], float(elems[2]), float(elems[3]), elems[10]),)
        ]

    return lambda lines: _parse(lines, options or ParseOptions())


def check(
    options: None | CheckOptions = None,
) -> Callable[[ParsedType], Insights]:
    """Returns insights from preprocessed `ps` output"""

    def _check(
        processes: ParsedType, _opts: CheckOptions, now: datetime = datetime.now()
    ) -> Insights:
        for user, cpu, mem, cmd in processes:
            yield CheckResult(
                "excessive",
                f"{user} {cpu} {mem} {cmd.split(maxsplit=1)[0]}",
                "info" if cpu < 20 else "warn",
                now,
            )

    return lambda processes: _check(processes, options or CheckOptions())
