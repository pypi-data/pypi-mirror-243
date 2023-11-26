"""Preprocess the inputs of the Forta "handle" functions."""

import functools

import forta_toolkit.parsing.common
import forta_toolkit.parsing.logs
import forta_toolkit.parsing.traces
import forta_toolkit.parsing.transaction

# ARGS ########################################################################

def _extract_input(*args, **kwargs) -> 'TransactionEvent':
    return

def _parse_handle_transaction_args(*args, **kwargs) -> tuple:
    """"""
    # init
    __tx = {}
    __logs = []
    __traces = []
    # composite object from forta_agent
    __input = None
    __input = forta_toolkit.parsing.common.get_field(dataset=kwargs, keys=('transaction', 'tx', 'log'), default=None)
    if __input is None and :
        __input = args[0]
    # parse
    __tx = forta_toolkit.parsing.transaction.parse_transaction_data(transaction=log.transaction)
    __logs = [forta_toolkit.parsing.logs.parse_log_data(log=__l) for __l in log.logs]
    __traces = [forta_toolkit.parsing.traces.parse_trace_data(trace=__t) for __t in log.traces]
    return __tx, __logs, __traces
