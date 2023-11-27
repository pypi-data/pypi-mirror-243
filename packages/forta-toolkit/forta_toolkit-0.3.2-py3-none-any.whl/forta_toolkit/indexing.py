"""Save and index the bot data on the disk."""

import functools
import os
import pickle
import typing

import forta_toolkit.parsing.common
import forta_toolkit.parsing.logs
import forta_toolkit.parsing.traces
import forta_toolkit.parsing.transaction

# CONSTANTS ###################################################################

PATH = '.data/{alert}/{txhash}/'

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
                __hash = '0x' + forta_toolkit.parsing.common.get_field(dataset=__metadata, keys=('tx_hash', 'txhash', 'hash',), default='')
                __path = path.format(alert=__id, txhash=__hash)
                # dump the inputs
                if arguments:
                    _serialize_inputs(path=__path, args=args, kwargs=kwargs)
                # dump the outputs
                if results:
                    _dump(data=__f, path=os.path.join(__path, 'finding.pkl'))
            return __findings

        return __wrapper

    return __decorator

# DATA SCHEMA #################################################################

# schema for transactions
# -----------------------
# - transaction_type: uint32
# - gas_used: uint64
# - transaction_index: uint64
# - max_priority_fee_per_gas: uint64
# - block_number: uint64
# - to_address: binary
# - gas_price: uint64
# - success: bool
# - from_address: binary
# - value_binary: binary
# - value_string: string
# - value_f64: float64
# - input: binary
# - max_fee_per_gas: uint64
# - transaction_hash: binary
# - nonce: uint64
# - chain_id: uint64
# - gas_limit: uint64

# schema for logs
# ---------------
# - topic0: binary
# - block_number: uint32
# - chain_id: uint64
# - transaction_hash: binary
# - topic2: binary
# - topic1: binary
# - topic3: binary
# - transaction_index: uint32
# - data: binary
# - log_index: uint32
# - address: binary

# schema for traces
# -----------------
# - action_gas: uint32
# - action_from: binary
# - action_value: string
# - action_to: binary
# - result_address: binary
# - action_init: binary
# - block_hash: binary
# - action_reward_type: string
# - chain_id: uint64
# - action_call_type: string
# - result_gas_used: uint32
# - result_code: binary
# - transaction_hash: binary
# - action_type: string
# - result_output: binary
# - trace_address: string
# - subtraces: uint32
# - error: string
# - action_input: binary
# - transaction_index: uint32
# - block_number: uint32

# schema for contracts
# --------------------
# - block_number: uint32
# - contract_address: binary
# - init_code: binary
# - init_code_hash: binary
# - factory: binary
# - create_index: uint32
# - code: binary
# - code_hash: binary
# - transaction_hash: binary
# - deployer: binary
# - chain_id: uint64

# DATABASE ####################################################################

def import_from_database(func: callable) -> callable:
    """Creates a decorator for handle_transaction to add a connection to the database as argument."""

    @functools.wraps(func)
    def __wrapper(*args, **kwargs):
        """Main function called on the logs gathered by the Forta network."""
        # connect to the database
        __database = None
        # call handle_transaction
        return func(*args, database=__database, **kwargs)

    return __wrapper

def export_to_database(transaction: bool=True, logs: bool=True, traces:bool=True, contracts:bool=True, findings: bool=True) -> callable:
    """Creates a decorator for handle_transaction save and index all the data it handles."""

    def __decorator(func: callable) -> callable:
        """Actually wraps the handle_transaction and saves items in the database."""

        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            """Main function called on the logs gathered by the Forta network."""
            # connect to the database
            __database = None
            # process the transaction
            __findings = func(*args, **kwargs)
            # return the findings
            return __findings

        return __wrapper

    return __decorator
