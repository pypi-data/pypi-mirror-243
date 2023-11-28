"""Save and index the bot data on the disk."""

import functools
import os
import pickle
import typing

import pyarrow

import forta_toolkit.parsing.common
import forta_toolkit.parsing.logs
import forta_toolkit.parsing.traces
import forta_toolkit.parsing.transaction

# CONSTANTS ###################################################################

PATH = '.data/pickle/{alert_id}/{transaction_hash}/'

# FILE SYSTEM #################################################################

def _dump(data: typing.Any, path: str) -> None:
    """Pickle any Python object into a file."""
    os.makedirs(name=os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as __file:
        pickle.dump(obj=data, file=__file)

# PICKLE ######################################################################

def _serialize_inputs(path: str, args: tuple, kwargs: dict) -> None:
    """Serialize any function inputs with pickle."""
    for __i in range(len(args)):
        _dump(data=args[__i], path=os.path.join(path, '{name}.pkl'.format(name=__i)))
    for __k, __v in kwargs.items():
        _dump(data=__v, path=os.path.join(path, '{name}.pkl'.format(name=__k)))

def serialize_io(arguments: bool=True, results: bool=True, filter: bool=True, compress: bool=False, path: str=PATH) -> callable:
    """Creates a decorator for handle_transaction to dump its data as serialized python objects."""

    def __decorator(func: callable) -> callable:
        """Actually wraps the handle_transaction and dumps data"""

        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            """Main function called on the logs gathered by the Forta network."""
            __findings = func(*args, **kwargs)
            # dump each finding separately
            for __f in __findings:
                # compute the path
                __id = forta_toolkit.parsing.common.get_field(dataset=__f, keys=('alert_id',), default='')
                __metadata = forta_toolkit.parsing.common.get_field(dataset=__f, keys=('metadata',), default={})
                __hash = forta_toolkit.parsing.common.add_hex_prefix(forta_toolkit.parsing.common.get_field(dataset=__metadata, keys=('tx_hash', 'txhash', 'transaction_hash', 'hash',), default=''))
                __path = path.format(alert_id=__id, transaction_hash=__hash)
                # dump the inputs
                if arguments:
                    _serialize_inputs(path=__path, args=args, kwargs=kwargs)
                # dump the outputs
                if results:
                    _dump(data=__f, path=os.path.join(__path, 'finding.pkl'))
            return __findings

        return __wrapper

    return __decorator
