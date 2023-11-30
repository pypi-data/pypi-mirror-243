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
    'block_number': '0x00',
    'chain_id': '0x01',
    'from_address': '0x584Df055A35acf2d2183d37fC7F42cb4c502Dc51',
    'gas_limit': '0x00',
    'gas_price': '0x0a68fde78f',
    'gas_used': '0x035672',
    'input': '0xac9650d8000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000022450087bdf00000000000000000000000000000000000000000000000006f05b59d3b200000000000000000000000000000000000000000000000196f307ea5990a07aa23d0000000000000000000000000000000000000000000000000000000000000120000000000000000000000000246f5df47af6c407e4149937fbdd74bd4238bbb5000000000000000000000000000000000000000000000000000000006564bea7000000000000000000000000000000000000000000000000001cd4f2da76438c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041ea5d41eeacc2d5c4072260945118a13bb7ebce0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000196e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f0000000000000000000000005c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f00000000000000000000000000000000000000000000000000000000',
    'max_fee_per_gas': '0x00',
    'max_priority_fee_per_gas': '0x00',
    'nonce': '0x3863',
    'success': '0x01',
    'to_address': '0x1D2B04F5008295918BA9c78B1e664fEE8b444007',
    'transaction_hash': '0x030ceaef086d4f8cb8d19ac6f6e0d38522e731db357b6e73a2f7642cf0c9e7fa',
    'transaction_index': '0x00',
    'transaction_type': '0x02',
    'value': '0x00'}
```

Each log is like:

```python
{
    'address': '0x7262a43c94258e6071d3bAC00eBeC6d7c9B4Ef30',
    'blockHash': '0x27fad9215f66a8d3c1d5bd4009bb0af5f3bad76abcf11aadabb2586b33aca837',
    'blockNumber': '0x011cca51',
    'block_hash': '0x27fad9215f66a8d3c1d5bd4009bb0af5f3bad76abcf11aadabb2586b33aca837',
    'block_number': '0x011cca51',
    'chain_id': '0x01',
    'data': '0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006d38666f93bbc74000000000000000000000000000000000000000000032de60fd4b32140f5447b0000000000000000000000000000000000000000000000000000000000000000',
    'logIndex': '0x8c',
    'log_index': '0x8c',
    'topics': [
        b"\xd7\x8a\xd9_\xa4l\x99KeQ\xd0\xda\x85\xfc'_\xe6\x13\xce7"
        b'e\x7f\xb8\xd5\xe3\xd10\x84\x01Y\xd8"',
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d+\x04\xf5'
        b'\x00\x82\x95\x91\x8b\xa9\xc7\x8b\x1efO\xee\x8bD@\x07',
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$o]\xf4'
        b'z\xf6\xc4\x07\xe4\x14\x997\xfb\xddt\xbdB8\xbb\xb5'],
    'transactionHash': '0x030ceaef086d4f8cb8d19ac6f6e0d38522e731db357b6e73a2f7642cf0c9e7fa',
    'transactionIndex': '0x2c',
    'transaction_hash': '0x030ceaef086d4f8cb8d19ac6f6e0d38522e731db357b6e73a2f7642cf0c9e7fa',
    'transaction_index': '0x2c'}
```

The key aliases in camel-case are meant to satisfy the `web3` package expectations.

The `topics` are the only data encoded as `bytes` instead of HEX strings.

And finally the each trace looks like this call:

```python
{
    'action_call_type': 'staticcall',
    'action_from': '0x1D2B04F5008295918BA9c78B1e664fEE8b444007',
    'action_gas': '0x00',
    'action_init': '0x',
    'action_input': '0x70a08231000000000000000000000000246f5df47af6c407e4149937fbdd74bd4238bbb5',
    'action_reward_type': '',
    'action_to': '0x41EA5d41EEACc2D5c4072260945118a13bb7EbCE',
    'action_type': 'call',
    'action_value': '0x00',
    'block_hash': '0x27fad9215f66a8d3c1d5bd4009bb0af5f3bad76abcf11aadabb2586b33aca837',
    'block_number': '0x011cca51',
    'chain_id': '0x01',
    'error': None,
    'result_address': '',
    'result_code': '0x',
    'result_gas_used': '0x0253',
    'result_output': '0x000000000000000000000000000000000000000000356d47e966a8ef1b7c49e3',
    'subtraces': '0x00',
    'trace_address': [0, 8],
    'transaction_hash': '0x030ceaef086d4f8cb8d19ac6f6e0d38522e731db357b6e73a2f7642cf0c9e7fa',
    'transaction_index': '0x2c'}
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
import forta_toolkit.logging
import forta_toolkit.parsing.env

forta_toolkit.logging.setup_logger(level=logging.INFO, version=forta_toolkit.parsing.env.get_bot_version())
```

Which will produce [messages with the bot version and log level][forta-example-alerts]:

```
[0.1.17 - INFO] Metamorphism: 0x212728A4567F63e41eCD57A7dc329dbF2081B370 is deploying a factory contract at 0xF20e35e946C95ea4fcdadbEd1d79f28f2B8F44DE
```

### Indexing

#### Serialization (Pickle)

The input arguments and the output findings can be automatically saved to the disk with:

```python
import forta_toolkit.indexing.dump

@forta_toolkit.indexing.pickle.serialize_io()
def handle_transaction(log: TransactionEvent) -> list:
    pass
```

The decorator accepts a few optional arguments:

```python
@forta_toolkit.indexing.pickle.serialize_io(arguments=False, results=True, filter=True, compress=False, path='.data/{alert}/{txhash}/')
def handle_transaction(log: TransactionEvent) -> list:
    pass
```

#### Database (Parquet)

The blockchain data can be indexed in a database with:

```python
import forta_toolkit.indexing.parquet

@forta_toolkit.indexing.parquet.export_to_database(chain_id=1, dataset='contracts', path='.data/contracts/', chunksize=2**10, compress=True)
def handle_transaction(log: TransactionEvent) -> list:
    pass
```

Currently, only the `contracts` dataset is supported.
The module will soon cover `transaction`, `logs` and `traces` data too.

The database is saved using the `parquet` file format and using the library `pyarrow`.

This historic data can then be imported with:

```python
@forta_toolkit.indexing.parquet.import_from_database(chain_id=CHAIN_ID, dataset='contracts', path='.data/contracts/')
```

Which would lead to the final declaration:

```python
@forta_toolkit.indexing.parquet.export_to_database(chain_id=1, dataset='contracts', path='.data/contracts/', chunksize=2**10, compress=True)
@forta_toolkit.indexing.parquet.import_from_database(chain_id=CHAIN_ID, dataset='contracts', path='.data/contracts/')
def handle_transaction(log: TransactionEvent, dataset: 'pyarrow._dataset.FileSystemDataset') -> list:
    pass
```

> Note that the dataset is automatically passed as argument to `handle_transaction`.

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
@forta_toolkit.indexing.pickle.serialize_io(arguments=True, results=True)
def handle_transaction(transaction: dict, logs: list, traces: list) -> list:
    pass
```

In the configuration above, the `serialize_io` decorator will save each of the `transaction`, `logs` and `traces` objects.
However if the decorators were switched:

```python
@forta_toolkit.indexing.pickle.serialize_io(arguments=True, results=True)`
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
