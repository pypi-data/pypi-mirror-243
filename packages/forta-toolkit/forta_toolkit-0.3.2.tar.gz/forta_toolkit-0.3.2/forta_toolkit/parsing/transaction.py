"""Format blockchain logs."""

import forta_toolkit.parsing.address
import forta_toolkit.parsing.common

# TRANSACTION LOGS ############################################################

def parse_transaction_data(transaction: dict) -> dict:
    """Flatten and format all the data in a transaction log."""
    # sanitize & enforce types
    return {
        'hash': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('hash',), default='', callback=forta_toolkit.parsing.common.to_hexstr),
        'from': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('from', 'from_'), default='', callback=forta_toolkit.parsing.address.format_with_checksum),
        'to': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('to',), default='', callback=forta_toolkit.parsing.address.format_with_checksum),
        'value': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('value',), default='00', callback=forta_toolkit.parsing.common.to_hexstr),
        'data': forta_toolkit.parsing.common.get_field(dataset=transaction, keys=('data', 'input'), default='', callback=forta_toolkit.parsing.common.to_hexstr),}
