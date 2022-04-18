from django.urls import path
from Home.views_api import *

urlpatterns = [
    path('home/subscibe', subscription, name='subscription'),
    path('home/comment', create_comment, name='create-comment')
]
