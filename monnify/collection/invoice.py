from base import Base
from urllib import parse as url_encoder

from validators.invoice_validator import InvoiceCreationSchema


class Invoice(Base):

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)


    def create_invoice(self, auth_token, data) -> tuple:

        validated_data = InvoiceCreationSchema.load(data)

        url_path = "/api/v1/merchant/transactions/init-transaction"
        return self.do_post(url_path, auth_token, validated_data)


    def get_invoice_details(self, auth_token, invoice_reference) -> tuple:

        encoded_reference = url_encoder.quote_plus(invoice_reference)
        url_path = f"/api/v1/invoice/{encoded_reference}/details"
        return self.do_get(url_path, auth_token)
    
    def get_all_invoices(self, auth_token,page=0,size=10):

        url_path = f"/api/v1/invoice/all?page={page}&size={size}"
        return self.do_get(url_path, auth_token)
    
    def cancel_invoice(self, auth_token, invoice_reference):

        encoded_reference = url_encoder.quote_plus(invoice_reference)
        url_path = f"/api/v1/invoice/{encoded_reference}/cancel"
        return self.do_get(url_path, auth_token)
    