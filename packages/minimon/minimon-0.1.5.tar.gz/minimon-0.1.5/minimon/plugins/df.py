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

"""This is a simple check plugin example around the `df` tool"""

import re
from collections.abc import Callable, Iterable, Sequence
from datetime import datetime
from typing import TypeAlias

from pydantic import BaseModel

from minimon.builder import Host, Insights, Pipeline, StrSeq, process_stdout_lines
from minimon.core import CheckResult

ParsedType: TypeAlias = Sequence[tuple[str, str, float]]


class ParseOptions(BaseModel):
    """Parse options you can provide"""

    mountpoint_opt_in: None | str = None
    mountpoint_opt_out: None | str = "^/dev(/.*)?|/boot/efi|/sys/.*$"


class CheckOptions(BaseModel):
    """Check options you can provide"""


def generate(host: Host) -> Pipeline[StrSeq]:
    """Convenience shortcut for Pipeline(process_output(...))"""
    return Pipeline(process_stdout_lines(host, "df -P", when="10"))


def parse(
    options: None | ParseOptions = None,
) -> Callable[[StrSeq], Iterable[ParsedType]]:
    """
    Filesystem     1K-blocks      Used Available Use% Mounted on
    /dev/dm-0      981723644 814736524 117044544  88% /
    """

    def _parse(lines: StrSeq, options: ParseOptions) -> Iterable[ParsedType]:
        """Mandatory docstring"""
        yield [
            (mpoint, device, use)
            for line in lines[1:]
            for elems in (line.split(),)
            if len(elems) > 5
            for mpoint, device, use in ((elems[5], elems[0], int(elems[4][:-1])),)
            if not options.mountpoint_opt_in or re.match(options.mountpoint_opt_in, mpoint)
            if not options.mountpoint_opt_out or not re.match(options.mountpoint_opt_out, mpoint)
        ]

    return lambda lines: _parse(lines, options or ParseOptions())


def check(
    options: None | CheckOptions = None,
) -> Callable[[ParsedType], Insights]:
    """Returns insights from preprocessed `df` output"""

    def _check(
        mountpoints: ParsedType, _opts: CheckOptions, now: datetime = datetime.now()
    ) -> Insights:
        for mountp, _dev, use in mountpoints:
            yield CheckResult(
                mountp, f"({use}%)", "ok" if use < 80 else "warn" if use < 90 else "crit", now
            )

    return lambda mountpoints: _check(mountpoints, options or CheckOptions())
