from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
import sys
from django import forms
from django.utils.html import format_html
from rest_framework.generics import get_object_or_404
from dateutil.relativedelta import relativedelta

from Employee import models as employee_models
from Account import models as account_models
from limoucloud_backend.settings import from_email
from Company import models as company_models
from Account.models import User, UserProfile
from setting.models import VehicleType
from Client import models as client_models


def success_response_fe(data=None, msg='Operation Success', taxes=None):
    return {
        'success': True,
        'message': msg,
        'data': data,
        'taxes': taxes
    }


def failure_response_fe(errors=None, msg='Operation Failure'):
    return {
        'success': False,
        'message': msg,
        'errors': errors
    }


def success_response(status_code=None, data=None, msg='Operation Success!'):
    response = {
        'success': True,
        'message': msg,
        'data': data
    }
    if status_code:
        response["status_code"] = status_code
    return response


def failure_response(status_code=None, errors=None, msg='Operation Failure'):
    response = {
        'success': False,
        'message': msg,
        'errors': errors
    }
    if status_code:
        response["status_code"] = status_code
    return response


# TODO.. Update the code
def send_email(subject, context, user=None, email=None, password=None):
    html = render_to_string('emails/email.html', context)
    if not subject:
        subject = "Dear {}".format(user)
    send_mail(
        subject,
        '',
        from_email,
        recipient_list=[user.email if user else email],
        html_message=html, fail_silently=True
    )


def logger(message: str = "", frame=None):
    """Logs specified message.

    Args:
        message: A message to log.
        frame: A frame object from the call stack.

    See:
        https://docs.python.org/3/library/sys.html#sys._getframe
    """
    function = None
    location = None

    if frame is None:
        try:
            frame = sys._getframe()
        except:
            pass

    if frame is not None:
        try:
            previous = frame.f_back
            function = previous.f_code.co_name
            location = "%s:%s" % (
                previous.f_code.co_filename, previous.f_lineno)
        except:
            pass
    sys.stderr.write("[%s] [%s] %s\r\n" %
                     (function, location, message))


def _get_error_msg(errors):
    """Parse Error message from Error list"""
    try:
        if errors.__len__() > 0:
            key = errors.popitem()
            return key[1][0].title()
    except:
        pass
    return "Unknown Error"


def delete_action(reverse, name):
    return format_html(
        '<button class="btn text-danger btn-sm pull-right" data-toggle="modal" data-target="#exampleModal" '
        'data-whatever="{}" data-name="{}"><i class="fa fa-trash"></i></button>',
        reverse, name)


def detail_action(reverse, name):
    return format_html(
        '<button class="btn text-warning btn-sm pull-right" data-toggle="modal" data-target="#detailModal" '
        'data-url="{}" data-name="{}"><i class="fa fa-eye"></i></button>',
        reverse, name)


def checklist_action(reverse, name):
    return format_html(
        '<button class="btn text-primary btn-sm pull-right" data-toggle="modal" data-target="#detailModal" '
        'data-url="{}" data-name="{}"><i class="fa fa-list"></i></button>',
        reverse, name)


