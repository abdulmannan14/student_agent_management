import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html

from .utils import create_payment_intent
from Client import models as client_models
from . import tables as stripe_tables


def list_client_cards(request, pk):
    client = client_models.PersonalClientProfileModel.objects.get(pk=pk)
    if not client.merchant_account or not client.merchant_account.stripe_id:
        client.create_stripe_merchant_account()
    cards = stripe.PaymentMethod.list(customer=client.merchant_account.stripe_id, type="card").get("data", [])
    query_set = []
    for card in cards:
        query_set.append({
            "pk": pk,
            "id": card.get("id", ""),
            "card_holder": card.get("billing_details", {}).get("name", ""),
            "card_no": "{}".format(card.get("card", {}).get("last4", "")),
            "expires_at": "{}/{}".format(card.get("card", {}).get("exp_month", ""),
                                         card.get("card", {}).get("exp_year", "")),
            "brand": card.get("card", {}).get("brand", ""),
            "customer_id": card.get("customer", "")
        })

    table = stripe_tables.PaymentMethodTable(query_set)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Card",
                "href": "javascript:;",
                "icon": "fa fa-plus",
                "attrs": format_html(
                    'data-toggle="modal" data-target="#detailModal" data-url="{}" data-name="{}"'.format(
                        reverse("stripe-add-card", kwargs={'pk': pk}), "Enter card details"))
            },
        ],
        'count': 1,
        "page_title": "{}'s Cards".format(client.name),
        'table': table,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['clients'],
        },
    }
    return render(request, "dashboard/list-entries.html", context=context)


def add_card(request, pk):
    client = client_models.PersonalClientProfileModel.objects.get(pk=pk)
    if client.merchant_account and client.merchant_account.stripe_id:
        stripe_customer_id = client.merchant_account.stripe_id
    else:
        stripe_customer_id = client.create_stripe_merchant_account().stripe_id
    intent = create_payment_intent(customer_id=stripe_customer_id, amount=500)
    context = {
        "client_secret": intent.client_secret,
        "public_key": settings.STRIPE_PUBLIC_KEY,
        "webhook": "{}://{}{}".format(request.scheme, request.get_host(),
                                      reverse("stripe-add-card-success", kwargs={"pk": pk}))
    }
    return render(request, "merchant/add_card.html")


def add_success(request, pk):
    payment_method_id = request.GET.get("payment_method_id", "")
    client = client_models.PersonalClientProfileModel.objects.get(pk=pk)
    if payment_method_id:
        stripe.PaymentMethod.attach(payment_method_id, customer=client.merchant_account.stripe_id)
        return redirect(reverse("stripe-client-cards", kwargs={"pk": pk}))
    else:
        return JsonResponse({
            "client": client.name,
            "payment_method_add": "failure",
            "payment_id": payment_method_id
        }, safe=False)


def delete_card(request, pk, customer_id, card_id):
    resp = stripe.PaymentMethod.detach(card_id)
    if resp.get("deleted", False):
        return redirect(reverse("stripe-client-cards", kwargs={"pk": pk}))
    else:
        return redirect(reverse("stripe-client-cards", kwargs={"pk": pk}))


def success(request, pk):
    client = client_models.PersonalClientProfileModel.objects.get(pk=pk)
    return JsonResponse({
        "client_id": client.pk,
        "payment": "success"
    }, safe=False)
