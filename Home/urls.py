from django.urls import path
from Home.views import *

urlpatterns = [
    path('index1', index, name='index'),
    path('', index2, name='index2'),
    path('404', handler404, name='404'),
    path('500', handler500, name='500'),
    path('contact', contact, name='contact'),
    path('about', about, name='about'),
    path('features', features, name='features'),
    path('terms-and-conditions', terms_and_conditions, name='terms-and-conditions'),
]


def index():
    return reverse("index")
