"""Turn detection data into a Forta alert."""

# METADATA ####################################################################

def default_get_alert_metadata(chain_id: int, transaction: dict, log: dict, trace: dict, confidence: float, **kwargs) -> dict:
    """Generate the alert metadata."""
    return {
        'chain_id': str(chain_id),
        'tx_hash': transaction.get('transaction_hash', ''),
        'from': transaction.get('from_address', '0x'),
        'to': transaction.get('to_address', '0x'),
        'confidence': str(round(confidence, 1)),}

# FACTORY #####################################################################

def format_finding_factory(
    get_alert_id: callable,
    get_alert_name: callable,
    get_alert_description: callable,
    get_alert_type: callable,
    get_alert_severity: callable,
    get_alert_labels: callable,
    get_alert_log: callable,
    get_alert_metadata: callable=default_get_alert_metadata
) -> callable:
    """Prepare a formatting function for a specific bot."""
    def __format_finding(**kwargs) -> dict:
        """Structure all the metadata of the transaction in a Forta "Finding" object."""
        # raise a Forta network alert
        return {
            'alert_id': get_alert_id(**kwargs),
            'name': get_alert_name(**kwargs),
            'description': get_alert_description(**kwargs),
            'type': get_alert_type(**kwargs),
            'severity': get_alert_severity(**kwargs),
            'metadata': get_alert_metadata(**kwargs),
            'labels': get_alert_labels(**kwargs),}
    # return the actual function
    return __format_finding
