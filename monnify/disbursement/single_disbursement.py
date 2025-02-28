from base import Base
from urllib import parse as url_encoder

from validators.disbursement_validator import SingleTransferSchema, AuthorizeTransferSchema,ResendOTPSchema


class DisbursementSingle(Base):

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def initiate_transfer(self, auth_token, data):

        validated_data = SingleTransferSchema.load(data)

        url_path = "/api/v2/disbursements/single"
        return self.do_post(url_path, auth_token, validated_data)
    

    def authorize_transfer(self, auth_token, data):

        validated_data = AuthorizeTransferSchema.load(data)

        url_path = "/api/v2/disbursements/single/validate-otp"
        return self.do_post(url_path, auth_token, validated_data)
    
    
    def resend_otp(self, auth_token, data):

        validated_data = ResendOTPSchema.load(data)
        
        url_path = "/api/v2/disbursements/single/resend-otp"
        return self.do_post(url_path, auth_token, validated_data)
    
    
    def get_transfer_status(self, auth_token, reference):

        encoded_reference = url_encoder.quote_plus(reference)
        url_path = f"/api/v2/disbursements/single/summary?reference={encoded_reference}"
        return self.do_get(url_path, auth_token)
    
    
    def list_all_transfers(self, auth_token, page=0, size=10):

        url_path = f'/api/v2/disbursements/single/transactions?pageNo={page}&pageSize={size}'
        return self.do_get(url_path, auth_token)
    
    
    def get_wallet_balance(self, auth_token, wallet_account_number):

        url_path = f'/api/v2/disbursements/wallet-balance?accountNumber={wallet_account_number}'
        return self.do_get(url_path, auth_token)

