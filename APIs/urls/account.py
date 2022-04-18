from django.urls import path
from Account import views_api as account_views

urlpatterns = [
    path("forget-password/", account_views.reset_password),
    path("reset-password/", account_views.reset_password),  # kept same for url name confusion
    path("reset-password/enter-code/<str:username>/", account_views.confirm_reset_password_code),
    path("reset-password/set-new/<str:username>/<int:code>/", account_views.set_user_password),
    path("update-profile/", account_views.update_user_profile),
    path("settings/update/", account_views.user_settings),
]
