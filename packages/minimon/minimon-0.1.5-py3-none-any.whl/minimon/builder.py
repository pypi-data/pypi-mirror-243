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

"""Provides generic machinery to spawn a bunch of local or remote monitoring processes in a
minimon application context
"""
# pylint: disable=too-few-public-methods,fixme

import argparse
import asyncio
import functools
import logging
import shlex
import sys
import traceback
from asyncio import StreamReader
from asyncio.subprocess import PIPE, create_subprocess_exec
from collections.abc import (
    AsyncIterable,
    AsyncIterator,
    Callable,
    Iterable,
    Mapping,
    Sequence,
)
from contextlib import suppress
from dataclasses import dataclass
from itertools import count
from pathlib import Path
from typing import Any, Type, TypeAlias, TypeVar, cast

import asyncssh
from apparat import Bundler, PipeError, Pipeline, collect_chunks
from pydantic import BaseModel

from minimon.core import (
    AInsights,
    CheckEvent,
    CheckMetric,
    CheckResult,
    Insight,
    Insights,
    PipedValue,
    StrIter,
    StrSeq,
)
from minimon.server import Context, Singleton, async_serve

__all__ = [
    "Monitor",
    "GlobalMonitorContext",
    "Pipeline",
    "PipeError",
    "Host",
    "Hosts",
    "LocalHost",
    "Insight",
    "Insights",
    "AInsights",
    "CheckResult",
    "CheckEvent",
    "CheckMetric",
    "StrSeq",
    "StrIter",
    "view",
    "Bundler",
    "process_output",
    "this_dir",
]


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("minimon")


Args: TypeAlias = argparse.Namespace


def this_dir() -> Path:
    """Returns directory of caller file"""
    # pylint: disable=protected-access
    return Path(traceback.extract_stack(sys._getframe(1))[-1].filename).parent


class GlobalMonitorContext(Context, metaclass=Singleton):
    """A singleton minimon application context"""


@dataclass
class Host:
    """Specification of a remote host with everything needed to establish an SSH connection"""

    name: str
    ip_address: None | str
    ssh_user: None | str
    ssh_key_file: None | Path
    ssh_key_passphrase_cmd: None | str
    ssh_port: None | int
    use_ssh: bool

    def __init__(
        self,
        name: str,
        *,
        ip_address: None | str = None,
        ssh_user: None | str = None,
        ssh_key_file: None | str | Path = None,
        ssh_key_passphrase_cmd: None | str = None,
        ssh_port: None | int = None,
        use_ssh: bool = True,
    ):
        self.name = name
        self.ip_address = ip_address or name
        self.ssh_user = ssh_user
        self.ssh_key_file = Path(ssh_key_file).expanduser() if ssh_key_file else None
        self.ssh_key_passphrase_cmd = ssh_key_passphrase_cmd
        self.ssh_port = ssh_port
        self.use_ssh = use_ssh

    def __str__(self) -> str:
        user_str = f"{self.ssh_user}@" if self.ssh_user else ""
        return f"{user_str}{self.ip_address}-{'ssh' if self.use_ssh else 'local'}"


Hosts: TypeAlias = Sequence[Host]


class LocalHost(Host):
    """Convenience wrapper for Host"""

    def __init__(self) -> None:
        super().__init__("localhost", use_ssh=False)


class RemoteConnectionError(RuntimeError):
    """Raised when something's going wrong with a SSH connection"""


ViewArg1T = TypeVar("ViewArg1T")  # pylint: disable=invalid-name
ViewArg2T = TypeVar("ViewArg2T")  # pylint: disable=invalid-name

Call0: TypeAlias = Callable[[], AInsights]
Call1: TypeAlias = Callable[[ViewArg1T], AInsights]
Call2: TypeAlias = Callable[[ViewArg1T, ViewArg2T], AInsights]


