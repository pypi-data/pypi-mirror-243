"""Top-level module cli for dailylog."""

import logging
import sys
from types import MappingProxyType
from typing import AnyStr, NoReturn, Optional

import click
from click.core import Context

from dailylog1.cache import CONST_HOUR, Cache
from dailylog1.config import Config
from dailylog1.version import VERSION

CONTEXT_SETTINGS = MappingProxyType({"help_option_names": ["-h", "--help"]})
LOG_LEVELS = MappingProxyType(
    {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    },
)


def log_level_name(level: int, default: str = "info") -> str:
    """Return logger level name.

    Parameters
    ----------
    level : int
        Level number
    default : str, optional
        Default if not matched, by default "info"

    Returns
    -------
    str
        Level name
    """
    for key, valor in LOG_LEVELS.items():
        if level == valor:
            return key
    return default


def print_version(ctx: Context, _aparam: AnyStr, avalue: AnyStr) -> None:
    """Print package version and exits.

    Parameters
    ----------
    ctx : Context
        click context object
    _aparam : AnyStr
        dunno
    avalue : AnyStr
        dunno
    """
    if not avalue or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.command()
@click.option("key", "-k", type=str, required=True, help="Specify key")
@click.option("message", "-m", type=str, required=True, help="Specify message")
@click.option(
    "suppress",
    "-s",
    default=CONST_HOUR,
    help="Specify seconds to suppress (default 86400 [one day])",
)
@click.option(
    "level",
    "-l",
    default=logging.ERROR,
    help="Specify one of logging levels (default: logging.ERROR)",
)
@click.option(
    "log_fn",
    "-f",
    type=str,
    required=False,
    help="Specify alternate log file",
)
@click.pass_context
def log(
    ctx: Context,
    key: str,
    message: str,
    suppress: int,
    level: int,
    log_fn: Optional[str],
) -> NoReturn:
    """Log a message."""
    cache = Cache(ctx)
    if log_fn is None:
        log_fn = cache.default_log()
    cache.log_message(
        key,
        message,
        label=log_level_name(level, "ERROR"),
        suppress=suppress,
        logfn=log_fn,
    )
    sys.exit(0)


@click.command()
@click.argument("log_fn", type=str, required=True, nargs=1)
@click.pass_context
def set_default_log(ctx: Context, log_fn: str) -> NoReturn:
    """Set a new default log."""
    config = Config(ctx)
    config.set_default_log(log_fn)
    if config.is_test():
        # For coverage purposes
        config.is_verbose()
    sys.exit(0)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-C",
    "--cache",
    required=False,
    type=str,
    help="specify alternate cache file (default ~/.cache/dailylog.json)",
)
@click.option(
    "-c",
    "--config",
    required=False,
    type=str,
    help="specify alternate config file (default ~/.config/dailylog.yaml)",
)
@click.option("-d", "--debug", count=True, default=0, help="increment debug level")
@click.option("-t", "--test/--no-test", default=False, help="specify test mode")
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="increment verbosity level",
)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    expose_value=False,
    callback=print_version,
    is_eager=True,
    help="show version and exit",
)
@click.pass_context
def main(ctx, cache, config, debug, test, verbose):
    """Entry point for click script."""
    ctx.ensure_object(dict)
    if cache is None:
        cache = ""
    if config is None:
        config = ""
    ctx.obj["debug"] = debug
    ctx.obj["test"] = test
    ctx.obj["verbose"] = verbose
    ctx.obj["cache"] = cache
    ctx.obj["config"] = config


main.add_command(log)
main.add_command(set_default_log)

if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma no cover
# vim:ft=py noqa: E800
