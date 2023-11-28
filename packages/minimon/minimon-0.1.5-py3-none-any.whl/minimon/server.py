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

# pylint: disable=too-many-locals

"""The core stuff"""

import asyncio
import logging
import signal
from collections.abc import Awaitable, Callable, MutableMapping, MutableSequence
from contextlib import suppress
from contextvars import ContextVar
from dataclasses import dataclass

import psutil
from rich.console import Console
from rich.logging import RichHandler
from rich.markup import escape as markup_escape
from rich.style import Style
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult, ScreenStackError
from textual.containers import Horizontal, VerticalScroll
from textual.events import Idle, MouseEvent
from textual.message import Message
from textual.scrollbar import ScrollTo
from textual.widgets import Header, Label, Log, RichLog, Static, Tree
from textual.widgets.tree import TreeNode

from minimon.core import (
    AInsights,
    CheckEvent,
    CheckMetric,
    CheckResult,
    PipeError,
    StrIter,
)
from minimon.logging_utils import setup_introspection_on_signal


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("minimon")


@dataclass
class ViewData:
    "Accumulated data to display in a View"
    checks: MutableMapping[str, CheckResult]
    metrics: MutableMapping[str, CheckMetric]
    events: MutableSequence[CheckEvent]


class Context:
    """A minimon application context - too fuzzy to describe for now"""

    def __init__(self) -> None:
        self.things: MutableMapping[str, AInsights] = {}
        self.log_widgets: MutableMapping[str, Callable[[StrIter, bool], None]] = {}
        self.logger_context: ContextVar[str] = ContextVar("logger_context")

    def add(self, name: str, generator: AInsights) -> None:
        """Registeres a view's generator"""
        self.things[name] = generator

    def ctx_log_fn(self) -> Callable[[StrIter, bool], None]:
        """Returns the UI logging function for the current async context"""

        style_std = Style(color="green")
        style_err = Style(color="red")
        console = Console()

        def dummy_print(lines: StrIter, err: bool) -> None:
            for line in filter(bool, map(str.rstrip, lines)):
                console.print(f":│ {line}", style=(style_err if err else style_std))

        try:
            return self.log_widgets[self.logger_context.get()]
        except LookupError:
            return dummy_print

    def set_current_logger(self, name: str, log_widget: Log) -> None:
        """Configures the logging function for the async context called from"""
        self.logger_context.set(name)
        style_std = Style(color="green")
        style_err = Style(color="red")
        self.log_widgets[name] = lambda lines, err: (
            None
            if log_widget.write_lines(
                ((style_err if err else style_std).render(line) for line in lines)
            )
            else None
        )


class RichLogHandler(RichHandler):
    """Redirects rich.RichHanlder capabilities to a textual.RichLog"""

    def __init__(self, widget: RichLog, error_widget: RichLog):
        super().__init__(show_time=False, show_path=False, markup=True)
        self.widget: RichLog = widget
        self.error_widget: RichLog = error_widget
        self.error_widget.visible = False
        self.widget.styles.width = "100%"
        self.error_widget.styles.width = "0%"

    def emit(self, record: logging.LogRecord) -> None:
        record.args = record.args and tuple(
            markup_escape(arg) if isinstance(arg, str) else arg for arg in record.args
        )
        record.msg = markup_escape(record.msg)
        log_renderable = self.render(
            record=record,
            traceback=None,
            message_renderable=self.render_message(record, self.format(record)),
        )
        self.widget.write(log_renderable)
        if record.levelname not in {"[DD]", "[II]", "[WW]", "DEBUG", "INFO", "WARNING"}:
            if not self.error_widget.visible:
                self.widget.styles.width = "50%"
                self.error_widget.styles.width = "50%"
                self.error_widget.visible = True
            self.error_widget.write(log_renderable)


class LockingRichLog(RichLog):
    """A RichLog which turns off autoscroll when scrolling manually"""

    @on(ScrollTo)
    def on_scroll_to(self, _event: Message) -> None:
        """Mandatory comment"""
        self.auto_scroll = self.is_vertical_scroll_end


class TaskWidget(Static):
    """Generic widget for task visualization"""

    def compose(self) -> ComposeResult:
        yield Tree(label="stuff")
        yield Log(classes="box")


