from random import randint
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_jwt.settings import api_settings

from Company.models import CompanyPackage
from limoucloud_backend.utils import send_email
from . import urls as view_urls
from threading import Thread

from .models import UserProfile


def get_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def random_digits():
    range_start = 10 ** (4 - 1)
    range_end = (10 ** 4) - 1
    return randint(range_start, range_end)


def get_full_url(request, path):
    return "{}://{}{}".format(request.scheme, request.get_host(), path)


def _get_signup_step(step: int):
    new_step = step + 1
    if new_step == 2:
        signup_step = view_urls.account_signup_step_2
    elif new_step == 3:
        signup_step = view_urls.account_signup_step_3
    elif new_step == 4:
        signup_step = view_urls.account_signup_step_4
    return signup_step


def _thread_making(target, arguments: list):
    t = Thread(target=target,
               args=arguments)
    t.setDaemon(True)
    t.start()


def _get_user(username=None, email=None):
    if username:
        return User.objects.filter(username=username).first()
    elif email:
        return User.objects.filter(email=email).first()
    return None


def create_user_profile(user: User, email_verified=False, role=UserProfile.COMPANY):
    return UserProfile.objects.create(user=user, verification_code=random_digits(), email_verified=email_verified,
                                      role=role,step_count=4)


def create_company(address_form, company_form, userprofile, package=None):
    address = address_form.save()
    company = company_form.save(commit=False)
    company.address = address
    company.userprofile = userprofile
    company.company_package = package
    # company.step_count = 4
    company.save()
    return company


def create_package(package_form):
    package: CompanyPackage = package_form.save(commit=False)
    package.set_on_trail(commit=True)
    return package


# def renew_package


def send_welcome_email(request, company, verification_url):
    user = company.userprofile.user
    context = {'subject': 'Company Account has been successfully created!',
               'message': 'Thank you {first_name} for signing up to LimouCloud. As you are new to our system so we need to verify'
                          ' your email first. Either enter the code <strong>{code}</strong> or click on the link given below to'
                          ' verify your email. <strong>{link}</strong> '.format(first_name=user.first_name,
                                                                                code=user.userprofile.verification_code,
                                                                                link=get_full_url(
                                                                                    request,
                                                                                    verification_url)), }

    _thread_making(send_email, ["Welcome to LimouCloud", context, user])
