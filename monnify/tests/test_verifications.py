import pytest
import os
from secrets import token_hex

from monnify.tests import prefetch_token, preset_env ,set_token as token
from monnify.verification import Verification





class TestSettlementAPIs:
    

    @pytest.fixture(autouse=True)
    def instantiate_class(self):
        self.__instance = Verification(os.environ.get('API_KEY'),os.environ.get('SECRET_KEY'))
    
    @pytest.fixture(autouse=True)
    def initialise_data(self):
        self.__account_number = '2085886393'
        self.__bank_code ='057'
        
    
    def test_account_validation(self, token):

        code, result = self.__instance.validate_bank_account(token,self.__account_number,self.__bank_code)
        assert code == 200