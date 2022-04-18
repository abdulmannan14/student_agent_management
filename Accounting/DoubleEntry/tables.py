import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from .models import JournalEntry


class JournalEntryTable(tables.Table):
    journal_no = tables.Column(attrs={"td": {"class": "Id"}})
    amount = tables.Column(empty_values=())
    action = tables.Column(empty_values=())

    class Meta:
        model = JournalEntry
        attrs = {"class": "table table-striped mb-0 dataTable"}
        fields = ["journal_no", "dated", "amount", "description", "action"]

    def render_journal_no(self, value, record):
        return format_html("""
        <a href="{}" class="Id">{}</a>
        """.format(reverse("journal-entry-detail", kwargs={"pk": record.pk}), value)
                           )

    def render_action(self, value, record):
        return format_html("""
        <a href="{}" class="edit-icon"><i class="fas fa-pencil-alt"></i></a>
        
        <a href="#"
        class="delete-icon "
        data-toggle="tooltip"
        data-original-title="Delete"
        data-confirm="Are You Sure?|This action can not be undone. Do you want to continue?"
        data-confirm-yes="document.getElementById('{}').submit();">
        <i class="fas fa-trash"></i>
        </a>
        <form method="POST" action="{}"
        accept-charset="UTF-8" id="{}"><input
        name="_method" type="hidden" value="DELETE">
        <input type="hidden" name="csrfmiddlewaretoken" value="KiILU2qHxFbQMYZm0HxhH4WZnEii8EHwaib5kpo3x2RqOysHDbVRK5sHlfVpj3kt">
        </form>
                                                                                                                                                </span>
                                        </td>
        """.format(reverse("journal-entry-edit", kwargs={"pk": record.pk}), record.pk,
                   reverse("journal-entry-delete", kwargs={"pk": record.pk}), record.pk)
                           )

    def render_amount(self, record):
        return "${}".format(sum([item.debit for item in record.journalitem_set.all()]))