def view(
    arg1: None | tuple[str, Iterable[ViewArg1T]] = None,
    arg2: None | tuple[str, Iterable[ViewArg2T]] = None,
) -> Callable[[Call0 | Call1[ViewArg1T] | Call2[ViewArg1T, ViewArg2T]], None]:
    """A decorator generating a minimon view for each value in @arg_values"""

    def deco_wrapper(afunc: Call0 | Call1[ViewArg1T] | Call2[ViewArg1T, ViewArg2T]) -> None:
        @functools.wraps(afunc)
        async def wrapper_view(**kwargs: ViewArg1T | ViewArg2T) -> AInsights:
            try:
                async for element in afunc(**kwargs):  # type: ignore[call-arg]
                    yield element
            except StopAsyncIteration:
                log().info("StopAsyncIteration in %s", afunc.__name__)
                return
            except Exception:  # pylint: disable=broad-except
                log().exception("Unhandled exception in view generator:")
                await asyncio.sleep(5)  # todo: handle elsewhere

        fn_name = afunc.__name__
        if arg2 is not None:
            assert arg1 is not None
            for arg1_value in arg1[1]:
                for arg2_value in arg2[1]:
                    GlobalMonitorContext().add(
                        f"{fn_name}-{arg1_value}-{arg2_value}",
                        wrapper_view(
                            **cast(
                                Mapping[str, ViewArg1T | ViewArg2T],
                                {arg1[0]: arg1_value, arg2[0]: arg2_value},
                            )
                        ),
                    )

        elif arg1 is not None:
            for arg1_value in arg1[1]:
                GlobalMonitorContext().add(
                    f"{fn_name}-{arg1_value}", wrapper_view(**{arg1[0]: arg1_value})
                )
        else:
            GlobalMonitorContext().add(f"{fn_name}", wrapper_view())

    return deco_wrapper


