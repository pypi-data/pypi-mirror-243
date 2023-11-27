"""Format transaction traces."""

import forta_toolkit.parsing.address
import forta_toolkit.parsing.common

# TRACES ######################################################################

def parse_trace_data(trace: dict) -> dict:
    """Flatten and format all the data in a transaction trace."""
    # common
    __action = forta_toolkit.parsing.common.get_field(dataset=trace, keys=('action',), default=trace)
    __result = forta_toolkit.parsing.common.get_field(dataset=trace, keys=('result',), default=trace)
    # common
    __data = {
        'block': forta_toolkit.parsing.common.get_field(dataset=trace, keys=('block_number', 'blockNumber', 'block'), default='', callback=forta_toolkit.parsing.common.to_hexstr),
        'hash': forta_toolkit.parsing.common.get_field(dataset=trace, keys=('transaction_hash', 'transactionHash', 'hash'), default='', callback=forta_toolkit.parsing.common.to_hexstr),
        'type': forta_toolkit.parsing.common.get_field(dataset=trace, keys=('type',), default=''),
        'value': forta_toolkit.parsing.common.get_field(dataset=trace, keys=('value',), default='00', callback=forta_toolkit.parsing.common.to_hexstr),
        'gas': forta_toolkit.parsing.common.get_field(dataset=trace, keys=('gas_used', 'gasUsed', 'gas'), default='00', callback=forta_toolkit.parsing.common.to_hexstr),
        'from': '',
        'to': '',
        'input': '',
        'output': ''}
    # call
    if 'call' in __data['type']:
        __data['type'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('call_type', 'callType', 'type'), default='call') # actually get the exact variant of the call
        __data['from'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('from', 'from_'), default='', callback=forta_toolkit.parsing.address.format_with_checksum)
        __data['to'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('to',), default='', callback=forta_toolkit.parsing.address.format_with_checksum)
        __data['input'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('input',), default='', callback=forta_toolkit.parsing.common.to_hexstr)
        __data['output'] = forta_toolkit.parsing.common.get_field(dataset=__result, keys=('output',), default='', callback=forta_toolkit.parsing.common.to_hexstr)
    # create
    if 'create' in __data['type']:
        __data['from'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('from', 'from_'), default='', callback=forta_toolkit.parsing.address.format_with_checksum)
        __data['to'] = forta_toolkit.parsing.common.get_field(dataset=__result, keys=('address', 'to'), default='', callback=forta_toolkit.parsing.address.format_with_checksum)
        __data['input'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('init', 'input'), default='', callback=forta_toolkit.parsing.common.to_hexstr)
        __data['output'] = forta_toolkit.parsing.common.get_field(dataset=__result, keys=('code', 'output'), default='', callback=forta_toolkit.parsing.common.to_hexstr)
    # suicide
    if 'suicide' in __data['type']:
        __data['from'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('address', 'from'), default='', callback=forta_toolkit.parsing.address.format_with_checksum)
        __data['to'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('refund_address', 'refundAddress', 'to'), default='', callback=forta_toolkit.parsing.address.format_with_checksum)
        __data['input'] = forta_toolkit.parsing.common.get_field(dataset=__action, keys=('balance', 'input'), default='', callback=forta_toolkit.parsing.common.to_hexstr)
        __data['output'] = ''
    # output
    return __data
