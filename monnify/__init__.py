from monnify.collection import Transaction, Invoice, ReservedAccount,TransactionRefund
from monnify.disbursement import DisbursementSingle, DisibursementBulk, Paycode
from monnify.settlement import Settlement
from monnify.verification import Verification


class Monnify:
    """
    This is the main class that is used to access all the other classes in the package.
    """    

    def __init__(self, API_KEY=None, SECRET_KEY=None, ENV="SANDBOX"):
        

        classes = [
            Transaction,
            TransactionRefund,
            Invoice,
            ReservedAccount,
            DisbursementSingle,
            DisibursementBulk,
            Paycode,
            Settlement,
            Verification,
        ]

        for cls_ in classes:
            instance = cls_(API_KEY=API_KEY, SECRET_KEY=SECRET_KEY, ENV=ENV)
            setattr(self, cls_.__name__, instance)