class HostConnection:
    """An SSH connection to a given @host"""

    def __init__(self, host: Host, log_fn: Callable[[StrIter, bool], None]) -> None:
        self.host_info = host
        self.log_fn = log_fn
        self.ssh_connection: None | asyncssh.SSHClientConnection = None
        self.current_connection_error: None | RemoteConnectionError = None
        self._connection_established = asyncio.Event()

    async def __aenter__(self) -> "HostConnection":
        if self.host_info.use_ssh:
            asyncio.create_task(self._establish_connection(), name="establish_connection")
        return self

    async def __aexit__(self, *args: object) -> None:
        log().debug("close connection")
        if self.ssh_connection:
            self.ssh_connection.close()

    async def _establish_connection(self) -> None:

        remote_str = (
            f"{f'{self.host_info.ssh_user}@' if self.host_info.ssh_user else ''}"
            f"{self.host_info.ip_address}"
            f"{f':{self.host_info.ssh_port}' if self.host_info.ssh_port else ''}"
        )
        log().info("connect to remote %s", remote_str)

        while not self.ssh_connection:
            try:
                self.ssh_connection = await asyncssh.connect(
                    self.host_info.ip_address,
                    **{
                        key: value
                        for key, value in (
                            ("port", self.host_info.ssh_port),
                            ("username", self.host_info.ssh_user),
                            ("client_keys", self.host_info.ssh_key_file),
                        )
                        if value is not None
                    },
                    keepalive_interval=2,
                    keepalive_count_max=2,
                    known_hosts=None,
                )
                self.current_connection_error = None
                self._connection_established.set()
                break

            except asyncssh.PermissionDenied:
                self.current_connection_error = RemoteConnectionError(
                    f"PermissionDenied({remote_str})"
                )
            except asyncssh.HostKeyNotVerifiable as exc:
                self.current_connection_error = RemoteConnectionError(
                    f"Cannot connect to {self.host_info.name}: {exc}"
                )
            except OSError as exc:
                self.current_connection_error = RemoteConnectionError(
                    f"OSError({remote_str}): {exc}"
                )
            log().warning("Could not connect (%s) - retry..", self.current_connection_error)
            self._connection_established.set()
            await asyncio.sleep(3)

    @staticmethod
    def clean_lines(
        raw_lines: Iterable[bytes],
        log_fn: Callable[[StrIter, bool], None],
        err: bool = False,
    ) -> StrSeq:
        """Sanatize and log a bytes line"""
        lines = [
            (raw_line.decode() if isinstance(raw_line, bytes) else raw_line).strip("\n")
            for raw_line in raw_lines
        ]
        log_fn(lines, err)
        return lines

    async def listen(self, stream: StreamReader | asyncssh.SSHReader[Any], *, err: bool) -> StrSeq:
        """Creates a sanatized list of strings from something iterable and logs on the go"""
        return [
            line
            async for raw_lines in collect_chunks(aiter(stream), min_interval=3, bucket_size=5)
            for line in self.clean_lines(raw_lines, self.log_fn, err=err)
        ]

    async def handle_line(
        self, stream: StreamReader | asyncssh.SSHReader[Any], *, err: bool
    ) -> AsyncIterator[str]:
        """Creates a sanatized list of strings from something iterable and logs on the go"""
        async for raw_lines in collect_chunks(aiter(stream), min_interval=3, bucket_size=5):
            for line in self.clean_lines(raw_lines, self.log_fn, err=err):
                yield line

    async def _execute_ssh(
        self, command: str, single_line: bool
    ) -> AsyncIterator[RemoteConnectionError | StrSeq | str]:
        """Remote/SSH implementation of execute()"""

        while True:
            await self._connection_established.wait()
            assert bool(self.current_connection_error) != bool(self.ssh_connection)
            if self.ssh_connection:
                break
            yield RemoteConnectionError(f"{self.current_connection_error}")
            self._connection_established.clear()

        try:
            ssh_process = await self.ssh_connection.create_process(command)
        except asyncssh.ChannelOpenError as exc:
            yield RemoteConnectionError(f"{exc}")
            return

        assert ssh_process.stdout and ssh_process.stderr

        try:
            log().debug("run command via SSH..")
            if single_line:
                process_task = asyncio.ensure_future(
                    asyncio.gather(
                        self.listen(ssh_process.stderr, err=True),
                        asyncio.ensure_future(ssh_process.wait()),
                    )
                )
                try:
                    async for line in self.handle_line(ssh_process.stdout, err=False):
                        yield line
                finally:
                    # todo: handle _stderr, completed.returncode
                    _stderr, _completed = await process_task
            else:
                stdout, _stderr, completed = await asyncio.gather(
                    self.listen(ssh_process.stdout, err=False),
                    self.listen(ssh_process.stderr, err=True),
                    asyncio.ensure_future(ssh_process.wait()),
                )
                assert completed.returncode is not None
                # todo: handle _stderr, completed.returncode
                yield stdout
        except asyncssh.ConnectionLost as exc:
            yield RemoteConnectionError(f"{exc}")
            asyncio.create_task(self._establish_connection(), name="establish_connection")
            if self.ssh_connection:
                self.ssh_connection.close()
                self.ssh_connection = None
            self._connection_established.clear()

        finally:
            log().debug("terminate() remote process '%s'..", command)
            ssh_process.terminate()
        return

    async def _execute_locally(
        self, command: str, single_line: bool
    ) -> AsyncIterator[RemoteConnectionError | StrSeq | str]:
        """Local implementation of execute()"""
        log().debug("run command '%s' locally..", command)
        process = await create_subprocess_exec(*shlex.split(command), stdout=PIPE, stderr=PIPE)
        assert process.stdout and process.stderr
        try:
            if single_line:
                process_task = asyncio.ensure_future(
                    asyncio.gather(
                        self.listen(process.stderr, err=True),
                        process.wait(),
                    )
                )
                try:
                    async for line in self.handle_line(process.stdout, err=False):
                        yield line
                finally:
                    # todo: handle _stderr, _return_code
                    _stderr, _return_code = await process_task
            else:
                stdout, _stderr, _return_code = await asyncio.gather(
                    self.listen(process.stdout, err=False),
                    self.listen(process.stderr, err=True),
                    process.wait(),
                )
                # todo: handle _stderr, _return_code
                yield stdout
        finally:
            log().debug("terminate() local process '%s'..", command)
            with suppress(ProcessLookupError):
                process.terminate()

    async def execute(
        self, command: str, single_line: bool = False
    ) -> AsyncIterator[RemoteConnectionError | StrSeq | str]:
        """Executes @command via ssh connection if specified else locally"""
        if self.host_info.use_ssh:
            async for element in self._execute_ssh(command, single_line):
                yield element
        else:
            async for element in self._execute_locally(command, single_line):
                yield element


