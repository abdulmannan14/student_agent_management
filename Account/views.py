import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from rest_framework.response import Response
from Company.models import CompanyProfileModel, CompanyPackage, Package
from limoucloud_backend.utils import success_response, send_email, failure_response
from . import forms as account_forms, account
from . import urls_api as api_urls
from . import urls as account_urls
from Company import forms as company_forms
# Create your views here.
from .models import UserProfile
from . import utils as account_utils
from threading import Thread
from Home import urls as home_urls
from . import utils as account_utils
from django.contrib import messages
from . import models as account_models
from Employee import models as employee_models
from Accounting.DoubleEntry.utils import init_accounts


def user_login(request):
    context = {
        "title": "Login",
        "page_title": "Welcome Back!",
        "page_subtitle": "Please use your credentials to login to your account.",

        "main_btn": {
            "title": "Sign In",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Forget password?",
                "href": account_urls.forget_password()
            },
            {
                "title": "Create account?",
                "href": account_urls.account_signup()
            }
        ],
        "form": {
            "action": api_urls.get_login_url(),
            "form": account_forms.AuthForm(),
            "title": "log in"
        }
    }
    return render(request, "accounts/multi-steps.html", context)


def company_register(request):
    context = {
        "title": "Sign Up",
        "page_title": "Sign Up",
        "page_subtitle": "Free 30 Day Trial. No Contract. Cancel When You Want.",
        "main_btn": {
            "title": "Sign Up",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Forget Password?",
                "href": account_urls.forget_password()
            },
            {
                "title": "Create account",
                "href": "javascript:;"
            }
        ],
        "forms": {
            "action": api_urls.get_login_url(),
            "personal_form": {
                "title": "Personal Information",
                "form": account_forms.UserRegisterForm(),
            },
            "company_form": {
                "title": "Company Information",
                "form": company_forms.CompanyProfileForm()
            },
            "address_form": {
                "title": "Company Address",
                "form": company_forms.CompanyAddressForm()
            },
            "package_form": {
                "title": "Please select package",
                "subtitle": "Please choose a package and enter payment information but you will not be"
                            " charged until the trial ends. You can cancel anytime during trail period.",
                "form": company_forms.CompanyPackageForm()
            },
            "title": "Sign Up"
        }
    }
    return render(request, "accounts/signup.html", context)


def forget_password(request):
    context = {
        "title": "Forget Password",
        "page_title": "Don't worry!",
        "page_subtitle": "We will help you reset your password.",
        "main_btn": {
            "title": "Send Code",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Login",
                "href": account_urls.login_url()
            },
            {
                "title": "Create account",
                "href": "javascript:;"
            }
        ],
        "form": {
            "action": api_urls.get_reset_password_url(),
            "form": account_forms.ForgotPasswordForm(),
            "title": "Please enter your email."
        }
    }
    return render(request, "accounts/multi-steps.html", context)


def enter_code(request, username):
    context = {
        "title": "Enter Code",
        "page_title": "Get the code?",
        "page_subtitle": "",
        "main_btn": {
            "title": "Confirm",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Login?",
                "href": account_urls.login_url()
            },
            {
                "title": "Create account",
                "href": "javascript:;"
            }
        ],
        "form": {
            "action": api_urls.confirm_reset_password_code(username),
            "form": account_forms.CodeForm(),
            "title": "Enter the code you got!"
        }
    }
    return render(request, "accounts/multi-steps.html", context)


def reset_password(request, username, code):
    context = {
        "title": "Login",
        "page_title": "Start with new!",
        "page_subtitle": "Please enter new password you want to set.",
        "main_btn": {
            "title": "Set New Password!",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Login?",
                "href": account_urls.login_url()
            },
            {
                "title": "Create account",
                "href": "javascript:;"
            }
        ],
        "form": {
            "action": api_urls.set_user_password(username, code),
            "form": account_forms.ConfirmResetForm(),
            "title": "Set new password"
        }
    }
    return render(request, "accounts/multi-steps.html", context)


def account_logout(request):
    logout(request)
    return redirect("account-login")


