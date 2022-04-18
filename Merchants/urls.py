from django.urls import path
from .stripe import views as stripe_views

urlpatterns = [
    path("", stripe_views.list_client_cards, name="stripe-client-cards"),
    path("add", stripe_views.add_card, name="stripe-add-card"),
    path("add/success", stripe_views.add_success, name="stripe-add-card-success"),
    path("delete/<str:customer_id>/<str:card_id>", stripe_views.delete_card, name="stripe-card-delete"),
    # path("add/success", stripe_views.success, name="stripe-add-card-success"),
]
