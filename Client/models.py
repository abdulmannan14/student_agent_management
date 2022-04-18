from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse

from Account.models import UserProfile
from Vehicle.models import Vehicle
from Company import models as company_models
import stripe
from django.conf import settings


class ClientAddressModel(models.Model):
    address = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    zip_code = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.address


class BusinessClientProfileModel(models.Model):
    business_name = models.CharField(max_length=50, null=True, blank=True)
    business_phone = models.CharField(max_length=20, null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.business_name


class ClientPaymentInfoModel(models.Model):
    CASH = "CASH"
    CHECQUE = "CHECQUE"
    CREDIT_CARD = "CREDIT CARD"
    INVOICE = "INVOICE"
    payment_method = [
        (CASH, CASH),
        (CHECQUE, CHECQUE),
        (CREDIT_CARD, CREDIT_CARD),
        (INVOICE, INVOICE)
    ]

    payment_method = models.CharField(choices=payment_method, max_length=60, null=True, blank=True)
    card_name = models.CharField(max_length=50, null=True, blank=True)
    card_number = models.CharField(max_length=50, null=True, blank=True)
    card_expiration_date = models.CharField(max_length=20, null=True, blank=True)
    cvv = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.payment_method)


class MerchantAccount(models.Model):
    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    chosen_payment_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Merchant# %s" % self.pk


class PersonalClientProfileModel(models.Model):
    # LC_ACCOUNT = [
    #     ('TRUE', 'TRUE'),
    #     ('FALSE', 'FALSE'),
    # ]
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.SET_NULL, null=True, blank=True)
    userprofile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    # client_address = models.ForeignKey(ClientAddressModel, on_delete=models.SET_NULL, null=True, blank=True)
    business_client = models.ForeignKey(BusinessClientProfileModel, on_delete=models.SET_NULL, null=True, blank=True)
    client_payment_info = models.ForeignKey(ClientPaymentInfoModel, on_delete=models.SET_NULL, null=True, blank=True)
    primary_phone = models.CharField(max_length=20, null=False, blank=False)
    secondary_phone = models.CharField(max_length=20, null=True, blank=True)
    is_client_active = models.BooleanField(verbose_name="Create LC Account", null=True, blank=True, default=True)
    is_corporate_client = models.BooleanField(default=False, null=False)
    merchant_account = models.ForeignKey(MerchantAccount, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        try:
            return "{} ({})".format(self.userprofile.user.get_full_name(), self.userprofile.user.username)
        except:
            return "--"

    def client_edit_url(self):
        return reverse("company-edit-client", kwargs={'pk': self.pk})

    def client_delete_url(self):
        return reverse("company-delete-client", kwargs={'pk': self.pk})

    @property
    def name(self):
        return self.userprofile.name

    def create_stripe_merchant_account(self):
        stripe.api_key = self.company.stripepayment_set.last().secret_key
        customer = stripe.Customer.create(
            name=self.name,
            email=self.userprofile.email,
            # currency="usd",
        )
        if not self.merchant_account:
            merchant_account = MerchantAccount.objects.create(stripe_id=customer.get("id", ""))
            self.merchant_account = merchant_account
        else:
            self.merchant_account.stripe_id = customer.get("id", "")
            self.merchant_account.save()
        self.save()
        return self.merchant_account

    def has_stripe_account(self):
        if self.merchant_account:
            return True
        else:
            return False
