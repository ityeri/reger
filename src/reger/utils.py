"""
Copyright (c) 2026 ityeri

Original Copyright (c) 2015-present Rapptz
"""
import logging
import os
import sys
from typing import Any

from reger.colour_formater import ColourFormatter


def is_docker() -> bool:
    path = '/proc/self/cgroup'
    return os.path.exists('/.dockerenv') or (os.path.isfile(path) and any('docker' in line for line in open(path)))

def is_stream_supports_colour(stream: Any) -> bool:
    is_a_tty = hasattr(stream, 'isatty') and stream.isatty()

    # Pycharm and Vscode support colour in their inbuilt editors
    if 'PYCHARM_HOSTED' in os.environ or os.environ.get('TERM_PROGRAM') == 'vscode':
        return is_a_tty

    if sys.platform != 'win32':
        # Docker does not consistently have a tty attached to it
        return is_a_tty or is_docker()

    # ANSICON checks for things like ConEmu
    # WT_SESSION checks if this is Windows Terminal
    return is_a_tty and ('ANSICON' in os.environ or 'WT_SESSION' in os.environ)


def setup_logging(
    *,
    logger: logging.Logger = None,
    handler: logging.Handler = None,
    formatter: logging.Formatter = None,
    level: int = None,
) -> None:
    """A helper function to setup logging.

    This is superficially similar to :func:`logging.basicConfig` but
    uses different defaults and a colour formatter if the stream can
    display colour.

    This is used by the :class:`~discord.Client` to set up logging
    if ``log_handler`` is not ``None``.

    .. versionadded:: 2.0

    Parameters
    -----------
    logger: :class:`logging.Logger`
        The target handler to setup.
        If not provided then it defaults using root logger.
    handler: :class:`logging.Handler`
        The log handler to use for the library's logger.

        The default log handler if not provided is :class:`logging.StreamHandler`.
    formatter: :class:`logging.Formatter`
        The formatter to use with the given log handler. If not provided then it
        defaults to a colour based logging formatter (if available). If colour
        is not available then a simple logging formatter is provided.
    level: :class:`int`
        The default log level for the library's logger. Defaults to ``logging.INFO``.
    """

    if level is None:
        level = logging.INFO

    if handler is None:
        handler = logging.StreamHandler()

    if formatter is None:
        if isinstance(handler, logging.StreamHandler) and is_stream_supports_colour(handler.stream):
            formatter = ColourFormatter()
        else:
            dt_fmt = '%Y-%m-%d %H:%M:%S'
            formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

    if logger is None:
        logger = logging.getLogger()

    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)
