import stripe

from Client import models as client_models
from django.conf import settings
from Company import models as company_models


from limoucloud_backend.utils import logger



def create_payment_intent(customer_id, setup_future_usage="off_session", amount=0, currency="usd",
                          automatic_payment_methods_enabled=True, payment_type="card", company=None):
    """
    Create stripe Payment Intent
    """

    company: company_models.CompanyProfileModel
    stripe.api_key = company.stripepayment_set.last().secret_key
    return stripe.PaymentIntent.create(
        customer=customer_id,
        setup_future_usage=setup_future_usage,
        amount=amount,
        currency=currency,
        # automatic_payment_methods={
        #     'enabled': automatic_payment_methods_enabled,
        # },
        payment_method_types=[payment_type],
    )


def create_payment_method(card_data: dict, **kwargs):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        payment_obj = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_data.get("card_number", 0),
                "exp_month": card_data.get("expiry_month", 0),
                "exp_year": card_data.get("expiry_year", 0),
                "cvc": card_data.get("security_code", ""),
            },
            billing_details={
                "name": card_data.get("card_holder_name", "")
            }
        )
        payment_id = payment_obj.get("id", None)
        return {
            "payment_id": payment_id,
            "success": True,
            "message": "Problem creating payment method" if not payment_id else "Payment created"
        }
    except Exception as err:
        error_words = err.__str__().split(":")
        logger(err.__str__())
        err_msg = error_words[error_words.__len__() - 1]
        return {
            "payment_id": None,
            "success": False,
            "message": err_msg
        }


# import stripe
# from django.conf import settings

from Client.models import MerchantAccount


def create_stripe_merchant_account(obj):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # stripe.api_key = obj.merchant_account.stripe_id
    customer = stripe.Customer.create(
        name=obj.userprofile.name,
        email=obj.email,
        # currency="usd",
    )
    if not obj.merchant_account:
        merchant_account = MerchantAccount.objects.create(stripe_id=customer.get("id", ""))
        obj.merchant_account = merchant_account
    else:
        obj.merchant_account.stripe_id = customer.get("id", "")
        obj.merchant_account.save()
    obj.save()
    return obj.merchant_account


def attach_payment_method_to_client(payment_method_id, merchant_account: MerchantAccount):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=merchant_account.stripe_id,
    )
