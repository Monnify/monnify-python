from monnify.base import Base

from monnify.validators.verification_validator import BVNMatchSchema, BVNVerificationSchema, NINVerificationSchema





class Verification(Base):

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def verify_bvn(self, auth_token, data):
    
        validated_data = BVNVerificationSchema().load(data)

        url_path = "/api/v1/vas/bvn-details-match"
        return self.do_post(url_path, auth_token, data)
    
    
    def match_bvn_with_account_name(self, auth_token, data):
    
        validated_data = BVNMatchSchema().load(data)

        url_path = "/api/v1/vas/bvn-account-match"
        return self.do_post(url_path, auth_token, data)
    
    
    def verify_nin(self, auth_token, data):
    
        validated_data = NINVerificationSchema().load(data)

        url_path = "/api/v1/vas/nin-details"
        return self.do_post(url_path, auth_token, data)
    
    def validate_bank_account(self, auth_token, account_number, bank_code):
    
        url_path = f'/api/v1/disbursements/account/validate?accountNumber={account_number}&bankCode={bank_code}'
        return self.do_get(url_path, auth_token)
