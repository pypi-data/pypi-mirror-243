# dailylog

[![Build Status](https://github.com/wtfo-guru/Dailyloglinux/workflows/Dailylog/badge.svg?branch=main&event=push)](https://github.com/wtfo-guru/dailylog/actions?query=workflow%3ADailyloglinux)
[![codecov](https://codecov.io/gh/wtfo-guru/dailylog/branch/main/graph/badge.svg)](https://codecov.io/gh/wtfo-guru/dailylog)
[![Python Version](https://img.shields.io/pypi/pyversions/dailylog1.svg)](https://pypi.org/project/dailylog1/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## Overview

I have many scripts run by cron and report errors via cron's email. This is great until
one of the scripts that runs frequently starts failing. Rather than waking to a full
mailbox, using this tool will throttled specific errors to a log and only show the error
every 24 hours by default. The time can be adjusted by passing a parameter.

## Installation

Check out this repo and cd into the project directory and run:

```bash

pip install dailylog1

```

## Usage

```bash
dailylog --help
Usage: dailylog [OPTIONS] COMMAND [ARGS]...

  Entry point for click script.

Options:
  -C, --cache TEXT        specify alternate cache file (default ~/.cache/dailylog.json)
  -c, --config TEXT       specify alternate config file (default ~/.config/dailylog.yaml)
  -d, --debug             increment debug level
  -t, --test / --no-test  specify test mode
  -v, --verbose           increment verbosity level
  -V, --version           show version and exit
  -h, --help              Show this message and exit.

Commands:
  log              Log an error.
  set-default-log  Set a new default log.
```

```bash
dailylog log --help
Usage: dailylog log [OPTIONS]

  Log a message.

Options:
  -k TEXT     Specify key  [required]
  -m TEXT     Specify message  [required]
  -s INTEGER  Specify seconds to suppress (default 86400 [one day])
  -l INTEGER  Specify one of logging levels (default: logging.ERROR)
  -f TEXT     Specify alternate log file
  -h, --help  Show this message and exit.
```

```bash
dailylog set-default-log --help
Usage: dailylog set-default-log [OPTIONS] LOG_FN

  Set a new default log.

Options:
  -h, --help  Show this message and exit.
```

## Documentation

- [Stable](https://dailylog1.readthedocs.io/en/stable)

- [Latest](https://dailylog1.readthedocs.io/en/latest)

## License

[MIT](https://github.com/wtfo-guru/dailylog/blob/main/LICENSE)
