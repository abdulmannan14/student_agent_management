import django_tables2 as tables
from django.utils.html import format_html

from Reservation.models import Reservation


class ReservationTable(tables.Table):
    action = tables.Column(empty_values=())
    total_fare = tables.Column(verbose_name="Total Fare")
    deposit_amount = tables.Column(verbose_name="Deposit")
    balance_fare = tables.Column(verbose_name="Balance Due")
    id = tables.Column(verbose_name="#")

    class Meta:
        attrs = {"class": 'table table-striped mb-0 dataTable'}
        model = Reservation
        fields = ["id", "client", "total_fare", "deposit_amount", "balance_fare"]

    def render_client(self, value, record):
        return "{}".format(value.name)

    def render_action(self, record):
        if record.balance_paid:
            return format_html(
                """
                <a data-size="2xl" id="{}" class="btn btn-xs btn-success width-auto" href="#">Paid</a>
                """.format(record.pk)
            )
        else:
            return format_html(
                """
                <a data-size="2xl"
                                        id="{}"
                                       data-toggle="modal" data-target="#commonModal"
                                       class="btn btn-xs btn-white btn-icon-only width-auto commonModal resevation" href="#{}">Payment</a>
                """.format(record.pk, record.pk)
            )
