"""Top level module cache for dailylog."""

import sys
from datetime import datetime, timezone
from typing import Dict, Optional

from click.core import Context
from wtforglib.files import load_json_file, write_json_file
from wtforglib.kinds import StrAnyDict

from dailylog1.config import Config

CONST_CACHE_VERSION = 1
CONST_HOUR = 86400


class CacheRecord(object):
    """Class representing a cache record."""

    shown: int
    suppressed: int

    def __init__(self, d_obj: Optional[Dict[str, int]] = None) -> None:
        """Class constructor.

        Parameters
        ----------
        d_obj : Dict[str, int], optional
            Cache record object, by default None
        """
        if d_obj is None:
            self.shown = 0
            self.suppressed = 0
            return
        self._from_dict(d_obj)

    def suppress(self, stifle: int) -> bool:
        """Suppress diplay of cache record.

        Parameters
        ----------
        stifle : int
            Suppress if last display is > stifle seconds

        Returns
        -------
        bool
            True if suppressed
        """
        now = int(datetime.utcnow().timestamp())
        if now - self.shown > stifle:
            self.shown = now
            self.suppressed = 0
            return False
        self.suppressed += 1
        return True

    def to_dict(self) -> Dict[str, int]:
        """Convert instance to dict.

        Returns
        -------
        Dict[str, int]
            Instance data as dict
        """
        return {"shown": self.shown, "suppressed": self.suppressed}

    def _from_dict(self, d_obj: Dict[str, int]) -> None:
        """Assign instance data from dict.

        Parameters
        ----------
        d_obj : Dict[str, int]
            Record data
        """
        self.shown = d_obj.get("shown", 0)
        self.suppressed = d_obj.get("suppressed", 0)


class Cache(Config):
    """Class to manage the cache."""

    cache: StrAnyDict

    def __init__(self, ctx: Context):
        """Constructor for cache class."""
        super().__init__(ctx)
        self._load_cache()

    def log_message(self, key: str, message: str, **kwargs) -> bool:
        r"""Log message.

        Parameters
        ----------
        key : str
            unique key for message
        message : str
            the message to log
        \*\*kwargs : dict, optional
            label: str
                Should be one of CRITICAL, ERROR, WARNING, INFO, DEBUG
            suppress: int
                Integer representing number of seconds to suppress screen output
            logfn: str
                this is a string representing a log file other than the default

        Returns
        -------
        bool
            True if record was was displayed
        """
        # default values
        label = "ERROR"
        log_fn = self.default_log()
        stifle = CONST_HOUR
        rtn_val = False
        if kwargs is not None:
            label = kwargs.get("label", label)
            log_fn = kwargs.get("logfn", log_fn)
            stifle = kwargs.get("suppress", stifle)
        record: CacheRecord = self._get_record(key)
        if not record.suppress(stifle):
            sys.stderr.write("{0}: {1}\n".format(label, message))
            rtn_val = True
        Cache.append_daily(label, message, log_fn, record.suppressed)
        self.cache["entries"][key] = record.to_dict()
        self._save_cache()
        return rtn_val

    @staticmethod
    def append_daily(
        label: str,
        message: str,
        log_fn: str,
        s_cnt: Optional[int] = None,
    ) -> None:
        """Append a message to the specified log file.

        Parameters
        ----------
        label : str
            Log level label DEBUG, INFO, WARNING, ERROR ...
        message : str
            Record to log
        log_fn : str
            Path name of log file
        s_cnt : int
            Number of seconds to suppress screen output.
        """
        # WPS323 Found `%` string formatting
        fmt = "%a %b %d %H:%M:%S %p %Z %Y"  # noqa: WPS323
        stamp = datetime.now(timezone.utc).astimezone().strftime(fmt)
        with open(log_fn, "a") as daily_log:
            if s_cnt is None:  # no suppressed count
                daily_log.write("{0} {1}: {2}\n".format(stamp, label, message))
            else:
                daily_log.write(
                    "{0} {1}: {2} [{3}]\n".format(stamp, label, message, s_cnt),
                )
            daily_log.close()

    def _get_record(self, key: str) -> CacheRecord:
        """Get cache record.

        Parameters
        ----------
        key : str
            unique key for record

        Returns
        -------
        CacheRecord
            The record
        """
        entries = self.cache.get("entries", {})
        return CacheRecord(entries.get(key, None))

    def _load_cache(self) -> None:
        """Load case from file it exist otherwise create a cache."""
        cache_path = self.cache_path()
        if cache_path.is_file():
            self.cache = load_json_file(cache_path)
        else:
            self.cache = {}
            self.cache["version"] = CONST_CACHE_VERSION
            self.cache["entries"] = {}
            self._save_cache()

    def _save_cache(self) -> None:
        """Load cacheuration from file."""
        write_json_file(self.cache_path(), self.cache)
