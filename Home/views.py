from django.shortcuts import render, redirect
from django.urls import reverse

from Company.models import Package
from Home.form import CommentsForm, SubscriptionsForm
from Company import models as company_models


# Create your views here.


def index(request):
    user = request.user
    is_company = user.is_authenticated and user.userprofile.role == user.userprofile.COMPANY

    context = {
        'title': 'LimouCloud',
        'active_home': 'active',
        'navbarbar': 'navnavhome',
        'contact_page_url': reverse('contact'),
        'home_page_url': reverse('index'),
        'about_page_url': reverse('about'),
        'features_page_url': reverse('features'),
        'company_authentication': is_company,
    }

    return render(request, 'index.html', context)


def index2(request):
    user = request.user
    # is_company = user.is_authenticated and user.userprofile.role == user.userprofile.COMPANY
    packages = Package.objects.filter(is_active=True)
    monthly_packages = packages.filter(pricing_duration=Package.MONTHLY)
    yearly_packages = packages.filter(pricing_duration=Package.YEARLY)
    context = {
        'title': 'LimouCloud',
        'active_home': 'active',
        'navbarbar': 'navnavhome',
        'contact_page_url': reverse('contact'),
        'home_page_url': reverse('index'),
        'about_page_url': reverse('about'),
        'features_page_url': reverse('features'),
        # 'company_authentication': company_authenticationis_company,
        'monthly_packages': monthly_packages,
        'yearly_packages': yearly_packages,
    }

    return render(request, 'home/index.html', context)


def contact(request):
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create-comment')
    else:
        form = CommentsForm()
    context = {
        'title': 'Contact',
        'active_contact': 'active',
        'navbar_active': 'active',
        'contact_page_url': reverse('contact'),
        'home_page_url': reverse('index'),
        'about_page_url': reverse('about'),
        'features_page_url': reverse('features')
    }
    return render(request, 'contact.html', context)


def about(request):
    context = {
        'title': 'About',
        'active_about': 'active',
        'navbar_active': 'active',
        'contact_page_url': reverse('contact'),
        'home_page_url': reverse('index'),
        'about_page_url': reverse('about'),
        'features_page_url': reverse('features')
    }
    return render(request, 'about.html', context)


def features(request):
    context = {
        'title': 'Features',
        'active_features': 'active',
        'navbar_active': 'active',
        'contact_page_url': reverse('contact'),
        'home_page_url': reverse('index'),
        'about_page_url': reverse('about'),
        'features_page_url': reverse('features')
    }
    return render(request, 'features.html', context)


def terms_and_conditions(request):
    context = {
        'page_title': 'Terms and Conditions',
        'active_features': 'active',
        'navbar_active': 'active',

    }
    return render(request, 'home/terms-and-conditions.html', context)


def handler404(request, exception=None):
    context = {
        "img": "/staticfiles/assets/img/page404 updated.png",
        "page_title": "Looks like you lost the way!",
        "links": [
            {
                "href": reverse("index2"),
                "title": "Take me home"
            }
        ]
    }
    response = render(request, "home/error.html", context=context)
    response.status_code = 404
    return response


def handler500(request, exception=None):
    context = {
        "page_title": "We are sorry!",
        "img": "/staticfiles/assets/img/500page.png",
        "links": [
            {
                "href": reverse("index2"),
                "title": "Take me home"
            }
        ]
    }
    response = render(request, "home/error.html", context=context)
    response.status_code = 500
    return response
