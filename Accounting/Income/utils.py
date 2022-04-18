from Client import models as client_models
from Merchants.stripe import utils as merchant_stripe_utils
from limoucloud_backend.utils import success_response_fe, failure_response_fe


def stripe_reservation_payment(client, amount):
    if client.merchant_account and client.merchant_account.stripe_id:
        try:
            making_payment = merchant_stripe_utils.create_payment_intent(client.merchant_account.stripe_id,
                                                                         amount=int(float(amount) * 100),
                                                                         company=client.company)
            making_payment.confirm(making_payment['id'], payment_method='pm_card_visa', )
            return True
        except Exception as ex:
            print(ex)
            return False

    else:
        return None
