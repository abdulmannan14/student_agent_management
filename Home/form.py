from django import forms
from Home.models import Comment, Subscription


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'


class SubscriptionsForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'