def _get_details_table(model, vehicle=None, driver=None, vehicle_type=None,
                       exclude=['id', 'company_id', 'created_at', 'updated_at']):
    fields = model._meta.fields
    trs = ''
    for field in fields:
        if field.attname not in exclude:
            if field.attname == "is_active":
                value = getattr(model, field.attname)
                if value == True:
                    value = "Active"
                elif value == False:
                    value = "Inactive"
                field.attname = "Work Status"

            elif field.attname == "all_vehicle_name_id" or field.attname == "vehicle_id":
                value = ''
                if not vehicle:
                    # value = getattr(model, field.attname)
                    # get_vehicle= vehicle_models.Vehicle.objects.get(id=value)
                    # name=get_vehicle.all_vehicle_name_id
                    # vehicle_name = vehicle_models.GeneralVehicle.objects.get(id=name)
                    # vehicle_name=vehicle_name.name
                    # value = vehicle_name
                    value = "N/A"
                else:
                    value = vehicle
                field.attname = "Vehicle"

            elif field.attname == "vehicle_type_id":
                value = ''
                if not vehicle_type:
                    # value = getattr(model, field.attname)
                    # get_vehicle_type= VehicleType.objects.get(id=value)
                    # name=get_vehicle_type.all_vehicle_type_name.name
                    # value=name
                    value = "N/A"
                else:
                    value = vehicle_type
                field.attname = "Vehicle Type"

            elif field.attname == "driver_id":
                value = ''
                if not driver:
                    # value = getattr(model, field.attname)
                    # get_employee= employee_models.EmployeeProfileModel.objects.get(id=value)
                    # name=get_employee.full_name
                    # value=name
                    value = "N/A"
                else:
                    value = driver
                field.attname = "Driver"


            else:
                value = getattr(model, field.attname)
                if value == "True":
                    value = "Yes"
                elif value == "False":
                    value = "No"
                elif value == None:
                    value = "N/A"

            tr = '<tr><th>{name}</th><td>{value}</td></tr>'.format(name=field.attname.replace("_", " ").title(),
                                                                   value=value)
            # trs.append(tr)
            trs = trs + tr
    return format_html("<table class='table'>{}</table>".format(trs))


def _get_details_table_checklist(checklist):
    trs = ''
    tr = '<tr><th>Driver</th><td>{driver}</td></tr>' \
         '<tr><th>Vehicle</th><td>{vehicle}</td></tr>' \
         '<tr><th>Fluid</th><td>{fluids}</td></tr>' \
         '<tr><th>Brakes</th><td>{brakes}</td></tr>' \
         '<tr><th>Lights</th><td>{lights}</td></tr>' \
         '<tr><th>Miscellaneous</th><td>{misc}</td></tr>' \
         '<tr><th>Other</th><td>{others}</td></tr>'.format(driver=checklist.driver,
                                                           vehicle=checklist.vehicle,
                                                           fluids=_get_details_table(checklist.fluids),
                                                           brakes=_get_details_table(checklist.brake_and_tyres),
                                                           lights=_get_details_table(checklist.lights),
                                                           misc=_get_details_table(checklist.misc),
                                                           others=checklist.other)
    trs = trs + tr
    return format_html("<table class='table'>{}</table>".format(trs))


def _delete_table_entry(row):
    row.delete()
    return True



def _delete_checklist_table_entry(model, pk):
    row = get_object_or_404(model, pk=pk)
    row.delete()
    return True


def _get_requested_user_related_data(user, request):
    get_request_user = request.user
    get_request_user_name = get_request_user.username
    try:
        get_company = employee_models.EmployeeProfileModel.objects.get(
            userprofile__user__username=get_request_user_name)
    except:
        get_company = company_models.CompanyProfileModel.objects.get(userprofile__user__username=get_request_user_name)


class Get_or_edit_user(forms.ModelForm):
    class Meta:
        model = account_models.User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            # 'phone',
        )


class Get_or_edit_user_profile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Get_or_edit_user_profile, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['readonly'] = False

    class Meta:
        model = account_models.UserProfile
        fields = ('phone',)


class Get_or_edit_user_address(forms.ModelForm):
    class Meta:
        model = account_models.Address
        fields = "__all__"
        exclude = ['longitude', 'latitude', 'country', 'apartment', 'city', 'state', 'zip_code']


def check_current_pass(user: User, currentpassword):
    if user.check_password(currentpassword):
        return True
    else:
        False


def check_password_matches(newpassword: str, confirmpassword: str):
    if newpassword == confirmpassword:
        return True
    else:
        return False


def change_password(user: User, newpassword):
    try:
        user_pass = user.set_password(newpassword)
        # user_pass.save()
        # login(request=request, user=user)

        return True
    except:
        return False


