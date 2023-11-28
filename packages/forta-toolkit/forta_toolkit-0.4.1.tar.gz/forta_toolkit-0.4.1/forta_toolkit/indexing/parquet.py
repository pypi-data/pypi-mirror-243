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

PATH = '.data/parquet/{chain_id}/{dataset}/'

# TRANSACTIONS SCHEMA #########################################################

TRANSACTIONS_SCHEMA = pyarrow.schema([
    pyarrow.field('chain_id', pyarrow.uint64()),
    pyarrow.field('block_number', pyarrow.uint64()),
    pyarrow.field('transaction_hash', pyarrow.binary()),
    pyarrow.field('transaction_type', pyarrow.uint32()),
    pyarrow.field('transaction_index', pyarrow.uint64()),
    pyarrow.field('nonce', pyarrow.uint64()),
    pyarrow.field('gas_used', pyarrow.uint64()),
    pyarrow.field('gas_limit', pyarrow.uint64()),
    pyarrow.field('gas_price', pyarrow.uint64()),
    pyarrow.field('max_fee_per_gas', pyarrow.uint64()),
    pyarrow.field('max_priority_fee_per_gas', pyarrow.uint64()),
    pyarrow.field('success', pyarrow.bool()),
    pyarrow.field('from_address', pyarrow.binary()),
    pyarrow.field('to_address', pyarrow.binary()),
    pyarrow.field('value_binary', pyarrow.binary()),
    pyarrow.field('value_string', pyarrow.string()),
    pyarrow.field('value_f64', pyarrow.float64()),
    pyarrow.field('input', pyarrow.binary()),])

# TRANSACTIONS SCHEMA #########################################################

LOGS_SCHEMA = pyarrow.schema([
    pyarrow.field('chain_id', pyarrow.uint64()),
    pyarrow.field('block_number', pyarrow.uint32()),
    pyarrow.field('transaction_hash', pyarrow.binary()),
    pyarrow.field('transaction_index', pyarrow.uint32()),
    pyarrow.field('address', pyarrow.binary()),
    pyarrow.field('log_index', pyarrow.uint32()),
    pyarrow.field('topic0', pyarrow.binary()),
    pyarrow.field('topic2', pyarrow.binary()),
    pyarrow.field('topic1', pyarrow.binary()),
    pyarrow.field('topic3', pyarrow.binary()),
    pyarrow.field('data', pyarrow.binary()),])

# TRANSACTIONS SCHEMA #########################################################

TRACES_SCHEMA = pyarrow.schema([
    pyarrow.field('chain_id', pyarrow.uint64()),
    pyarrow.field('block_hash', pyarrow.binary()),
    pyarrow.field('block_number', pyarrow.uint32()),
    pyarrow.field('transaction_hash', pyarrow.binary()),
    pyarrow.field('transaction_index', pyarrow.uint32()),
    pyarrow.field('action_type', pyarrow.string()),
    pyarrow.field('action_call_type', pyarrow.string()),
    pyarrow.field('action_reward_type', pyarrow.string()),
    pyarrow.field('action_gas', pyarrow.uint32()),
    pyarrow.field('action_from', pyarrow.binary()),
    pyarrow.field('action_to', pyarrow.binary()),
    pyarrow.field('action_input', pyarrow.binary()),
    pyarrow.field('action_init', pyarrow.binary()),
    pyarrow.field('action_value', pyarrow.string()),
    pyarrow.field('result_address', pyarrow.binary()),
    pyarrow.field('result_gas_used', pyarrow.uint32()),
    pyarrow.field('result_code', pyarrow.binary()),
    pyarrow.field('result_output', pyarrow.binary()),
    pyarrow.field('trace_address', pyarrow.string()),
    pyarrow.field('subtraces', pyarrow.uint32()),
    pyarrow.field('error', pyarrow.string()),])

# TRANSACTIONS SCHEMA #########################################################

CONTRACTS_SCHEMA = pyarrow.schema([
    pyarrow.field('chain_id', pyarrow.uint64()),
    pyarrow.field('block_number', pyarrow.uint32()),
    pyarrow.field('transaction_hash', pyarrow.binary()),
    pyarrow.field('deployer', pyarrow.binary()),
    pyarrow.field('contract_address', pyarrow.binary()),
    pyarrow.field('create_index', pyarrow.uint32()),
    pyarrow.field('init_code', pyarrow.binary()),
    pyarrow.field('init_code_hash', pyarrow.binary()),
    pyarrow.field('code', pyarrow.binary()),
    pyarrow.field('code_hash', pyarrow.binary()),
    pyarrow.field('factory', pyarrow.binary()),])

# IMPORT ######################################################################

def import_from_database(path: str=PATH) -> callable:
    """Creates a decorator for handle_transaction to add a connection to the database as argument."""

    def __decorator(func: callable) -> callable:
        """Actually wraps the handle_transaction and saves items in the database."""

        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            """Main function called on the logs gathered by the Forta network."""
            # connect to the database
            __database = None
            # call handle_transaction
            return func(*args, database=__database, **kwargs)

        return __wrapper

    return __decorator

# EXPORT ######################################################################

def export_to_database(transaction: bool=True, logs: bool=True, traces: bool=True, contracts: bool=True, findings: bool=True, path: str=PATH) -> callable:
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
