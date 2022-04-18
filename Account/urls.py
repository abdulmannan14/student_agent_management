from django.urls import path, reverse
from . import views as account_views

urlpatterns = [
    path('', account_views.user_login, name="account-login"),
    path('login', account_views.user_login, name="account-login"),
    path('logout', account_views.account_logout, name="account-logout"),
    path('sign-up', account_views.company_register, name="account-signup"),
    path('register-old', account_views.account_signup, name="account-signup-1"),
    path('register', account_views.create_company_account, name="company-register"),
    path('verify/email/<str:user_username>', account_views.verify_email, name="verify-email"),
    path('register-step-2/<str:username>', account_views.account_signup_step_2, name="account-signup-2"),
    path('register-step-3/<str:username>', account_views.account_signup_step_3, name="account-signup-3"),
    path('register-step-4/<str:username>', account_views.account_signup_step_4, name="account-signup-4"),
    path('forget-password/', account_views.forget_password, name="account-forget-password"),
    path('reset-password/<str:username>/<int:code>', account_views.reset_password, name="account-reset-password"),
    path('enter-code/<str:username>', account_views.enter_code, name="account-enter-reset-password-code"),

]


def verify_email(user_username):
    return reverse("verify-email", kwargs={"user_username": user_username})


def login_url():
    return reverse("account-login")


def forget_password():
    return reverse("account-forget-password")


def reset_password(username, code):
    return reverse("account-reset-password", kwargs={"username": username, "code": code})


def reset_password_code(username):
    return reverse("account-enter-reset-password-code", kwargs={"username": username})


def account_logout():
    return reverse("account-logout")


def account_signup():
    return reverse("company-register")


def account_signup_step_2(username):
    return reverse("account-signup-2", kwargs={"username": username})
    # return reverse("account-signup")


def account_signup_step_3(username):
    return reverse("account-signup-3", kwargs={"username": username})


def account_signup_step_4(username):
    return reverse("account-signup-4", kwargs={"username": username})
