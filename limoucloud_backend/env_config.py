import os

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "LC-TEST-SECRET.KEY")
if not SECRET_KEY:
    raise Exception("Please add SECRET_KEY in .env")

# EMAIL_USE_TLS = True
# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = os.getenv("EMAIL_PORT")

# from_email = EMAIL_HOST_USER
# admin_email = os.getenv("ADMIN_EMAIL")

LOGIN_URL = os.getenv("LOGIN_URL", "/account/login")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
LC_TRAIL_PERIOD = int(os.getenv("LC_TRAIL_PERIOD", 0))
