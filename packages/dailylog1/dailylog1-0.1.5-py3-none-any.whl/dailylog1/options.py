"""Top level module options for dailylog."""

from pathlib import Path

from click.core import Context
from wtforglib.files import ensure_directory


class Options(object):
    """Class to manage the options."""

    debug: int
    test: bool
    verbose: int
    cache_fn: str
    config_fn: str

    def __init__(self, ctx: Context) -> None:
        """Constructor for cache class.

        Args:
            ctx (Context): dictionary of click options

        Raises:
            ValueError: when config is an empty string
            ValueError: when config is not an absolute path
        """
        self.debug = int(ctx.obj.get("debug", 0))
        self.test = bool(ctx.obj.get("test", False))
        self.verbose = int(ctx.obj.get("verbose", 0))

        key = "cache"
        fn = str(ctx.obj.get(key, ""))
        if not fn:
            path = Path.home() / ".cache"
            ensure_directory(path)
            fn = str(path / "dailylog.json")
        self.cache_fn = Options.validate_fn_absolute(key, fn)
        key = "config"
        fn = str(ctx.obj.get(key, ""))
        if not fn:
            path = Path.home() / ".config"
            ensure_directory(path)
            fn = str(path / "dailylog.yaml")
        self.config_fn = Options.validate_fn_absolute(key, fn)

    def is_debug(self) -> bool:
        """Return True if debug option is greater than 0."""
        return self.debug > 0

    def is_test(self) -> bool:
        """Return True if test option is greater than 0."""
        return self.test

    def is_verbose(self) -> bool:
        """Return True if verbose option is greater than 0."""
        return self.verbose > 0

    def config_path(self) -> Path:
        """Return the config file path."""
        return Path(self.config_fn)

    def cache_path(self) -> Path:
        """Return the cache file path."""
        return Path(self.cache_fn)

    @staticmethod
    def validate_fn_absolute(file_key: str, file_name: str) -> str:
        """Validate an absolute file name/path.

        Args:
            file_key (str): key name of file "config | cache"
            file_name (str): path name of file to validate

        Raises:
            ValueError: when file_name is empty string
            ValueError: when file_name is not absolute

        Returns:
            str: validate file name/path as a string
        """
        if file_name == "":
            raise ValueError("{0} path name cannot be empty".format(file_key))
        path = Path(file_name)
        if not path.is_absolute():
            raise ValueError("{0} path name must be absolute".format(file_key))
        return str(path)
