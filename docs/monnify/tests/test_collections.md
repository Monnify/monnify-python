Module monnify.tests.test_collections
=====================================

Functions
---------

`test_authentication(prefetch_token)`
:   

Classes
-------

`TestInvoiceAPIs()`
:   

    ### Methods

    `get_reference(self)`
    :

    `initialize_data(self)`
    :

    `instantiate_class(self)`
    :

    `test_all_invoice(self)`
    :

    `test_delete_invoice(self, get_reference)`
    :

    `test_invoice_creation(self, token)`
    :

    `test_invoice_details(self, get_reference)`
    :

`TestReservedAccountAPIs()`
:   

    ### Methods

    `get_account_reference(self, token)`
    :

    `init_class(self)`
    :

    `init_data(self)`
    :

    `test_account_creation(self, token)`
    :

    `test_account_deallocation(self, get_account_reference)`
    :

    `test_account_details(self, get_account_reference)`
    :

    `test_account_transactions(self, get_account_reference)`
    :

    `test_add_linked_account(self, get_account_reference)`
    :

`TestTransactionAPIs()`
:   

    ### Methods

    `get_reference(self)`
    :

    `initialise_data(self)`
    :

    `instantiate_class(self)`
    :

    `test_bank_transfer(self, get_reference)`
    :

    `test_card(self, get_reference)`
    :

    `test_transaction_initialization(self)`
    :

    `test_transaction_status(self)`
    :

    `test_transaction_status_v2(self)`
    :

    `test_ussd_transaction(self, get_reference)`
    :