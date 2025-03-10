from monnify.base import Base
from urllib import parse as url_encoder

from monnify.validators.disbursement_validator import BulkTransferSchema, AuthorizeTransferSchema, ResendOTPSchema



class DisibursementBulk(Base):

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def initiate_transfer(self, auth_token, data):

        validated_data = BulkTransferSchema().load(data)
        url_path = "/api/v2/disbursements/batch"
        return self.do_post(url_path, auth_token, validated_data)
    

    def authorize_transfer(self, auth_token, data):

        validated_data = AuthorizeTransferSchema().load(data)
        url_path = "/api/v2/disbursements/batch/validate-otp"
        return self.do_post(url_path, auth_token, validated_data)
    

    def resend_otp(self, auth_token, data):
        
        validated_data = ResendOTPSchema().load(data)
        url_path = "/api/v2/disbursements/single/resend-otp"
        return self.do_post(url_path, auth_token, validated_data)
    
    def get_transfer_status(self, auth_token, reference):

        encoded_reference = url_encoder.quote_plus(reference)
        url_path = f"/api/v2/disbursements/bulk/{encoded_reference}/transactions"
        return self.do_get(url_path, auth_token)
    
    def search_transactions(self, auth_token, wallet_account_number):

        url_path = f'/api/v2/disbursements/search-transactions?sourceAccountNumber={wallet_account_number}'
        return self.do_get(url_path, auth_token)

