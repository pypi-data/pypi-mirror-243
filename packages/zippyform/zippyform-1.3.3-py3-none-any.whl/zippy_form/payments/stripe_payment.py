import stripe

from zippy_form.utils import PAYMENT_TYPE, APPLICATION_TYPE


def create_product(secret_key, application_type, connected_account_id, name):
    """
    Create Product in Stripe
    """
    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        created_product = stripe.Product.create(name=name, stripe_account=connected_account_id)
    else:
        created_product = stripe.Product.create(name=name)

    return created_product.id


def update_product(secret_key, application_type, connected_account_id, product_id, name):
    """
    Update Stripe Product
    """
    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        stripe.Product.modify(product_id, name=name, stripe_account=connected_account_id)
    else:
        stripe.Product.modify(product_id, name=name)


def create_price(secret_key, application_type, connected_account_id, product_id, payment_type, currency, amount):
    """
    Create Price for Stripe Product
    """
    stripe.api_key = secret_key

    if payment_type == PAYMENT_TYPE[0][0]:
        unit_amount = int(float(amount) * 100)
        if application_type == APPLICATION_TYPE[1][0]:
            created_price = stripe.Price.create(currency=currency, unit_amount=unit_amount, product=product_id,
                                                stripe_account=connected_account_id)
        else:
            created_price = stripe.Price.create(currency=currency, unit_amount=unit_amount, product=product_id)

    return created_price.id


def update_price(secret_key, application_type, connected_account_id, product_id, payment_type, currency, amount,
                 price_id):
    """
    Update Stripe Product Price
    """
    stripe.api_key = secret_key

    if payment_type == PAYMENT_TYPE[0][0]:
        if application_type == APPLICATION_TYPE[1][0]:
            # InActivate Existing Stripe Price
            stripe.Price.modify(price_id, active=False, stripe_account=connected_account_id)
        else:
            # InActivate Existing Stripe Price
            stripe.Price.modify(price_id, active=False)

        # Create New Price For The Product
        created_price_id = create_price(secret_key, application_type, connected_account_id, product_id, payment_type,
                                     currency, amount)

        return created_price_id


def stripe_create_checkout_session(secret_key, application_type, connected_account_id, application_fee_amount,
                                   line_items, after_payment_redirect_url, form_id):
    """
    Create Stripe Checkout Session
    """
    stripe.api_key = secret_key

    application_fee_amount = int(float(application_fee_amount) * 100)

    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            mode='payment',
            line_items=line_items,
            payment_intent_data={
                'application_fee_amount': application_fee_amount,
            },
            stripe_account=connected_account_id,
            return_url=after_payment_redirect_url,
            metadata={'form_id': form_id}
        )

        # Extract the client secret
        client_secret = session.client_secret
    else:
        # Todo
        pass

    return client_secret


def stripe_connect(secret_key, code):
    """
    Stripe Connect
    """
    stripe.api_key = secret_key

    response = stripe.OAuth.token(
        grant_type='authorization_code',
        code=code
    )

    stripe_account_id = response['stripe_user_id']

    return stripe_account_id
