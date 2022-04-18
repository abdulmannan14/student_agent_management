from .models import User, UserProfile
from limoucloud_backend import utils as lc_utils


def get_user_profile(username=None, code=None, email=None):
    try:
        if username and code:
            return UserProfile.objects.get(user__username=username, verification_code=code)
        if email and code:
            return UserProfile.objects.get(user__email=email,verification_code=code)
        if username:
            return UserProfile.objects.get(user__username=username)
        if email:
            return UserProfile.objects.get(user__email=email)
        if code:
            return UserProfile.objects.get(verification_code=code)

        lc_utils.logger("Username or email not provided!")
        return None
    except UserProfile.DoesNotExist as exep:
        lc_utils.logger(str(exep))
        return None


def get_user(username: str = None, email: str = None):
    try:
        if username:
            return User.objects.get(username=username.lower())
        if email:
            return User.objects.get(email=email.lower())
        lc_utils.logger("Username or email not provided!")
        return None
    except User.DoesNotExist as exep:
        lc_utils.logger(str(exep))
        return None