async def process_output(
    host: Host,
    command: str,
    *,
    when: None | str = None,
    single_line: bool = False,
) -> AsyncIterable[PipedValue[StrSeq | str]]:
    """Executes a process defined by @command on @host in a manner specified by @when"""
    iterations = None
    interval = float(when) if when is not None else None

    async with HostConnection(host, GlobalMonitorContext().ctx_log_fn()) as connection:
        for iteration in count():
            if iterations is not None and iteration >= iterations:
                break

            log().info("start task %r: %d", command, iteration)
            try:
                # a connection can yield different sorts of results:
                # - line by line
                # - stdout, stderr and return code
                # - a PipeError
                # based on connection and execution types
                async for result in connection.execute(command, single_line=single_line):
                    yield PipedValue(
                        "process",
                        PipeError(f"{result}")
                        if isinstance(result, RemoteConnectionError)
                        else result,
                    )
            except Exception:  # pylint: disable=broad-except
                log().exception("Executing command %s resulted in unhandled exception", command)
                raise

            if interval is not None:
                await asyncio.sleep(interval)


def process_stdout_lines(
    host: Host, command: str, *, when: None | str = None
) -> AsyncIterable[PipedValue[StrSeq]]:
    """Wraps process_output for typing convenience"""
    return cast(
        AsyncIterable[PipedValue[StrSeq]],
        process_output(host, command, when=when, single_line=False),
    )


def process_stdout_single_line(
    host: Host, command: str, *, when: None | str = None
) -> AsyncIterable[PipedValue[str]]:
    """Wraps process_output for typing convenience"""
    return cast(
        AsyncIterable[PipedValue[str]],
        process_output(host, command, when=when, single_line=True),
    )


def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["ALL_DEBUG", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
        help="Sets the logging level - ALL_DEBUG sets all other loggers to DEBUG, too",
        type=str.upper,
    )

    return parser.parse_args()


def in_doctest() -> bool:
    """Self-introspect to find out if we're in the Matrix"""
    if "_pytest.doctest" in sys.modules:
        return True
    ##
    if hasattr(sys.modules["__main__"], "_SpoofOut"):
        return True
    ##
    if sys.modules["__main__"].__dict__.get("__file__", "").endswith("/pytest"):
        return True
    ##
    return False


class Monitor:
    """Top level application context, instantiating the monitoring application"""

    def __init__(self, name: str, log_level: str = "INFO") -> None:
        if not in_doctest():
            args = parse_args()
            self.name = name
            self.log_level = args.log_level or log_level or "INFO"

    def __enter__(self) -> "Monitor":
        return self

    def __exit__(self, *args: object) -> None:
        if in_doctest():
            return

        if sys.exc_info() != (None, None, None):
            raise

        asyncio.run(async_serve(GlobalMonitorContext(), self.log_level))


HostConfigT = TypeVar("HostConfigT")


class ConfigBase(BaseModel):
    """Individual Host configuration"""

    host: Host

    def __str__(self) -> str:
        return str(self.host)

    @classmethod
    def create_multiple(cls: Type[HostConfigT], configs: Sequence[Any]) -> Sequence[HostConfigT]:
        """Convenience function for creating a vector of BaseHostConfig"""
        return list(map(cls.model_validate, configs))  # type: ignore[attr-defined]
