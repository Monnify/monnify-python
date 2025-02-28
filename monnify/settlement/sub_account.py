from base import Base
from urllib import parse as url_encoder

from validators.settlement_validator import SubAccountSchema







class Settlement(Base):

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def create_sub_account(self, auth_token, data):
    
        validated_data = SubAccountSchema.load(data)

        url_path = "/api/v1/sub-accounts"
        return self.do_post(url_path, auth_token, validated_data)
    

    def update_sub_account(self, auth_token, data):

        validated_data = SubAccountSchema.load(data)

        url_path = "/api/v1/sub-accounts"
        return self.do_put(url_path, auth_token, validated_data)
    
    def get_sub_accounts(self, auth_token):
    
        url_path = f'/api/v1/sub-accounts'
        return self.do_get(url_path, auth_token)
    
    def delete_sub_accounts(self, auth_token, sub_account_code):
        
        url_path = f'/api/v1/sub-accounts/{sub_account_code}'
        return self.do_delete(url_path, auth_token)
    
    def get_transaction_by_settlement_reference(self, auth_token, settlement_reference, page=0, size=10):
    
        encoded_reference = url_encoder.quote_plus(settlement_reference)
        url_path = (
            f"/api/v1/transactions/find-by-settlement-reference?settlement-reference={encoded_reference}&page={page}&size={size}"
        )
        return self.do_get(url_path, auth_token)
    
    def get_transaction_by_transaction_reference(self, auth_token, transaction_reference):
        
        encoded_reference = url_encoder.quote_plus(transaction_reference)
        url_path = (
            f"/api/v1/settlement-detail?transactionReference={encoded_reference}"
        )
        return self.do_get(url_path, auth_token)
