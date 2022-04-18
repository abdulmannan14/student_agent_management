import re
from datetime import date

from Reservation.models import Reservation
from .models import JournalItem, JournalEntry, ChartOfAccount
from ..Transaction.models import Transaction


def get_len(post_data):
    indexes = []
    for key in post_data:
        if key.__contains__("accounts["):
            index = int(re.findall(r"\d+", key)[0])
            indexes.append(index)
    return max(indexes) + 1


def parse_dict(post_data: dict):
    l = get_len(post_data)
    accounts = [{} for i in range(l)]
    for key in post_data:
        if key.__contains__("accounts["):
            vals = key.replace("]", "").split("[")
            index = int(vals[1])
            accounts[index][vals[2]] = post_data[key]
    return accounts


def create_journal_items(accounts: list, journal_entry):
    for account in accounts:
        account["account"] = ChartOfAccount.objects.get(pk=int(account["account"]))
        JournalItem.objects.create(**account, journal_entry=journal_entry)


def create_journal_entry(journal_entry_form, company):
    journal_entry = journal_entry_form.save(commit=False)
    journal_entry.company = company
    journal_entry.save()
    return journal_entry


def journal_entry_reservation_add(reservation):
    entry_obj = JournalEntry.objects.create(reservation=reservation, company=reservation.company,
                                            journal_no='JR_000INV', dated=date.today(),
                                            description=f"Reservation Invoice - {reservation.id}")
    ac_receivable = ChartOfAccount.objects.get(name='Accounts Receivable', company=reservation.company)
    JournalItem.objects.create(journal_entry=entry_obj, account=ac_receivable, debit=reservation.total_fare,
                               description=f"Reservation Item - {reservation.id}", company=reservation.company)

    if reservation.sales_tax:
        ac_sales_tax = ChartOfAccount.objects.get(name=reservation.sales_tax.name, company=reservation.company)
        sales_tax_amount = reservation.base_fare * reservation.sales_tax_percentage / 100
        # Add Tax Journal Item
        JournalItem.objects.create(journal_entry=entry_obj, account=ac_sales_tax,
                                   credit=sales_tax_amount,
                                   description=f"Reservation Sales Tax - {reservation.id}", company=reservation.company)
        # Add Res. Sale Journal Item
        ac_res_sales = ChartOfAccount.objects.get(name='Reservation Sales', company=reservation.company)
        JournalItem.objects.create(journal_entry=entry_obj, account=ac_res_sales,
                                   credit=reservation.total_fare - sales_tax_amount,
                                   description=f"Reservation Sales Income - {reservation.id}",
                                   company=reservation.company)
    else:
        # Add Res. Sale Journal Item
        ac_res_sales = ChartOfAccount.objects.get(name='Reservation Sales', company=reservation.company)
        JournalItem.objects.create(journal_entry=entry_obj, account=ac_res_sales,
                                   credit=reservation.total_fare,
                                   description=f"Reservation Sales Income - {reservation.id}",
                                   company=reservation.company)

    if reservation.deposit_amount != 0:
        if reservation.deposit_type == reservation.CASH:
            ac_coh = ChartOfAccount.objects.get(name=reservation.COH, company=reservation.company)
            journal_entry_payment(reservation, amount=reservation.deposit_amount, dated=date.today(), account=ac_coh,
                                  is_deposit=True)
        elif reservation.deposit_type == reservation.CREDIT_CARD:
            ac_stripe = ChartOfAccount.objects.get(
                name='Stripe_' + reservation.company.stripepayment_set.last().account_id, company=reservation.company)
            journal_entry_payment(reservation, amount=reservation.deposit_amount, dated=date.today(), account=ac_stripe,
                                  is_deposit=True)

    return entry_obj


def journal_entry_reservation_edit(reservation):
    entry_obj = reservation.journalentry_set.last()
    if entry_obj:
        journal_items = entry_obj.journalitem_set.all()
        for item in journal_items:
            if item.account.name == 'Accounts Receivable':
                item.debit = reservation.total_fare
                item.save()
            elif item.account.name == 'Reservation Sales':
                item.credit = reservation.total_fare
                item.save()


def journal_entry_payment(reservation, amount, dated, account, is_deposit=False):
    description = 'Payment for reservation # RES_00001'
    if is_deposit is True:
        description = 'Advance deposit payment for reservation # RES_00001'
    ac_cash_bank = ChartOfAccount.objects.get(name=account, company=reservation.company)
    ac_receivable = ChartOfAccount.objects.get(name='Accounts Receivable', company=reservation.company)

    transaction_obj = Transaction.objects.create(reservation=reservation, dated=dated, amount=amount,
                                                 account_type=ac_cash_bank,
                                                 transaction_type='Deposit', category=ac_receivable,
                                                 description=description,
                                                 company=reservation.company)

    entry_obj = JournalEntry.objects.create(transaction=transaction_obj, company=transaction_obj.company,
                                            journal_no='JR_RES_0001', dated=dated,
                                            description=description,
                                            )

    JournalItem.objects.create(journal_entry=entry_obj, account=ac_cash_bank, debit=amount,
                               description=f"Reservation # RES_0001 Payment Item - {transaction_obj.id}",
                               company=transaction_obj.company)

    JournalItem.objects.create(journal_entry=entry_obj, account=ac_receivable, credit=amount,
                               description=f"Reservation # RES_0001 Payment Item - {transaction_obj.id}",
                               company=transaction_obj.company)

    return transaction_obj


