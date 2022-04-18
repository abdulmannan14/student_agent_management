import django_tables2 as tables
from django.utils.html import format_html

from Accounting.Vendor import models as vendor_models
from Accounting.Vendor import urls as vendor_urls


def details_btn(href: str):
    return """<a href="{}" class="edit-icon bg-info" data-toggle="tooltip" data-original-title="View">
                <i class="fas fa-eye"></i>
            </a>""".format(href)


def edit_btn(href: str = "#", data_url: str = "", title: str = "Edit"):
    return """
    <a href="{}" class="edit-icon" data-size="2xl" data-url="{}" data-ajax-popup="true" data-title="{}" data-toggle="tooltip" data-original-title="Edit">
                                                            <i class="fas fa-pencil-alt"></i>
                                                        </a>
    """.format(href, data_url, title)


def delete_btn(href):
    return """
    <a href="#" class="delete-icon trigger--fire-modal-1" data-toggle="tooltip" data-original-title="Delete"
        data-confirm="Are You Sure?|This action can not be undone. Do you want to continue?"
        data-confirm-yes="document.getElementById('delete-form-1').submit();">
         <i class="fas fa-trash"></i>
         <form method="GET" action="{}" accept-charset="UTF-8" id="delete-form-1">
        </form>
    </a>
    """.format(href)


class VendorTable(tables.Table):
    action = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table table-striped mb-0 dataTable"}
        model = vendor_models.Vendor
        fields = ["name", "contact", "email", "balance", "vendor_type", "action"]

    def render_action(self, record):
        return format_html("""
        <span>{}{}{}</span>                                                                                                                       </span>
        """.format(
            details_btn(vendor_urls.vendor_details(record.pk)),
            edit_btn(data_url="", title="Edit Vendor"),
            delete_btn(""))
        )

    def render_balance(self, value, record):
        return format_html("${} {}".format(value, record.name))