def account_signup(request):
    package = request.GET.get("package", "")
    if request.method == "POST":
        form = account_forms.UserRegisterForm(request.POST)
        password = request.POST['password']
        get_username = request.POST.get('username')
        get_email = request.POST.get('email')

        if account_utils._get_user(username=get_username):
            return JsonResponse(success_response(data={
                "redirect_url": '?message=sorry a user is already registered with this username&success=true'
            }))
        if account_utils._get_user(email=get_email):
            return JsonResponse(success_response(data={
                "redirect_url": '?message=sorry this email id has been registered already&success=true'
            }))

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            user_profile = UserProfile.objects.create(user=user, verification_code=account_utils.random_digits(),
                                                      role="COMPANY")
            user.userprofile.verification_code = account_utils.random_digits()
            code = user.userprofile.verification_code
            user.userprofile.save()
            verification_url = account_urls.verify_email(user.username) + '?code=' + str(code)
            context = {'subject': 'Company Account has been successfully created!',
                       'message': 'Thank you {first_name} for signing up to LimouCloud. As you are new to our system so we need to verify'
                                  ' your email first. Either enter the code <strong>{code}</strong> or click on the link given below to'
                                  ' verify your email. <strong>{link}</strong> '.format(first_name=user.first_name,
                                                                                        code=user.userprofile.verification_code,
                                                                                        link=account_utils.get_full_url(
                                                                                            request,
                                                                                            verification_url)), }

            account_utils._thread_making(send_email, ["Welcome to LimouCloud", context, user])

            return JsonResponse(success_response(data={
                "redirect_url": account_urls.account_signup_step_2(
                    username=user.username) + '?message=A verification mail has been sent to the provided email. You can continue here or go and verify email address&success=true'
            }))
        else:
            return JsonResponse(success_response(data={
                "redirect_url": '?message=Sorry This Username is Invalid&success=true'
            }))
    else:
        form = account_forms.UserRegisterForm()

    context = {

        "title": "Signup",
        "page_title": "Start your journey!",
        "page_subtitle": "Free 30 Day Trial. No Contract. Cancel When You Want.",
        "main_btn": {
            "title": "Next!",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Login?",
                "href": account_urls.login_url()
            },
        ],
        "form": {
            "action": account_urls.account_signup(),
            "form": form,
            "title": "Enter Personal Information (Step 1/4)"
        }
    }
    return render(request, "accounts/login.html", context)


def account_signup_step_2(request, username=None):
    userprofile = UserProfile.objects.get(user__username=username)
    if request.method == "POST":
        company_form = company_forms.CompanyProfileForm(request.POST)
        address_form = company_forms.CompanyAddressForm(request.POST)
        company_address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        if company_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            company: CompanyProfileModel = company_form.save(commit=False)
            company.address = address
            company.userprofile = userprofile
            company.save()
            userprofile.step_count = 2
            userprofile_address = account_models.Address.objects.create(address=company_address, city=city, state=state,
                                                                        zip_code=zip_code)
            userprofile.address = userprofile_address
            userprofile.save()
            employee_models.EmployeeRole.objects.create(title='Manager', company=company)
            employee_models.EmployeeRole.objects.create(title='Dispatcher', company=company)
            employee_models.EmployeeRole.objects.create(title='Driver', company=company)
            user_username = company.userprofile.user.username
        return JsonResponse(success_response(data={
            "redirect_url": account_urls.verify_email(user_username)
        }))
    context = {
        "title": "Signup",
        "page_title": "Start your journey!",
        "page_subtitle": "Free 30 Day Trial. No Contract. Cancel When You Want.",
        "main_btn": {
            "title": "Next!",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Login?",
                "href": account_urls.login_url()
            },
        ],
        "form": {
            "action": "",
            "form": company_forms.CompanyProfileForm(),
            "title": "Enter Company Information (Step 2/4)",
            "extra_form": company_forms.CompanyAddressForm(),
        }
    }
    return render(request, "accounts/login.html", context)


def account_signup_step_3(request, username=None):
    company = CompanyProfileModel.objects.get(userprofile__user__username=username)
    if request.method == "POST":
        form = company_forms.CompanyPackageForm(request.POST)
        if form.is_valid():
            package = form.save()
            company.company_package = package
            company.save()
            userprofile = UserProfile.objects.get(user__username=username)
            userprofile.step_count = 3
            userprofile.save()

        return JsonResponse(success_response(data={
            "redirect_url": account_urls.account_signup_step_4(username)
        }))
    context = {
        "title": "Signup",
        "page_title": "Choose package you need!",
        "page_subtitle": "We require that you choose a package but you will not be "
                         "charged"
                         " until the trial concludes. Remember, you can cancel at any time before the 30 days is up",
        "main_btn": {
            "title": "Next!",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Login?",
                "href": account_urls.login_url()
            },
        ],
        "form": {
            "action": "",
            "form": company_forms.CompanyPackageForm(),
            "title": "Select a package (Step 3/4)",

        }
    }
    return render(request, "accounts/login.html", context)


