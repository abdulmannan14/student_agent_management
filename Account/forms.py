from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'data_icon': 'fa fa-user', "required": ""}),
            'last_name': forms.TextInput(attrs={'data_icon': 'fa fa-user', "required": ""}),
            'username': forms.TextInput(attrs={'data_icon': 'fa fa-user', "required": ""}),
            'email': forms.TextInput(attrs={'data_icon': 'fa fa-at', "required": "", "type": "email"}),
            'password': forms.TextInput(attrs={'data_icon': 'fa fa-key', "required": "", "type": "password"}),
        }


class AuthForm(forms.Form):
    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'data_icon': 'fa fa-user'}))
    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'data_icon': 'fa fa-key'}))

    class Meta:
        fields = [
            'username',
            'password'
        ]


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True,
                             widget=forms.TextInput(attrs={'data_icon': 'fa fa-envelope', 'type': "email"}))

    class Meta:
        fields = [
            'email',
        ]


class ConfirmResetForm(forms.Form):
    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'data_icon': 'fa fa-lock'}))
    confirm_password = forms.CharField(max_length=100, required=True,
                                       widget=forms.PasswordInput(attrs={'data_icon': 'fa fa-lock'}))

    class Meta:
        fields = [
            'password',
            'confirm_password'
        ]


class CodeForm(forms.Form):
    code = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={'data_icon': 'fa fa-hashtag'}))

    class Meta:
        fields = [
            'code'
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True,
                            widget=forms.TextInput(attrs={"type": "email", "col_cls": "col-md-8", "email": "true"}))
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
