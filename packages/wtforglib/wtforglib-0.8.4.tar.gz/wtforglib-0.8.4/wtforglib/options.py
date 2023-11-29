"""Top-level module for Wtforg Library."""

from typing import Dict, Optional, Union

from wtforglib.scribe import LOG_LEVELS, Scribe

OptionsDict = Dict[str, Union[str, int, bool]]

OPTIONS_DEBUG = "debug"
OPTIONS_TEST = "test"
OPTIONS_VERBOSE = "verbose"


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


def basic_options(
    debug: Union[bool, int],
    test: bool,
    verbose: Union[bool, int],
) -> OptionsDict:
    """Return a dictionary of basic options.

    Parameters
    ----------
    debug : Union[bool, int]
        Sets debug: int in the returned dictionary
    test : bool
        Sets test: bool in the returned dictionary
    verbose : Union[bool, int]
        Sets verbose: int in the returned dictionary

    Returns
    -------
    OptionsDict
        Options dictionary
    """
    od: OptionsDict = {}
    od["debug"] = int(debug) if isinstance(debug, bool) else debug
    od["test"] = test
    od["verbose"] = int(verbose) if isinstance(verbose, bool) else verbose
    return od


class Options(object):  # noqa: WPS214
    """A class to handle Options."""

    options: OptionsDict
    scribe: Optional[Scribe]

    def __init__(self, opts: Optional[OptionsDict] = None) -> None:
        """Options constructor.

        Class to manage options for the module.

        Parameters
        ----------
        opts : OptionsDict Optional
            Options to merge with defaults
        """
        self.options = {OPTIONS_DEBUG: 0, OPTIONS_VERBOSE: 0, OPTIONS_TEST: False}
        self.errors = 0
        self.scribe = None
        if opts is not None:  # pragma no cover ???
            self.options.update(opts)
        if int(self.options[OPTIONS_DEBUG]) > 1:
            print(  # noqa: WPS421
                "created instance of class {0}".format(self.__class__.__name__),
            )

    def isdebug(self) -> bool:
        """Returns True if debug > 0."""
        return int(self.options[OPTIONS_DEBUG]) > 0

    def isverbose(self) -> bool:
        """Returns True if verbose > 0."""
        return int(self.options[OPTIONS_VERBOSE]) > 0

    def isnoop(self) -> bool:
        """Returns True if noop."""
        return bool(self.options.get("noop", False))

    def isforce(self) -> bool:
        """Returns True if noop."""
        return bool(self.options.get("force", False))

    def istest(self) -> bool:
        """Returns value of test flag."""
        return bool(self.options[OPTIONS_TEST])

    def debug(self, message: str, level: int = 1) -> None:
        """Utility debug method."""
        dl: int = int(self.options[OPTIONS_DEBUG])
        if self.options[OPTIONS_TEST] or dl >= level:  # pragma no branch
            self._dtrace(message)

    def verbose(self, message: str, level: int = 1) -> None:
        """Utility verbose method."""
        vl: int = int(self.options[OPTIONS_VERBOSE])
        if self.options[OPTIONS_TEST] or vl >= level:  # pragma no cover ???
            self._itrace(message)

    def info(self, message: str) -> None:  # noqa: WPS110
        """Utility trace info method."""
        if self.scribe is None:
            print("INFO: {0}".format(message))
        else:
            self.scribe.logger.info(message)

    def warning(self, message: str) -> None:
        """Utility trace warning method."""
        if self.scribe is None:
            print("WARNING: {0}".format(message))
        else:
            self.scribe.logger.warning(message)

    def warn(self, message: str) -> None:
        """Utility trace warn method."""
        self.warning(message)

    def error(self, message: str) -> None:
        """Utility trace error method."""
        if self.scribe is None:
            print("ERROR: {0}".format(message))
        else:
            self.scribe.logger.error(message)
        self.errors += 1

    def _dtrace(self, message: str) -> None:
        """Utility debug trace method."""
        if self.scribe is None:
            print("DEBUG: {0}".format(message))
        else:
            self.scribe.logger.debug(message)

    def _itrace(self, message: str) -> None:
        """Utility info trace method."""
        if self.scribe is None:
            print("INFO: {0}".format(message))
        else:
            self.scribe.logger.info(message)
