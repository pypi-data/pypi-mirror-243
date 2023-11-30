from zippy_form.utils import PAYMENT_GATEWAYS
from zippy_form.payments.stripe_payment import create_product, update_product, create_price, update_price, \
    stripe_create_checkout_session


class Payment:
    def __init__(self, primary_payment_gateway, secret_key, application_type, connected_account_id=""):
        self.primary_payment_gateway = primary_payment_gateway
        self.secret_key = secret_key
        self.application_type = application_type
        self.connected_account_id = connected_account_id

    def create_product(self, name):
        """
        Create Product
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            created_product = create_product(self.secret_key, self.application_type, self.connected_account_id, name)

            return created_product

    def update_product(self, product_id, name):
        """
        Update Product
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            update_product(self.secret_key, self.application_type, self.connected_account_id, product_id, name)

    def create_price(self, product_id, payment_type, currency, amount):
        """
        Create Price
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            created_price = create_price(self.secret_key, self.application_type, self.connected_account_id, product_id,
                                         payment_type, currency, amount)

            return created_price

    def update_price(self, product_id, payment_type, currency, amount, price_id):
        """
        Update Price
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            updated_price = update_price(self.secret_key, self.application_type, self.connected_account_id, product_id, payment_type,
                         currency, amount, price_id)

            return updated_price

    def checkout_session(self, application_fee_amount, line_items, after_payment_redirect_url, form_id ):
        """
        Checkout Session
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            checkout_client_secret = stripe_create_checkout_session(self.secret_key, self.application_type, self.connected_account_id, application_fee_amount, line_items, after_payment_redirect_url, form_id)

            return checkout_client_secret


"""
Usage Example:

payment = Payment("stripe", "YourSecretKey", "saas", "")
product_id = payment.create_product("Test Form")
"""
