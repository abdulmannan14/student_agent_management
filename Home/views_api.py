from rest_framework.decorators import api_view
from rest_framework.response import Response
from Home.models import *
from Home.serializers import *
from limoucloud_backend.utils import *


@api_view(['POST'])
def subscription(request):
    if request.method == 'POST':
        serializer = SubscriptionsSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.save()
            context = {
                'message': 'Subscription Success. Thank You for subscribing to LimouCloud. We will keep you updated.'
            }
            send_email('Welcome To LimouCloud', context, email)
            return Response(success_response(serializer.data, msg='Successfully subscribed!'))
        else:
            return Response(failure_response(serializer.errors, msg='This Email Already Subscribed, Try another one!'))
    else:
        return Response(failure_response('Bad Request!'))


@api_view(['POST'])
def create_comment(request):
    if request.method == 'POST':
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, msg='We have recorded your words, will get back to you!'))
        else:
            return Response(failure_response(serializer.errors, msg="Please fill out all fields!"))
    else:
        return Response(failure_response('Bad Request'))