def _get_total_fare(request, fare_amount):
    deposit_amount = request.POST.get('deposit_amount', 0)
    gratuity_percentage = request.POST.get('gratuity_percentage')
    fuel_Surcharge_percentage = request.POST.get('fuel_Surcharge_percentage', 0)
    discount_percentage = request.POST.get('discount_percentage', 0)
    sales_tax_percentage = request.POST.get('sales_tax_percentage', 0)
    tolls = request.POST.get('tolls', 0)
    meet_and_greet = request.POST.get('meet_and_greet', 0)
    fare_amount = float(fare_amount)
    gratuity_percentage = float(gratuity_percentage)
    fuel_Surcharge_percentage = float(fuel_Surcharge_percentage)
    discount_percentage = float(discount_percentage)
    sales_tax_percentage = float(sales_tax_percentage)
    tolls = int(tolls)
    meet_and_greet = int(meet_and_greet)
    deposit_amount = int(deposit_amount)
    gratuity_percentage_value = (fare_amount / 100) * gratuity_percentage
    fuel_Surcharge_percentage_value = (fare_amount / 100) * fuel_Surcharge_percentage
    discount_percentage_value = (fare_amount / 100) * discount_percentage
    sales_tax_percentage_value = (fare_amount / 100) * sales_tax_percentage
    pending_fare_amount = fare_amount + gratuity_percentage_value + fuel_Surcharge_percentage_value + sales_tax_percentage_value + tolls + meet_and_greet
    pending_fare_amount = pending_fare_amount - discount_percentage_value - deposit_amount
    pending_fare_amount = float(pending_fare_amount)
    pending_fare_amount = str(round(pending_fare_amount, 2))
    total_fare = float(pending_fare_amount) + int(deposit_amount)
    total_fare = str(round(total_fare, 2))
    return total_fare, pending_fare_amount


def _get_hours_rate(request):
    hour_rate = []
    i = 0
    for i in range(24):
        hour_number = str(i) + 'hr'
        hour = request.POST.get(hour_number)
        if hour is not None:
            hour = int(hour)
            hour_rate.append(hour)
        else:
            pass
    rate_of_total_hours = sum(hour_rate)
    total_hours = len(hour_rate)

    return rate_of_total_hours, total_hours


def get_vehicle_types():
    from setting.models import VehicleType
    vehicles = []  # VehicleType.objects.all()
    a = [('ALL', 'ALL')]
    for vehicle in vehicles:
        id = vehicle.id
        name = vehicle.name
        a.append((id, name))
    a = tuple(a)
    return a


def get_my_company_vehicle_type(company):
    vehicles = VehicleType.objects.filter(company=company)
    a = [('ALL', 'ALL')]
    for vehicle in vehicles:
        id = vehicle.id
        name = vehicle.all_vehicle_type_name
        a.append((id, name))
    a = tuple(a)
    return a


def get_my_company_customers(company_id):
    all_clients = client_models.PersonalClientProfileModel.objects.filter(company=company_id)
    # vehicles = VehicleType.objects.filter(company=get_company_id)
    a = [('', '')]
    for client in all_clients:
        id = client.id
        name = client.userprofile.user.username
        a.append((id, name))
    a = tuple(a)
    return a


def get_user_profile(username=None, code=None, email=None):
    try:
        if username and code:
            return UserProfile.objects.get(user__username=username, verification_code=code)
        if email and code:
            return UserProfile.objects.get(user__email=email, verification_code=code)
        if username:
            return UserProfile.objects.get(user__username=username)
        if email:
            return UserProfile.objects.get(user__email=email)
        if code:
            return UserProfile.objects.get(verification_code=code)

        logger("Username or email not provided!")
        return None
    except UserProfile.DoesNotExist as exep:
        logger(str(exep))
        return None


# def test_mail():
#     context = {
#         'subject': "Dear Mannan",
#         'message': "loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum " \
#                    "loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum " \
#                    "loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum " \
#                    "loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum " \
#                    "loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum loreum epsum ",
#     }
#     html = render_to_string('emails/email.html', context)
#     send_mail(
#         '',
#         '',
#         from_email,
#         recipient_list=['mannanmaan1425@gmail.com',],
#         html_message=html, fail_silently=True
#     )


def add_to_datetime(start_date, days=0, months=0, years=0):
    return start_date + relativedelta(days=days, months=months, years=years)
