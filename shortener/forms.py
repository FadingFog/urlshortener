from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Url


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'floatingInputUsername',
                                                             'placeholder': 'myusername'}))
    email = forms.EmailField(max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'id': 'floatingInputEmail',
                                                            'placeholder': 'name@example.com'}))

    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': 'floatingPassword',
                                                                  'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': 'floatingPasswordConfirm',
                                                                  'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
