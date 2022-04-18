import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from limoucloud_backend import utils as lc_utils


class PaymentMethodTable(tables.Table):
    card_holder = tables.Column()
    brand = tables.Column()
    card_no = tables.Column()
    expires_at = tables.Column()
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-sm table-stripped data-table', 'data-add-url': 'Url here'}

    def render_card_no(self, value):
        return format_html(
            "&#8226;&#8226;&#8226;&#8226; &#8226;&#8226;&#8226;&#8226; &#8226;&#8226;&#8226;&#8226; {}".format(value))

    def render_actions(self, record):
        delete_url = reverse("stripe-card-delete", kwargs={
            "pk": record.get("pk", ""),
            "card_id": record.get("id", ""),
            "customer_id": record.get("customer_id", "")
        })

        return format_html(
            lc_utils.delete_action(delete_url, "{} card ending with {}".format(str(record.get("brand", "")).upper(),
                                                                               record.get("card_no", ""))))