def add_stripe_chart_of_account(company, account_id):
    ChartOfAccount.objects.create(is_editable=False, company=company, account_type=ChartOfAccount.ASSET,
                                    category=ChartOfAccount.CASH_BANK,
                                    name='Stripe_' + account_id,
                                    description="Stripe Account integrated via Secret Key in Settings")

def init_accounts(company):
    # if request.user.userprofile.role == 'COMPANY':
    #     company = request.user.userprofile.companyprofilemodel
    # else:
    #     company = request.user.userprofile.employeeprofilemodel.company
    accounts = [
        {
            'is_editable': False,
            'account_type': 'Asset',
            'category': 'Cash and Bank',
            'name': 'Cash on Hand',
            'description': "Cash you haven't deposited in the bank. Add your bank and credit card accounts to accurately "
                           "categorize transactions that aren't cash. "
        },
        {
            'is_editable': False,
            'account_type': 'Asset',
            'category': 'Expected Payments from Customers',
            'name': 'Accounts Receivable',
            'description': ""
        },
        {
            'is_editable': False,
            'account_type': 'Liability',
            'category': 'Expected Payments to Vendors',
            'name': 'Accounts Payable',
            'description': ""
        },
        {
            'is_editable': False,
            'account_type': 'Liability',
            'category': 'Due for Payroll',
            'name': 'Payroll Liabilities',
            'description': "The total amount you owe for your payroll. This includes wages due to employees and payroll "
                           "taxes owed to the government. "
        },
        {
            'is_editable': False,
            'account_type': 'Liability',
            'category': 'Other Short-Term Liability',
            'name': 'Taxes Payable',
            'description': "The money your business owes in taxes at the federal, state/provincial, or municipal level."
        },
        {
            'is_editable': False,
            'account_type': 'Income',
            'category': 'Income',
            'name': 'Reservation Sales',
            'description': "Payments from your customers for reservation sales that your business sold."
        },
        {
            'is_editable': False,
            'account_type': 'Income',
            'category': 'Uncategorized Income',
            'name': 'Uncategorized Income',
            'description': "Income you haven't categorized yet. Categorize it now to keep your records accurate."
        },
        {
            'is_editable': False,
            'account_type': 'Equity',
            'category': 'Business Owner Contribution and Drawing',
            'name': 'Common Shares',
            'description': "Common shares of a corporation can be issued to business owners, investors, and employees."
        },
        {
            'is_editable': False,
            'account_type': 'Equity',
            'category': 'Retained Earnings: Profit',
            'name': 'Retained Earnings/Deficit',
            'description': "Retained earnings are the total net income your business has earned from its first day to the "
                           "current date, minus any dividends you've already distributed. If the amount of retained "
                           "earnings is negative, report it as a deficit. "
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Accounting Fees',
            'description': "Accounting or bookkeeping services for your business."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Advertising & Promotion',
            'description': "Advertising or other costs to promote your business. Includes web or social media promotion."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Vehicle – Fuel',
            'description': "Gas and fuel costs when driving for business."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Vehicle – Repairs & Maintenance',
            'description': "Repairs and preventative maintenance of the vehicle you drive for business."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Utilities',
            'description': "Utilities (electricity, water, etc.) for your business office. Does not include phone use."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Travel Expense',
            'description': "Transportation and travel costs while traveling for business. Does not include daily commute "
                           "costs. "
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Telephone',
            'description': "Land line and mobile phone services for your business."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Internet',
            'description': "Internet services for your business. Does not include data access for mobile devices."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Computer',
            'description': ""
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Repairs & Maintenance',
            'description': "Repair and upkeep of property or equipment, as long as the repair doesn't add value to the "
                           "property. Does not include replacements or upgrades. "
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Rent Expense',
            'description': "Costs to rent or lease property or furniture for your business office space. Does not include "
                           "equipment rentals. "
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Shipping',
            'description': ""
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Taxes – Corporate Tax',
            'description': "A tax imposed on corporations. If your business is incorporated, you may be required to pay "
                           "this tax depending on your jurisdiction. "
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Office Supplies',
            'description': "Office supplies and services for your business office or space."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Meals and Entertainment',
            'description': "Food and beverages you consume while conducting business, with clients and vendors, "
                           "or entertaining customers. "
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Misc. Expense',
            'description': ""
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Dues & Subscriptions',
            'description': "Fees or dues you pay to professional, business, and civic organizations. Does not include "
                           "business licenses and permits or business memberships. "
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Insurance – General Liability',
            'description': "Premiums that insure your business for things like general liability or workers compensation."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Insurance – Vehicles',
            'description': "Insurance for the vehicle you use for business."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Payroll – Salary & Wages',
            'description': "Wages and salaries paid to your employees."
        },
        {
            'is_editable': False,
            'account_type': 'Expense',
            'category': 'Operating Expense',
            'name': 'Uncategorized Expense',
            'description': "A business cost you haven't categorized yet. Categorize it now to keep your records "
                           "accurate."
        }

    ]
    for account in accounts:
        ChartOfAccount.objects.create(**account, company=company)
    # return redirect('chart-of-accounts')


def add_sales_tax_chart_of_account(company, sales_tax_obj):
    ChartOfAccount.objects.create(is_editable=False, company=company,
                                  account_type=ChartOfAccount.LIABILITY,
                                  category=ChartOfAccount.SALES_TAX,
                                  name=sales_tax_obj.name,
                                  description=sales_tax_obj.description)


def edit_sales_tax_chart_of_account(company, old_sales_tax_name, new_sales_tax_obj):
    account_obj = ChartOfAccount.objects.get(name=old_sales_tax_name, company=company)
    account_obj.name = new_sales_tax_obj.name
    account_obj.description = new_sales_tax_obj.description
    account_obj.save()
