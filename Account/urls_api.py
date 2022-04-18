from django.urls import path
from Account.views_api import *
from Account.api_views.user_auth import views as login_api
from Account.api_views.work_status import views as work_status_views

urlpatterns = [
    path('login', login_api.LoginApi.as_view(), name='login'),
    path('logout/', login_api.LogoutApi.as_view(), name='logout'),
    path('sendverificationcode/', login_api.SendVerificationCode.as_view(), name='send_verification_code'),
    path('emailverify/', login_api.EmailVerify.as_view(), name='email_verify'),
    path('verifyresetpassword/<str:email>/', login_api.VerifyResetPasswordCode.as_view(), name='verify_reset_password'),
    path('createnewpassword/<int:code>/', login_api.CreateNewPassword.as_view(), name='create_new_password'),
    path('changepassword/', login_api.ChangePassword.as_view(), name='change_password'),
    path('editprofile/', login_api.EditProfile.as_view(), name='edit_profile'),
    # ===================Work Status ===============================
    path('workstatus/', work_status_views.WorkStatus.as_view(), name='work-status'),
    # ===================Frontend Views Path  =======================

    path('user/register', register_user, name='register-user'),
    path('user/login/', user_login, name='user-login'),
    path('user/<str:username>/send-verification-code', send_verification_code, name="send-verification-code"),
    path('user/<str:username>/<int:code>', verify_email, name='email-verify'),
    path('user/reset-password', reset_password, name='reset-password'),
    path('user/confirm-reset-password-code/<str:username>/<int:code>', confirm_reset_password_code,
         name='confirm-reset-password-code'),
    path('user/set-user-password/<str:username>/<int:code>', set_user_password,
         name='set-user-password')
]


def get_login_url():
    return reverse("user-login")


def get_register_url():
    return reverse("register-user")


def get_verify_email_url(username, code):
    return reverse("email-verify", kwargs={"username": username, "code": code})


def get_reset_password_url():
    return reverse("reset-password")


def send_verification_code(username):
    return reverse("send-verification-code", kwargs={"username": username})


def set_user_password(username, code):
    return reverse("set-user-password", kwargs={"username": username, "code": code})


def confirm_reset_password_code(username, code=0):
    return reverse("confirm-reset-password-code", kwargs={"username": username, "code": code})
