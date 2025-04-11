# pymonnify
A Monnify Python Library

## Overview

`monnify-python` is a Python library for interacting with the Monnify API. It provides classes and methods to handle various Monnify services such as transactions, invoices, reserved accounts, disbursements, settlements, and verifications.

## Installation

To install the library, use pip:

After publication do:

```sh
pip install monnify-python
```

For testing do:
```sh
git clone https://github.com/Monnify/monnify-python

cd monnify-python

python3 -m venv dev

source dev/bin/activate

pip install .
```

## Usage

### Initialization
To use the library, you need to initialize the Monnify class with your API key, secret key, and environment (either "SANDBOX" or "LIVE").

```sh
from monnify import Monnify

monnify = Monnify(API_KEY="your_api_key", SECRET_KEY="your_secret_key", ENV="SANDBOX")
```
### Authentication

```sh
status_code, auth_token_obj = monnify.Transaction.get_auth_token()
auth_token = auth_token_obj.get("accessToken")
```

### Transaction
The Transaction class provides methods to handle transactions.

```sh
transaction = monnify.Transaction

# Initialize a transaction

data = {
    "paymentReference": "unique_reference",
    "amount": 1000,
    "customerName": "John Doe",
    "paymentDescription": "Test Payment",
    "currencyCode": "NGN",
    "contractCode": "your_contract_code",
    "customerEmail": "john.doe@example.com",
    "paymentMethods": ["CARD"],
    "redirectUrl": "https://your_redirect_url.com",
    "metaData": {"phoneNumber": "08012345678"},
    "incomeSplitConfig": []
}
status_code, response = transaction.initialize_transaction(data)
```



### Reserved Account
The ReservedAccount class provides methods to handle reserved accounts.

```sh
reserved_account = monnify.ReservedAccount

# Create a reserved account

data = {
    "accountReference": "unique_reference",
    "accountName": "Test Account",
    "customerName": "John Doe",
    "currencyCode": "NGN",
    "contractCode": "your_contract_code",
    "customerEmail": "john.doe@example.com",
    "bvn": "12345678901",
    "getAllAvailableBanks": True,
    "incomeSplitConfig": []
}
status_code, response = reserved_account.create_reserved_acount(data)
```


### Disbursement

The DisbursementSingle and DisibursementBulk classes provide methods to handle single and bulk disbursements, respectively.

```sh
single_disbursement = monnify.DisbursementSingle

# Initiate a single transfer

data = {
    "reference": "unique_reference",
    "amount": 1000,
    "narration": "Test Transfer",
    "destinationBankCode": "057",
    "destinationAccountNumber": "1234567890",
    "sourceAccountNumber": "0987654321",
    "currency": "NGN"
}
status_code, response = single_disbursement.initiate_transfer(data)
```

### Paycode

The Paycode classe provides methods to handle paycode manipulations.

```sh
paycode = monnify.Paycode

# Creates paycode

data = {
    "beneficiaryName": "Tester",
    "amount": 20,
    "paycodeReference": "sspcsspwvdjx0kt",
    "expiryDate": "2025-03-23 17:00:26",
    "clientId":"MK_TEST_FDH37842DJH"
}
status_code, response = paycode.create_paycode(data)
```


### Settlement
The Settlement class provides methods to handle settlements.

```sh
settlement = monnify.Settlement

# Create a sub-account

data = [{
    "bankCode": "057",
    "accountNumber": "1234567890",
    "email": "john.doe@example.com",
    "currencyCode": "NGN",
    "defaultSplitPercentage": 10.0
}]
status_code, response = settlement.create_sub_account(data)
```

### Verification
The Verification class provides methods to handle verifications such as BVN, NIN, and bank account validation.

```sh
verification = monnify.Verification

# Verify BVN

data = {
    "bvn": "12345678901",
    "name": "John Doe",
    "mobileNo": "08012345678",
    "dateOfBirth": "1990-01-01"
}
status_code, response = verification.verify_bvn(data)
```

## Documentation

You can view full library documentation [here](docs/monnify/index.md)
