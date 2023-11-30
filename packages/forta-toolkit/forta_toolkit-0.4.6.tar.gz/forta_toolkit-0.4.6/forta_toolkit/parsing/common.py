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

def is_empty_hexstr(data: typing.Any) -> bool:
    """Check whether the data is an empty hexadecimal string."""
    return (
        isinstance(data, str)
        and ((data == '') or (data.lower() == '0x')))

def is_hexstr(data: typing.Any) -> bool:
    """Check whether the data is a raw hexadecimal string."""
    try:
        int(data, 16) if not is_empty_hexstr(data=data) else 0
        return True
    except Exception:
        return False

# HEX STRINGS #################################################################

def del_hex_prefix(data: str) -> str:
    """Safely remove the HEX Ox prefix (no error when absent)."""
    return data.replace('0x', '').replace('0X', '')

def add_hex_prefix(data: str) -> str:
    """Safely prepend the HEX Ox prefix (no duplicates)."""
    return '0x' + del_hex_prefix(data=data)

def normalize_hexstr(data: str, prefix=False) -> str:
    """Format the hex data in a known and consistent way."""
    __prefix = '0x' if prefix else ''
    __padding = (len(data) % 2) * '0' # pad so that the length is pair => full bytes
    __data = del_hex_prefix(data.lower())
    return __prefix + __padding + __data

# CONVERSIONS #################################################################

def to_hexstr(data: typing.Any, prefix=False) -> str:
    """Format any data as a HEX string."""
    __data = ''
    if isinstance(data, int):
        __data = hex(data)
    if isinstance(data, str):
        __data = data if is_hexstr(data=data) else data.encode('utf-8').hex()
    if isinstance(data, bytes):
        __data = data.hex()
    return normalize_hexstr(data=__data, prefix=prefix)

def to_bytes(data: typing.Any) -> bytes:
    """Format any data as a bytes array."""
    return bytes.fromhex('' if is_empty_hexstr(data=data) else to_hexstr(data=data))

def to_int(data: typing.Any) -> int:
    """Format any data as an integer."""
    __data = to_hexstr(data=data, prefix=False)
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

