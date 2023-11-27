## Forta Toolkit

Various tools to help with the common problems of Forta bot development.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Alert statistics](#alert-statistics)
  - [Logging execution events](#logging-execution-events)
  - [Indexing](#indexing)
  - [Preprocessing](#preprocessing)
  - [Improving performances](#improving-performances)
  - [Load balancing](#load-balancing)
  - [Profiling](#profiling)
  - [Recommendation And Warning](#recommendation-and-warning)
- [Development](#development)
  - [Changelog](#changelog)
  - [Todo](#todo)
- [Credits](#credits)
- [License](#license)

## Installation

```bash
# globally
pip install forta_toolkit

# in a local environment
poetry add forta_toolkit
```

## Usage

### Bot setup

The Forta often require initialization steps to adapt to a given chain or use external tools.

The toolkit reads the OS environment and local files to load the settings:

```python
import forta_toolkit.parsing.env

forta_toolkit.parsing.env.get_bot_version() # reads "package.json" in the parent directory
forta_toolkit.parsing.env.load_secrets() # read the file "secrets.json", in the parent directory
forta_toolkit.parsing.env.load_chain_id(provider=w3) # load the chain_id from the env variables or query the provider if it is not set
```

### Alert statistics

This is an alternative to querying the Zetta API for alert statistics.
It saves a local history of the alerts in memory and use it to calculate the rates.
The main motivation is to improve performance by avoiding web requests.

To use it, just wrap `handle_block` / `handle_transaction` / `handle_alert` as follows:

```python
import forta_toolkit

@forta_toolkit.alerts.alert_history(size=10000)
def handle_block(log: BlockEvent) -> list:
    pass

@forta_toolkit.alerts.alert_history(size=10000)
def handle_transaction(log: TransactionEvent) -> list:
    pass

@forta_toolkit.alerts.alert_history(size=10000)
def handle_alert(log: AlertEvent) -> list:
    pass
```

The decorator will automatically add the `anomaly_score` in the metadata of the `Finding` objects.
It will use the field `alert_id` from the `Finding` objects to identify them.

> make sure the history size is big enough to contain occurences of the bot alerts!

For example, if your bot triggers `ALERT-1` every 2k transactions and `ALERT-2` every 10k on average:
`@alert_history(size=100000)` would gather enough alerts to have a relevant estimation of the rate of both alerts.

### Parsing logs / traces / transactions

The `forta-agent` returns slightly different objects compared to a direct query on a RPC endpoint.

The parsing functions convert these objects into plain dictionaries, with only HEX string data.
Instead of a mix of `bytes`, `HexBytes`, `str`, `int` with irregular formats.

Transactions are represented like the following:

```python
{
    'data': 'a9059cbb000000000000000000000000a95085101c57b0fefdecff295894041feb4071c50000000000000000000000000000000000000000000000000000000ee4165af2',
    'from': '0x6e7d071329267Ef7CD9D6d647C2E01a275dFb85c',
    'hash': '8f6c8d55a3d2da59e8c1d692e5ae0ab73e5eedded638a9d2877f10af8cedbb5e',
    'to': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'value': '00'}
```

Each log is like:

```python
{
    'address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'block': '011b58ad',
    'blockHash': '89b72d1fd0b7696ba62e37d5989fa97aef6b5b80cf2458bcdeed9eb1ea3a13e2',
    'blockNumber': '011b58ad',
    'data': '0000000000000000000000000000000000000000000000000000000022921900',
    'hash': 'cfb6fe2626262e2f53d8319f7a83299b95c5c756fb45951f0f7880b4dd70b60b',
    'index': '34',
    'logIndex': '34',
    'topics': [
        b'\xdd\xf2R\xad\x1b\xe2\xc8\x9bi\xc2\xb0h\xfc7\x8d\xaa\x95+\xa7\xf1'
        b'c\xc4\xa1\x16(\xf5ZM\xf5#\xb3\xef',
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00uv\x18\\'
        b'm\xd0\xae\x1d\xdb\xdc\x99\xeb\xc4\xfe\xe36\xd2\x97\xedO',
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84?\xed\x0b'
        b'B\x06Z\xceM\x1ed\xa9\x12\x97\xc4\xae\x16\xa6Xt'],
    'transactionHash': 'cfb6fe2626262e2f53d8319f7a83299b95c5c756fb45951f0f7880b4dd70b60b',
    'transactionIndex': '0a'}
```

The `topics` are the only data encoded as `bytes` instead of HEX strings.

And finally the each trace looks like this call:

```python
{
    'block': '011b58cd',
    'from': '0x2AB38a87CC9fdf6329aD1224Ef1D1a8b5E7b0aDE',
    'gas': '',
    'hash': '5bb74e335852f74d0cb1967e3df0b0e377bef3b00813d3c2522542078a3bc8c3',
    'input': 'e2bbb15800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    'output': '',
    'to': '0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd',
    'type': 'call',
    'value': ''}
```

The keys remain `("from", "to", "input", "output")` when the trace type is `suicide` or `create`:

```python
{
    'block': 'fe6b17',
    'from': '0x45F50A4aC2c4e636191ADcfBB347Ec2a3079FC02',
    'gas': '',
    'hash': '3bfcc1c5838ee17eec1ddda2f1ff0ac1c1ccdbd30dd520ee41215c54227a847f',
    'input': '5860208158601c335a63aaf10f428752fa158151803b80938091923cf3',
    'output': '7300000027f490acee7f11ab5fdd47209d6422c5a73314601d576023565b3d353d1a565b005b610101565b6101a1565b610269565b610353565b6103ef565b6104b3565b610599565b610635565b6106f9565b6107df565b610851565b6108a8565b6108ab565b610933565b6109b9565b610a4e565b610b27565b610bd8565b610c8f565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b610023565b3d3d60a43d3d60023560601c3d3d7f022c0d9f000000000000000000000000000000000000000000000000000000003d7f23b872dd000000000000000000000000000000000000000000000000000000003d523060045234604052846024523d3d60643d3d73c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25af15052600452602452601635463560001a523060445260806064525af1602357600080fd5b3d3d60a43d3d60023560601c3d3d7f022c0d9f000000000000000000000000000000000000000000000000000000003d7f23b872dd000000000000000000000000000000000000000000000000000000003d523060045234604052846024523d3d60643d3d73c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25af150526004526024526016357fffffffff0000000000000000000000000000000000000000000000000000000016463560001a523060445260806064525af1601a90813560001a57600080fd5b7f23b872dd00000000000000000000000000000000000000000000000000000000600052306004526000600060a460006000856002013560601c600060445286601a013560d81c604052806024526000600060646000600073c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25af1507f022c0d9f000000000000000000000000000000000000000000000000000000006000526000600452600060245286601601357fffffffff00000000000000000000000000000000000000000000000000000000168735461a5230604452608060645260006084525af190601f0190813560001a57600080fd5b3d3d60a43d3d60023560601c3d3d7f022c0d9f000000000000000000000000000000000000000000000000000000003d7fa9059cbb000000000000000000000000000000000000000000000000000000003d5284600452346024523d3d60443d3d73a0b86991c6218b36c1d19d4a2e9eb0ce3606eb485af15052600452602452601635463560001a523060445260806064525af1602357600080fd5b3d3d60a43d3d60023560601c3d3d7f022c0d9f000000000000000000000000000000000000000000000000000000003d7fa9059cbb000000000000000000000000000000000000000000000000000000003d5284600452346024523d3d60443d3d73a0b86991c6218b36c1d19d4a2e9eb0ce3606eb485af150526004526024526016357fffffffff0000000000000000000000000000000000000000000000000000000016463560001a523060445260806064525af1601a90813560001a57600080fd5b7fa9059cbb000000000000000000000000000000000000000000000000000000006000526000600060a460006000856002013560601c600060445286601a013560d81c602452806004526000600060446000600073a0b86991c6218b36c1d19d4a2e9eb0ce3606eb485af1507f022c0d9f000000000000000000000000000000000000000000000000000000006000526000600452600060245286601601357fffffffff00000000000000000000000000000000000000000000000000000000168735461a5230604452608060645260006084525af190601f0190813560001a57600080fd5b3d3d60a43d3d60023560601c3d3d7f022c0d9f000000000000000000000000000000000000000000000000000000003d7fa9059cbb000000000000000000000000000000000000000000000000000000003d5284600452346024523d3d60443d3d73dac17f958d2ee523a2206206994597c13d831ec75af15052600452602452601635463560001a523060445260806064525af1602357600080fd5b3d3d60a43d3d60023560601c3d3d7f022c0d9f000000000000000000000000000000000000000000000000000000003d7fa9059cbb000000000000000000000000000000000000000000000000000000003d5284600452346024523d3d60443d3d73dac17f958d2ee523a2206206994597c13d831ec75af150526004526024526016357fffffffff0000000000000000000000000000000000000000000000000000000016463560001a523060445260806064525af1601a90813560001a57600080fd5b7fa9059cbb000000000000000000000000000000000000000000000000000000006000526000600060a460006000856002013560601c600060445286601a013560d81c602452806004526000600060446000600073dac17f958d2ee523a2206206994597c13d831ec75af1507f022c0d9f000000000000000000000000000000000000000000000000000000006000526000600452600060245286601601357fffffffff00000000000000000000000000000000000000000000000000000000168735461a5230604452608060645260006084525af190601f0190813560001a57600080fd5b3d3d60443d3d7fa9059cbb000000000000000000000000000000000000000000000000000000003d526016357fffffffff00000000000000000000000000000000000000000000000000000000163d35461a52601c3560601c60045260023560601c5af1601a90813560001a57600080fd5b347f2e1a7d4d00000000000000000000000000000000000000000000000000000000013d523d3d60243d3d73c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25af1600060006000600047335af116602357600080fd5b33ff5b3d3d60a43d3d60023560601c7f022c0d9f000000000000000000000000000000000000000000000000000000003d3d7fa9059cbb000000000000000000000000000000000000000000000000000000003d52602a3546353d1a52836004523d3d60443d3d60163560601c5af15060045252346020523060445260806064525af1602357600080fd5b3d3d60a43d3d60023560601c7f022c0d9f0000000000000000000000000000000000000000000000000000000034013d3d7fa9059cbb000000000000000000000000000000000000000000000000000000003d52602a3546353d1a52836004523d3d60443d3d60163560601c5af150602452523060445260806064525af1602357600080fd5b3d3d60a460403d60023560601c7fa9059cbb000000000000000000000000000000000000000000000000000000003d52602a357fffffffff000000000000000000000000000000000000000000000000000000001646353d1a52806004523d3d60443d3d60163560601c5af15034602d35461a5263022c0d9f60245230608452608060a4525af1602f90813560001a57600080fd5b6000600060a460406000856002013560601c7fa9059cbb0000000000000000000000000000000000000000000000000000000060005286602a01357fffffffff00000000000000000000000000000000000000000000000000000000168735461a5280600452600080604481808b6016013560601c5af1506000604452600060645286601301357f000000000000000000000000000000000000000000000000000000ffffffffff168760320135461a5263022c0d9f60245230608452608060a452600060c4525af19060340190813560001a57600080fd5b3d3d60a43d3d60023560601c7f022c0d9f000000000000000000000000000000000000000000000000000000003d3d3d7fa9059cbb000000000000000000000000000000000000000000000000000000003d52602a357fffffffff00000000000000000000000000000000000000000000000000000000163d35461a52846004523d3d60443d3d60163560601c5af1506004526024525234602d35461a523060445260806064525af1602357600080fd5b3d3d60a43d3d60023560601c7f022c0d9f000000000000000000000000000000000000000000000000000000003d3d3d7fa9059cbb000000000000000000000000000000000000000000000000000000003d52602a357fffffffff00000000000000000000000000000000000000000000000000000000163d35461a52846004523d3d60443d3d60163560601c5af1506004526024525234602d35461a523060445260806064525af1602f90602e35461a57600080fd5b60008060a48180856002013560601c600060045260006024527fa9059cbb0000000000000000000000000000000000000000000000000000000060005286602a01357fffffffff00000000000000000000000000000000000000000000000000000000168735461a5280600452600080604481808b6016013560601c5af150600060045260006024527f022c0d9f00000000000000000000000000000000000000000000000000000000600052866013013564ffffffffff168760320135461a5230604452608060645260006084525af19060340190813560001a57600080fd',
    'to': '0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80',
    'type': 'create',
    'value': ''}
```

### Logging execution events

The logging level and message template can be setup with:

```python
forta_toolkit.logging.setup_logger(logging.INFO)
```

Which will produce [messages with the bot version and log level][forta-example-alerts]:

```
[0.1.17 - INFO] Metamorphism: 0x212728A4567F63e41eCD57A7dc329dbF2081B370 is deploying a factory contract at 0xF20e35e946C95ea4fcdadbEd1d79f28f2B8F44DE
```

### Indexing

The input arguments and the output findings can be automatically saved to the disk with:

```python
import forta_toolkit.indexing.dump

@forta_toolkit.indexing.serialize_io()
def handle_transaction(log: TransactionEvent) -> list:
    pass
```

The decorator accepts a few optional arguments:

```python
@forta_toolkit.indexing.serialize_io(arguments=False, results=True, filter=True, compress=False, path='.data/{alert}/{txhash}/')
def handle_transaction(log: TransactionEvent) -> list:
    pass
```

### Preprocessing

The decorator `parse_forta_arguments` processes the input `TransactionEvent` and returns the `transaction`, `logs` and `traces` objects.

These objects are automatically sanitized and parsed into fixed structures and base types (mostly `int`, HEX `str`, `list` and `bytes`).

```python
import forta_toolkit.preprocessing

@forta_toolkit.preprocessing.parse_forta_arguments
def handle_transaction(transaction: dict, logs: list, traces: list) -> list:
    pass
```

This decorator can only be placed right above a function with the signature `(transaction: dict, logs: list, traces: list) -> list`.

### Improving performances

### Load balancing

### Profiling

The bots have to follow the pace of the blockchain, so they need to process transactions relatively quickly.

You can leverage the profiling tools to find the performance bottlenecks in your bots:

```python
from forta_toolkit.profiling import test_performances, display_performances

test_performances(func=handle_transaction, data=some_tx_log)
display_performances(logpath='./test_performances')
```

Otherwise, you can monitor the performances directly when processing mainnet transactions.
Just decorate the `handle_block` / `handle_transaction` / `handle_alert` as follows:

```python
@forta_toolkit.alerts.profile
def handle_transaction(tx: TransactionEvent) -> list:
    pass
```

Then you can parse the profile logs manually with `pstats` or:

```python
display_performances(logpath='some/path/to/the/logs/handle_transaction')
```

### Recommendation And Warning

All the above decorators can be mixed and matched.

However the order in which the decorator are composed matters:

```python
@forta_toolkit.profiling.timeit
@forta_toolkit.alerts.alert_history(size=history_size)
@forta_toolkit.preprocessing.parse_forta_arguments
@forta_toolkit.indexing.serialize_io(arguments=True, results=True)
def handle_transaction(transaction: dict, logs: list, traces: list) -> list:
    pass
```

In the configuration above, the `serialize_io` decorator will save each of the `transaction`, `logs` and `traces` objects.
However if the decorators were switched:

```python
@forta_toolkit.indexing.serialize_io(arguments=True, results=True)`
@forta_toolkit.preprocessing.parse_forta_arguments
```

`serialize_io` would save to disk the arguments of the function returned by `parse_forta_arguments`: a single `TransactionEvent` would be serialized to the disk.

Be wary of this composition and test your setup!

> The recommended order is the one written at the start of this section.

## Development

Contributions welcome!

### Changelog

See [CHANGELOG](CHANGELOG.md).

### Todo

See [TODO](TODO.md).

## Credits

The RPC request queue was inspired by the [TS module `forta-helpers`][github-kovart-helpers] by Artem Kovalchuk.

## License

Licensed under the [aGPL v3](LICENSE).

[forta-example-alerts]: https://alerts.forta.network/logs/agents/0xf76ba7d1d681673300b433611d53c27c6a16666c8ee8fbd167314a6297702ef4
[github-kovart-helpers]: https://github.com/kovart/forta-helpers/blob/main/src/queue.ts
