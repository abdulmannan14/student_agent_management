from django.db import models
from Company import models as company_models
from ..Transaction import models as transaction_models
from Reservation import models as reservation_models


class ChartOfAccount(models.Model):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EXPENSE = "Expense"
    INCOME = "Income"
    EQUITY = "Equity"
    types = [
        (ASSET, ASSET),
        (LIABILITY, LIABILITY),
        (EXPENSE, EXPENSE),
        (INCOME, INCOME),
        (EQUITY, EQUITY)
    ]
    # ASSETS
    CASH_BANK = "Cash and Bank"
    EXPECTED_CUSTOMER_PAYMENT = "Expected Payments from Customers"
    # LIABILITY
    EXPECTED_VENDOR_PAYMENT = "Expected Payments to Vendors"
    SALES_TAX = "Sales Taxes"
    PAYROLL_LIABILITY = "Due for Payroll"
    SHORT_TERM_LIABILITY = "Other Short-Term Liability"
    # REVENUE
    INCOME = "Income"
    UNCATEGORIZED_INCOME = "Uncategorized Income"
    # EXPENSE
    OPERATING_EXPENSE = "Operating Expense"
    PAYROLL_EXPENSE = "Payroll Expense"
    UNCATEGORIZED_EXPENSE = "Uncategorized Expense"
    # EQUITY
    OWNER_CONTRIBUTION_DRAWING = "Business Owner Contribution and Drawing"
    RETAINED_EARNINGS = "Retained Earnings: Profit"

    categories = [
        (CASH_BANK, CASH_BANK),
        (EXPECTED_CUSTOMER_PAYMENT, EXPECTED_CUSTOMER_PAYMENT),
        (EXPECTED_VENDOR_PAYMENT, EXPECTED_VENDOR_PAYMENT),
        (SALES_TAX, SALES_TAX),
        (PAYROLL_LIABILITY, PAYROLL_LIABILITY),
        (SHORT_TERM_LIABILITY, SHORT_TERM_LIABILITY),
        (INCOME, INCOME),
        (UNCATEGORIZED_INCOME, UNCATEGORIZED_INCOME),
        (OPERATING_EXPENSE, OPERATING_EXPENSE),
        (PAYROLL_EXPENSE, PAYROLL_EXPENSE),
        (UNCATEGORIZED_EXPENSE, UNCATEGORIZED_EXPENSE),
        (OWNER_CONTRIBUTION_DRAWING, OWNER_CONTRIBUTION_DRAWING),
        (RETAINED_EARNINGS, RETAINED_EARNINGS)
    ]

    # For Dynamic Accounts Object Names
    COH = 'Cash on Hand'

    account_type = models.CharField(max_length=40, null=True, blank=True, choices=types)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=40, null=True, blank=True, choices=categories)
    is_enabled = models.BooleanField(null=True, default=True)
    is_editable = models.BooleanField(null=True, default=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
    def check_uniques_name(self):
        if self.objects.filter(name=self.name, company=self.company):
            return False
        else:
            return True
    def get_account_categories(self, account):
        if account == self.ASSET:
            return self.categories[0:2]
        elif account == self.LIABILITY:
            return self.categories[2:6]
        elif account == self.INCOME:
            return self.categories[6:8]
        elif account == self.EXPENSE:
            return self.categories[8:11]
        elif account == self.EQUITY:
            return self.categories[11:13]


class JournalEntry(models.Model):
    journal_no = models.CharField(max_length=40, null=True, blank=True)
    dated = models.DateField(null=True, verbose_name="Transaction Date")
    description = models.TextField(max_length=1000, null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    transaction = models.ForeignKey(transaction_models.Transaction, on_delete=models.CASCADE, null=True)
    reservation = models.ForeignKey(reservation_models.Reservation, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.journal_no)


class JournalItem(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, null=True)
    debit = models.FloatField(default=0, null=True, blank=False)
    credit = models.FloatField(default=0, null=True, blank=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    account = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