def account_signup_step_4(request, username=None):
    company = CompanyProfileModel.objects.get(userprofile__user__username=username)
    if request.method == "POST":
        get_user = UserProfile.objects.get(user__username=username)
        check_email_verified = get_user.email_verified
        form = company_forms.PaymentInfoForm(request.POST)
        if form.is_valid():
            card_details = form.save()
            company.card_details = card_details
            company.save()
            userprofile = UserProfile.objects.get(user__username=username)
            userprofile.step_count = 4
            userprofile.save()
            user_username = company.userprofile.user.username

        if check_email_verified == True:

            return JsonResponse(success_response(data={
                "redirect_url": home_urls.index()
            }))
        else:
            return JsonResponse(success_response(data={
                "redirect_url": account_urls.verify_email(user_username)
            }))
    context = {
        "title": "Signup",
        "page_title": "Payment Information!",
        "page_subtitle": "We require payment information but will not charge your credit card until the 30 day trial"
                         " expires.",
        "main_btn": {
            "title": "Finish!",
            "classes": "thm-btn"
        },
        "links": [
            {
                "title": "Login?",
                "href": account_urls.login_url()
            },
        ],
        "form": {
            "action": '',
            "form": company_forms.PaymentInfoForm(),
            "title": "Enter Payment Information (Step 4/4)",
        },
        "extras": [
            render_to_string("extras/cards.html"),
            render_to_string("extras/aggree_terms.html")
        ]
    }
    return render(request, "accounts/login.html", context)


def verify_email(request, user_username):
    if request.method == "POST":
        try:
            code = request.POST['code']
            user_profile = account.get_user_profile(user_username, code)
            if user_profile is not None:
                if user_profile.email_verified:
                    message = 'Email already verified! Please Login to continue'
                    return Response(
                        failure_response({}, message).update({"data": {"redirect_url": account_urls.login_url()}}))

                else:
                    user_profile.email_verified = True
                    user_profile.verification_code = account_utils.random_digits()  # to change code immediately to avoid future attacks
                    user_profile.save()
                    message = "Profile verified successfully! Please Login to continue"
                    # For populating Accounting Chart of accounts
                    user = User.objects.filter(username=user_username).first()
                    init_accounts(user.userprofile.companyprofilemodel)
                    return JsonResponse(success_response(data={
                        "redirect_url": account_urls.login_url(), 'message': message
                    }))
            else:
                message = "invalid 4-digit code"
                return JsonResponse(failure_response({}, message))
        except UserProfile.DoesNotExist:
            message = "invalid 4-digit code"
            return JsonResponse(failure_response({}, message))
    elif request.method == "GET":
        code = request.GET.get('code')
        if code:
            try:
                user_profile = account.get_user_profile(user_username, code)
                user_profile.email_verified = True
                user_profile.verification_code = account_utils.random_digits()  # to change code immediately to avoid future attacks
                user_profile.save()
            except:
                context = {
                    "title": "already verified",
                    "page_title": "you have verified from this account! please login to continue",
                    "page_subtitle": "Email already Verified.!",
                    "links": [
                        {
                            "title": "Login?",
                            "href": account_urls.login_url()
                        },
                    ],
                }
                return render(request, "accounts/multi-steps.html", context)
            return redirect(account_urls.login_url())
    context = {
        "title": "email verify",
        "page_title": "Congrats! you have successfully signed up!",
        "page_subtitle": "Email Verification plays an important role to filter out really genuine candidates among spammers.! ",
        "main_btn": {
            "title": "Verify and login!",
            "classes": "thm-btn"
        },
        "form": {
            "action": '',
            "form": account_forms.CodeForm(),
            "title": "Enter Your 4-Digit Verification Code here",
        },
    }
    return render(request, "accounts/multi-steps.html", context)


def company_account_create(request):
    if request.method == "POST":
        user_form = account_forms.UserRegisterForm(request.POST)
        company_form = company_forms.CompanyProfileForm(request.POST)
        address_form = company_forms.CompanyAddressForm(request.POST)
        package_form = company_form.CompanyPackageForm(request.POST)

    else:
        user_form = account_forms.UserRegisterForm()
        company_form = company_forms.CompanyProfileForm()
        address_form = company_forms.CompanyAddressForm()
        package_form = company_form.CompanyPackageForm()

    context = {
        "page_title": "Start Your Journey",
        "back_url": "",
        "user_form": user_form,
        "action": "",  # leave empty for same view
        "form_steps": [
            {
                "title": "Account Information",
                "icon": "fa fa-lock",
                "forms": [user_form],
                "active": True,
                "actions": [

                    {
                        "title": "Next",
                        "classes": "next btn btn-primary",
                        "type": "submit"
                    }
                ]
            },
            {
                "title": "Personal Information",
                "forms": [company_form, address_form],
                "icon": "fa fa-person",
                "actions": [
                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info",
                        "type": "button"
                    },
                    {
                        "title": "Submit",
                        "classes": "next btn btn-primary action-button",
                        "type": "submit"
                    }
                ]
            }
        ],
    }
    return render(request, "accounts/multi-steps.html", context)


