"""Log scanning events."""

import logging
import sys

# FORMAT ######################################################################

MESSAGE_PATTERN = '[{version}{{levelname}}] {{message}}'

def setup_log_format(pattern: str=MESSAGE_PATTERN, version: str='') -> str:
    """Return the log format string with the common informations filled."""
    __version = version + ' - ' if version else ''
    return pattern.format(version=__version)

# LOGGING #####################################################################

def setup_logger(level: int=logging.INFO, version: str='', pattern: str=MESSAGE_PATTERN) -> None:
    """Configure the default log objects for a specific bot."""
    __pattern = setup_log_format(pattern=pattern, version=version)
    __formatter = logging.Formatter(__pattern, style='{')

    __handler = logging.StreamHandler(sys.stdout)
    __handler.setLevel(level)
    __handler.setFormatter(__formatter)

    __logger = logging.getLogger()
    __logger.setLevel(level)
    __logger.addHandler(__handler)
