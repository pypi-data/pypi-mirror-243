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
import re
from collections.abc import Callable, Iterable
from datetime import datetime
from typing import TypeAlias

from pydantic import BaseModel

from minimon.builder import Host, Insights, Pipeline, process_stdout_single_line
from minimon.core import CheckEvent


class ParseOptions(BaseModel):
    """Parse options you can provide"""


class CheckOptions(BaseModel):
    """Check options you can provide"""


ParsedType: TypeAlias = tuple[datetime, str, str]


def generate(host: Host) -> Pipeline[str]:
    """Convenience shortcut for Pipeline(process_output(...))"""
    return Pipeline(process_stdout_single_line(host, "dmesg --follow --time-format iso", when="10"))


def parse(
    options: None | ParseOptions = None,
) -> Callable[[str], Iterable[ParsedType]]:
    """Extract usable data from dmesg lines
    >>> for parsed in parse()('2023-11-03T20:47:39,598551+01:00 PM: suspend exit'):
    ...     print(" ".join(map(str, parsed)))
    2023-11-03 20:47:39.598551+01:00 PM: suspend exit
    >>> for parsed in parse()('2023-11-03T20:47:39,694201+01:00 iwlwifi 0000:00:14.3: WRT: Invalid'
    ...         ' buffer destination'):
    ...     print(" ".join(map(str, parsed)))
    2023-11-03 20:47:39.694201+01:00 iwlwifi 0000:00:14.3: WRT: Invalid buffer destination
    """

    def _parse(raw_line: str, _opts: ParseOptions) -> Iterable[ParsedType]:
        # we don't need trailing spaces or empty lines
        if not (line := raw_line.rstrip()):
            return
        # sometimes a line resumes the prior line without a timestamp - for now we ignore it
        if line[:4] == "    ":
            return
        ts_raw, first, *rest = line.split(" ", maxsplit=2)
        yield datetime.fromisoformat(ts_raw), first, " ".join(rest)

    return lambda line: _parse(line, options or ParseOptions())


def check(
    options: None | CheckOptions = None,
) -> Callable[[ParsedType], Insights]:
    """Yields insights from preprocessed incoming `dmesg` lines"""

    def _check(message: ParsedType, _opts: CheckOptions) -> Insights:
        timestamp, source, text = message
        if match := re.match(".*(error|warning|failed).*", text, flags=re.IGNORECASE):
            mgs_type = match.group(1).lower()
            yield CheckEvent(
                "dmesg",
                f"[{source}] {text}",
                level="warn" if mgs_type == "warning" else "crit",
                timestamp=timestamp,
            )

    return lambda message: _check(message, options or CheckOptions())
