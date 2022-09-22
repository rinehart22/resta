from . models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# class LocationForm(ModelForm)


class SignupForm(UserCreationForm):
    mobile = forms.IntegerField(required=True, label="mobile")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'mobile']


class ChefForm(ModelForm):
    class Meta:
        model = Chef
        fields = '__all__'


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'


# class SignupForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email','password1', 'password2']
