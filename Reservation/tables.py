import django_tables2 as tables
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from limoucloud_backend import utils as backend_utils
from . import models as reservation_models
from Company import urls as company_urls


class ReservationTables(tables.Table):
    # Reservation=tables.Column(empty_values=())
    id = tables.Column(verbose_name='Reservation #')
    actions = tables.Column(empty_values=())
    pick_up_date = tables.Column(empty_values=(), verbose_name='Trip Date')
    pick_up_time = tables.Column(empty_values=(), verbose_name='Trip Time')
    client = tables.Column(verbose_name='Customer')
    pickup_address = tables.Column(verbose_name='Pick Up')
    destination_address = tables.Column(verbose_name='Drop Off')
    total_fare = tables.Column(empty_values=(), verbose_name='Amount')
    reservation_status = tables.Column(verbose_name='Status')

    class Meta:
        attrs = {"class": 'table table-sm table-stripped data-table', 'data-add-url': 'Url here'}
        model = reservation_models.Reservation
        # exclude=('id','company')
        fields = ['id', 'pick_up_date', 'pick_up_time', 'client', 'pickup_address', 'destination_address',
                  'total_fare',
                  'reservation_status']

    def render_id(self, value):
        return format_html("""
        <a  href="{}">#{}</a>
        """.format(reverse("company-detail-reservation", kwargs={"pk": value}), value)
                           )

    def render_client(self, value):
        return format_html("""
        <a target="_blank" href="{}">{}</a>
        """.format(reverse("client-overview", kwargs={"id": value.pk}), value)
                           )

    def render_pick_up_date(self, record):
        try:
            return "{}".format(record.pick_up_date.strftime('%B-%d-%Y'))
        except:
            return "{}".format(record.pick_up_date)

    def render_pick_up_time(self, record):
        try:
            return "{}".format(record.pick_up_time.strftime('%I:%M %p'))
        except:
            return "{}".format(record.pick_up_time)

    def render_total_fare(self, record):
        try:
            return "${}".format(record.total_fare)
        except:
            return "{}".format(record.total_fare)

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "<a class='btn text-warning btn-sm' href='{detail}'><i class='fa fa-eye'></i></a>"
                           "{delete}".format(
            update=company_urls.edit_reservation(record.pk),
            delete=backend_utils.delete_action(company_urls.delete_reservation(record.pk), record),
            detail=company_urls.get_detail_reservation(record.pk),
            # detail=backend_utils.detail_action(company_urls.get_detail_reservation(record.pk), record)
        ))


class ReservationTablesForAccounting(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = reservation_models.Reservation
        # exclude=('id','company')
        fields = ['pick_up_date', 'pick_up_time', 'client', 'pickup_address', 'destination_address', 'total_fare',
                  'reservation_status']

    def render_actions(self, record):
        context = {
            'links': [
                {
                    'option': "Update",
                    'href': reverse('company-add-reservations'),
                },
            ]
        }
        html = render_to_string("dashboard/accounts/sales/estimate/tables.html", context)
        return format_html(html)


# def get_color_for_options(option):
#     color='no_color'
#     if option == 'QUOTED':
#         color = 'pink'
#     if option == 'CONFIRMED':
#         color = 'orange'
#     if option == 'SCHEDULED':
#         color = 'sky'
#     if option == 'COMPLETED':
#         color = 'green'
#     if option == 'CANCELLED':
#         color = '&#x1F534;'
#     # if option[0] == 'REQUESTED':
#     if option == 'PENDING - PICKED UP':
#         color = 'blue'
#     if option == 'PENDING - DROPPED OFF':
#         color = 'yellow'
#     return color

class Dispatch_table(tables.Table):
    # Reservation=tables.Column(empty_values=())
    # pick_up = tables.Column(empty_values=())
    status = tables.Column(empty_values=())
    id = tables.Column(verbose_name='Reservation #')
    pick_up_date = tables.Column(verbose_name='Trip Date')
    pick_up_time = tables.Column(verbose_name='Trip Time')
    client = tables.Column(verbose_name='Customer')
    pickup_address = tables.Column(verbose_name='PickUp')
    destination_address = tables.Column(verbose_name='DropOff')
    total_fare = tables.Column(verbose_name='Amount')

    class Meta:
        attrs = {"class": 'table table-sm table-stripped data-table', 'data-add-url': 'Url here'}
        model = reservation_models.Reservation
        fields = ['id', 'pick_up_date', 'pick_up_time', 'client', 'pickup_address', 'destination_address', 'total_fare']

    # def render_pick_up(self, record):
    #     return "{} {}".format(record.pick_up_date, record.pick_up_time)

    def render_status(self, record):
        options = record.status_types
        html_options = ''
        for option in options:
            if record.reservation_status == option[0]:
                # color = get_color_for_options(option[0])
                opt = "<option selected  value={a}>{a} </option>".format(
                    a=option[0])
                html_options += opt

            else:
                # color = get_color_for_options(option[0])
                opt = "<option  value={a}>{a}</option>".format(
                    a=option[0])
                html_options += opt

        return format_html(
            '<select name="dispatch"  class="dispatch_dropdown_class dispatch-dropdown" id="dispatch_dropdown" data-url={url}>{html_options}</select>'.format(
                html_options=html_options, url=reverse('company-modify-dispatch', kwargs={'id': record.id})))
