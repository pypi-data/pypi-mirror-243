"""Format event logs."""

import forta_toolkit.parsing.address
import forta_toolkit.parsing.common

# TRACES ######################################################################

def parse_log_data(log: dict) -> dict:
    """Flatten and format all the data in an event log."""
    # common
    __data = {
        'block': forta_toolkit.parsing.common.get_field(dataset=log, keys=('block_number', 'blockNumber', 'block'), default='', callback=forta_toolkit.parsing.common.to_hexstr),
        'hash': forta_toolkit.parsing.common.get_field(dataset=log, keys=('transaction_hash', 'transactionHash', 'hash'), default='', callback=forta_toolkit.parsing.common.to_hexstr),
        'index': forta_toolkit.parsing.common.get_field(dataset=log, keys=('log_index', 'logIndex', 'index'), default='', callback=forta_toolkit.parsing.common.to_hexstr),
        'address': forta_toolkit.parsing.common.get_field(dataset=log, keys=('address',), default='', callback=forta_toolkit.parsing.address.format_with_checksum),
        'topics': forta_toolkit.parsing.common.get_field(dataset=log, keys=('topics',), default=[], callback=lambda __l: [forta_toolkit.parsing.common.to_bytes(__t) for __t in __l]),
        'data': forta_toolkit.parsing.common.get_field(dataset=log, keys=('data',), default='', callback=forta_toolkit.parsing.common.to_hexstr),}
    # aliases
    __data['blockHash'] = forta_toolkit.parsing.common.get_field(dataset=log, keys=('block_hash', 'blockHash'), default='', callback=forta_toolkit.parsing.common.to_hexstr)
    __data['blockNumber'] = __data['block']
    __data['transactionHash'] = __data['hash']
    __data['transactionIndex'] = forta_toolkit.parsing.common.get_field(dataset=log, keys=('transaction_index', 'transactionIndex'), default='', callback=forta_toolkit.parsing.common.to_hexstr)
    __data['logIndex'] = __data['index']
    # output
    return __data