class MiniMoni(App[None]):
    """Terminal monitor for minimon"""

    CSS_PATH = "minimon.css"
    TITLE = "minimon"

    def __init__(self, context: Context, log_level: str) -> None:
        super().__init__()
        self._widget_container = VerticalScroll()
        self._normal_log = LockingRichLog(id="log")
        self._normal_log.border_title = "messages"
        self._error_log = LockingRichLog(id="error_log")
        self._error_log.border_title = "errors"
        self.context = context
        self.setup_logging(log_level)
        self._footer_label = Label(Text.from_markup("nonsense"), id="footer")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self._widget_container
        with Horizontal():
            yield self._normal_log
            yield self._error_log
        yield self._footer_label

    @staticmethod
    async def _handle_monitoring_info(  # pylint: disable=too-many-arguments
        name: str,
        task_fn: AInsights,
        context: Context,
        widget: TaskWidget,
        cleanup: Callable[[], Awaitable[None]],
    ) -> None:
        """Reads from provided generator and updates corresponding widget"""
        try:
            log().info("task %r started", task_fn)
            context.set_current_logger(name, widget.query_one(Log))

            view_data = ViewData(checks={}, metrics={}, events=[])
            tree = widget.query_one(Tree)
            tree.root.expand_all()
            tree.root.allow_expand = False
            tree.show_root = False

            source_nodes: MutableMapping[
                str, tuple[TreeNode[None], MutableMapping[str, TreeNode[None]]]
            ] = {}
            level_icons = {
                "info": "⚪",
                "error": "⭕",
                "warn": "🟠",
                "ok": "🟢",
                "crit": "🔴",
            }

            async for data in task_fn:
                if (source := ".".join(data.source)) not in source_nodes:
                    source_nodes[source] = (
                        tree.root.add(source, allow_expand=False, expand=True),
                        {},
                    )

                source_node, item_nodes = source_nodes[source]

                if isinstance(data.value, PipeError):
                    for child in item_nodes.values():
                        child.remove()
                    source_node.remove_children()
                    item_nodes.clear()
                    source_node.set_label(f"{source} - {data.value}")
                    continue

                insight = data.value
                if isinstance(insight, CheckResult):
                    label = f"{level_icons[insight.level]} - {insight.key} - {insight.message}"
                    if insight.key not in item_nodes:
                        item_nodes[insight.key] = source_node.add(label, allow_expand=False)
                    else:
                        item_nodes[insight.key].set_label(label)
                    view_data.checks[insight.key] = insight
                if isinstance(insight, CheckMetric):
                    view_data.metrics[insight.key] = insight
                if isinstance(insight, CheckEvent):
                    view_data.events.append(insight)
                    label = (
                        f"{level_icons[insight.level]}"
                        f" - {str(insight.timestamp)[:19]} - {insight.message}"
                    )
                    item_nodes[str(insight.timestamp)] = source_node.add(label, allow_expand=False)

        except Exception:  # pylint: disable=broad-except
            log().exception("exception in %r", task_fn)
        finally:
            log().info("task %r terminated", task_fn)
            await cleanup()

    async def create_widget(self, title: str) -> TaskWidget:
        """Creates, configures and returns a TaskWidget"""
        await self._widget_container.mount(widget := TaskWidget())
        widget.border_title = title
        return widget

    async def remove_widget(self, widget: TaskWidget) -> None:
        """Asynchronously removes given @widget"""
        with suppress(ScreenStackError):

            await widget.remove()

    async def add_task(self, name: str, task: AInsights) -> TaskWidget:
        """Registers a new process task to be executed"""
        widget = await self.create_widget(name)
        asyncio.ensure_future(
            self._handle_monitoring_info(
                name,
                task,
                self.context,
                widget,
                lambda: self.remove_widget(widget),
            )
        )
        return widget

    async def state_updater(self) -> None:
        """Continuously write some internal stuff to log"""
        current_process = psutil.Process()
        while True:
            tasks = [
                name
                for t in asyncio.all_tasks()
                if not (name := t.get_name()).startswith("message pump ")
            ]
            self._footer_label.update(
                Text.from_markup(
                    f"PID: {current_process.pid} CPU: {current_process.cpu_percent()}%"
                    f" │ Tasks: {len(tasks)}"
                    f" │ Total CPU: {psutil.cpu_percent()} * {psutil.cpu_count()}%"
                )
            )
            await asyncio.sleep(3)

    def setup_logging(self, level: str) -> None:
        """Setup UI and text only logging"""
        logging.getLogger().handlers = [
            file_handler := logging.FileHandler("minimon.log", encoding=None, delay=False),
            ui_handler := RichLogHandler(self._normal_log, self._error_log),
        ]
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(name)-10s - %(message)s")
        )
        ui_handler.setFormatter(
            logging.Formatter(
                "│ %(asctime)s │ %(posixTID)d [grey53]%(stack)-32s[/] │ [bold white]%(message)s[/]",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        # global
        logging.getLogger().setLevel(logging.WARNING)
        # app
        log().setLevel(logging.DEBUG)
        # ui
        ui_handler.setLevel(getattr(logging, level.split("_")[-1]))
        # file
        file_handler.setLevel(logging.DEBUG)

    async def on_mount(self) -> None:
        """UI entry point"""

        # install_signal_handler(asyncio.get_event_loop(), self.exit)

        asyncio.create_task(self.state_updater(), name="state-updater")

        for name, generator in self.context.things.items():
            await self.add_task(name, generator)

    @on(Message)
    async def on_msg(self, event: Message) -> None:
        """Generic message handler"""
        if isinstance(event, (MouseEvent, Idle)):
            return
        log().info("Event: %s", type(event))


def install_signal_handler(loop: asyncio.AbstractEventLoop, on_signal: Callable[[], None]) -> None:
    """Installs the CTRL+C application termination signal handler"""
    for signal_enum in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(signal_enum, on_signal)


class Singleton(type):
    """Yes, a Singleton"""

    _instances: MutableMapping[type, object] = {}

    def __call__(cls: "Singleton", *args: object, **kwargs: object) -> object:
        """Creates an instance if not available yet, returns it"""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


async def print_state() -> None:
    """Continuously write some internal stuff to log"""
    while True:
        tasks = [
            name
            for t in asyncio.all_tasks()
            if not (name := t.get_name()).startswith("message pump ")
        ]
        log().debug("tasks(%d): %s", len(tasks), tasks)
        await asyncio.sleep(1)


async def async_serve(context: Context, log_level: str = "INFO") -> int:
    """Synchronous entry point"""
    setup_introspection_on_signal()
    asyncio.create_task(print_state(), name="print_state")

    await MiniMoni(context, log_level).run_async()

    log().info("application terminated")

    for task in asyncio.all_tasks():
        log().debug("cancel task '%s'", task.get_name())
        task.cancel()
        with suppress(StopAsyncIteration, asyncio.CancelledError):
            await task

    return 0


def serve(context: Context, log_level: str = "INFO") -> int:
    """Synchronous convenience wrapper"""
    return asyncio.run(async_serve(context, log_level))
