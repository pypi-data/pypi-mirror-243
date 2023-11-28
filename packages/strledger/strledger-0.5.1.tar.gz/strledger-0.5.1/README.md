# strledger - Sign Stellar Transaction with Ledger on the command line.

![example](https://github.com/overcat/strledger/blob/main/img/example.png)

## Installation
```shell
pip install -U strledger
```

## Cli Usage
```text
Usage: strledger [OPTIONS] COMMAND [ARGS]...

  Stellar Ledger commands.

  This project is built on the basis of ledgerctl, you can check ledgerctl for more features.

Options:
  -v, --verbose  Display exchanged APDU.
  --help         Show this message and exit.

Commands:
  app-info     Get Stellar app info.
  get-address  Get Stellar public address.
  sign-tx      Sign a base64-encoded transaction envelope.
  version      Get strledger version info.
```

## Library Usage

```python
from strledger import get_default_client

client = get_default_client()
# Use the Stellar Python SDK to build a transaction, see https://github.com/StellarCN/py-stellar-base
transaction_envelope = ...
client.sign_transaction(transaction_envelope=transaction_envelope, keypair_index=0)
print(f"signed tx: {transaction_envelope.to_xdr()}")
```