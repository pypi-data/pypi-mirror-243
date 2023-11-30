"""Format blockchain logs."""

import forta_toolkit.parsing.address
import forta_toolkit.parsing.common

# CASTING #####################################################################

to_hexstr_prefix = lambda __x: forta_toolkit.parsing.common.to_hexstr(data=__x, prefix=True)
to_address_checksum = forta_toolkit.parsing.address.format_with_checksum

# TRANSACTION LOGS ############################################################

def parse_transaction_data(transaction: dict) -> dict:
    """Flatten and format all the data in a transaction log."""
    # sanitize & enforce types
    return {
        'chain_id': '0x01', # TODO
        'block_number': '0x00', # TODO
        'transaction_hash': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('hash', 'transaction_hash',), default='', callback=to_hexstr_prefix),
        'transaction_type': '0x02', # TODO
        'transaction_index': '0x00', # TODO
        'nonce': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('nonce',), default='0x00', callback=to_hexstr_prefix),
        'gas_used': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('gas', 'gas_used',), default='0x00', callback=to_hexstr_prefix),
        'gas_limit': '0x00', # TODO
        'gas_price': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('gas_price',), default='0x00', callback=to_hexstr_prefix),
        'max_fee_per_gas': '0x00', # TODO
        'max_priority_fee_per_gas': '0x00', # TODO
        'success': '0x01', # TODO
        'from_address': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('from', 'from_', 'from_address'), default='', callback=to_address_checksum),
        'to_address': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('to', 'to_address',), default='', callback=to_address_checksum),
        'value': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('value',), default='0x00', callback=to_hexstr_prefix),
        'input': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('data', 'input'), default='', callback=to_hexstr_prefix),}
