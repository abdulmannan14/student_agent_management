from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404
import datetime
import Menu.models
from limoucloud_backend import utils as backend_utils
from Restaurant import models as restaurant_models
from Menu import models as menu_models
from limoucloud_backend.utils import success_response_fe
from . import tables as expense_table, forms as expense_form, models as restaurant_models


# Create your views here.


def customer_main_view(request):
    print("hello=======================")
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    restaurant_name = restaurant.name

    context = {
        'welcome': f'Welcome to {restaurant.name}',
        'view_menu': 'Menu',
        'get_bill': 'Get Bill',
        'call_waiter':'Call A Waiter',
        'call_waiter_url':reverse('call-a-waiter'),
    }
    return render(request, "company/customer_main.html", context)





def customer_menu_view(request):
    print("hello=======================")
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    restaurant_name = restaurant.name
    all_menu = []
    menu_head = menu_models.MenuHead.objects.filter(restaurant=restaurant)
    menu_item = menu_models.MenuItem.objects.filter(restaurant=restaurant)
    print("this is meanu head===================", menu_head)
    print("this is meanu item===================", menu_item)
    for head in menu_head:
        all_menu.append(menu_item.filter(menu_head=head))
    print("this is ========================", all_menu)

    context = {
        'welcome': f'Welcome to {restaurant.name}',
        'menu_head': menu_head,
        'all_menu': all_menu,
        'nav_conf': {
            'active_classes': ['restaurant'],
        },
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        # 'button': 'OK'

    }
    return render(request, "company/customer_main.html", context)



def get_bill(request):
    messages.success(request, "Waiter Called at your table, please wait!")
    print("okay----------==============")
    return redirect('restaurant-customer-main-view')