from Merchants.stripe import utils as stripe_utils


def create_company_account(request):
    user_form = account_forms.UserRegisterForm(request.POST or None)
    company_form = company_forms.CompanyProfileForm(request.POST or None)
    address_form = company_forms.CompanyAddressForm(request.POST or None)
    package_form = company_forms.CompanyPackageForm(request.POST or None)
    payment_form = company_forms.PaymentInfoForm(request.POST or None)
    if request.method == "POST":
        if payment_form.is_valid() and user_form.is_valid() and company_form.is_valid() and package_form.is_valid():
            if account_utils._get_user(email=request.POST.get("email")):
                return JsonResponse(
                    failure_response(msg="A user with email already exists"))
            payment = stripe_utils.create_payment_method(payment_form.cleaned_data)
            if not payment.get("success", False):
                return JsonResponse(
                    failure_response(msg=payment.get("message", "Something went wrong with payment processing")))
            # try:
            user = user_form.save()
            user.set_password(request.POST.get("password"))
            user.save()

            user_profile = account_utils.create_user_profile(user)
            package = account_utils.create_package(package_form)
            company = account_utils.create_company(address_form, company_form, user_profile, package)
            employee_models.EmployeeRole.objects.create(title='Manager', company=company)
            employee_models.EmployeeRole.objects.create(title='Dispatcher', company=company)
            employee_models.EmployeeRole.objects.create(title='Driver', company=company)
            merchant_account = stripe_utils.create_stripe_merchant_account(company)
            stripe_utils.attach_payment_method_to_client(payment.get("payment_id"), merchant_account)
            verification_url = account_urls.verify_email(user.username) + '?code=' + str(
                user_profile.verification_code)
            account_utils.send_welcome_email(request, company, verification_url)
            return JsonResponse(success_response(msg="Account created successfully!", data={
                "redirect_url": "{}?message=Check your email for verification code!&success=true".format(
                    account_urls.verify_email(user.username))
            }))
            # except:
            #     return JsonResponse(failure_response(msg="Error creating account, Please contact administration!"))
        else:
            errors = "{}{}{}{}".format(user_form.errors.__str__(), company_form.errors, package_form.errors,
                                       payment_form.errors)

            return JsonResponse(failure_response(msg="{}".format(errors)))
    else:
        selected_package = request.GET.get("package", "")
        active_packages = Package.objects.filter(is_active=True)
        if selected_package:
            selected_package = active_packages.filter(slug__iexact=selected_package).first()
        package_form = company_forms.CompanyPackageForm(initial={"package": selected_package})
        package_form.fields["package"].queryset = active_packages
    context = {
        "page_title": "Start Your Journey",
        "page_subtitle": "Free 30 Day Trial. No Contract. Cancel When You Want.",
        "back_url": "",
        "user_form": user_form,
        "action": "",  # leave empty for same view
        "forms": [
            {
                "title": "Account Information",
                "icon": "fa fa-lock",
                "sub_forms": [user_form],
                "active": True,

            },
            {
                "title": "Company Information",
                "sub_forms": [company_form, address_form],
                "icon": "fa fa-person",

            }, {
                "title": "Package (<small><a target='_blank' href='{}#pricing' class=''>Compare Packages</a></small>)".format(
                    reverse("index2")),
                "sub_forms": [package_form],
                "icon": "fa fa-person",
                "extras": [

                    "<small class='text-white'>We require that you choose a package and enter payment information but you"
                    " will not be charged until the trial concludes. Remember, you can cancel at any time before the 30"
                    " days is up.</small>",
                    render_to_string("extras/aggree_terms.html", {"terms_url": reverse("terms-and-conditions")}),
                ]

            }, {
                "title": "Payment Information",
                "sub_forms": [payment_form],
                "icon": "fa fa-person",

            }
        ],
        "main_btn": {
            "classes": "thm-btn",
            "title": "Submit"
        }
    }
    return render(request, "accounts/signup.html", context)
