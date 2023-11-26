"""Utility functions for type casting & sanitization."""

import collections.abc
import typing

# IDENTIFY DATA TYPES #########################################################

identity = lambda x: x

def is_iterable(data: typing.Any) -> bool:
    """Check whether the input can be iterated upon."""
    try:
        iter(data)
    except Exception:
        return False
    return True

def is_hexstr(data: typing.Any) -> bool:
    """Check whether the data is a raw hexadecimal string."""
    try:
        int(data, 16)
        return True
    except Exception:
        return False

# CONVERSIONS #################################################################

def normalize_hexstr(data: str) -> str:
    """Format the hex data in a known and consistent way."""
    return (
        ((len(data) % 2) * '0') # pad so that the length is pair => full bytes
        + data.lower().replace('0x', ''))

def to_hexstr(data: typing.Any) -> str:
    """Format any data as a HEX string."""
    __data = ''
    if isinstance(data, int):
        __data = hex(data)
    if isinstance(data, str):
        __data = data if is_hexstr(data=data) else data.replace('0x', '').encode('utf-8').hex()
    if isinstance(data, bytes):
        __data = data.hex()
    return normalize_hexstr(__data)

def to_bytes(data: typing.Any) -> bytes:
    """Format any data as a bytes array."""
    return bytes.fromhex(to_hexstr(data))

def to_int(data: typing.Any) -> int:
    """Format any data as an integer."""
    __data = to_hexstr(data)
    return int(__data if __data else '0', 16)

# ACCESS ######################################################################

def get_field_alias(dataset: typing.Any, key: typing.Any, default: typing.Any) -> any:
    """Get the value of a field in a dict like object."""
    __default = getattr(dataset, str(key), default)
    return dataset.get(key, __default) if isinstance(dataset, dict) else __default

def get_field(dataset: typing.Any, keys: collections.abc.Iterable, default: typing.Any, callback: callable=identity) -> any:
    """Get the value of a field in a dict like object."""
    if isinstance(keys, str):
        return callback(get_field_alias(dataset=dataset, key=keys, default=default))
    elif is_iterable(data=keys):
        if len(keys) == 1:
            return callback(get_field_alias(dataset=dataset, key=keys[0], default=default))
        elif len(keys) > 1:
            return get_field(
                dataset=dataset,
                keys=keys[:-1],
                default=get_field_alias(dataset=dataset, key=keys[-1], default=default),
                callback=callback)
    return callback(default)

