from django.urls import path
from APIs.views import client as client_views

urlpatterns = [
    path("reservation", client_views.post_reservation),
    path("add_card", client_views.add_client_card, name='add_client_card'),
    path("all_cards", client_views.get_client_cards, name='add_client_card'),
    path("register_client", client_views.register_client, name='register_client'),
    path("verify_client_email", client_views.verify_email, name='verify_email_client'),
]
