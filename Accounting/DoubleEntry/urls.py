from django.urls import path, reverse
from . import views

urlpatterns = [

    path("chart-of-accounts/", views.chart_of_accounts, name="chart-of-accounts"),

    # path("init-accounts", views.init_accounts, name="init-accounts"),
    path("chart-of-accounts/get-categories", views.get_account_type_categories,
         name="chart-of-accounts-categories"),
    path("edit-chart-of-account/<int:pk>", views.edit_chart_of_accounts, name="edit-chart-of-account"),
    path('delete-chart-of-account/<int:pk>', views.delete_chart_of_accounts, name="delete-chart-of-account"),

    path("balance-sheet", views.balance_sheet, name="balance-sheet"),
    path("ledger-summary", views.ledger_summary, name="ledger-summary"),
    path("trial-balance", views.trial_balance, name="trial-balance"),

    path("journal-entry", views.journal_entry, name="journal-entry"),
    path("journal-entry/add", views.add_journal_entry, name="journal-entry-add"),
    path("journal-entry/<pk>/edit", views.edit_journal_entry, name="journal-entry-edit"),
    path("journal-entry/<pk>", views.journal_entry_details, name="journal-entry-detail"),
    path('delete-journal-entry/<int:pk>', views.delete_journal_entry, name="journal-entry-delete"),

]
