from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm as BaseSetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Url


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'id': 'floatingInputUsername',
                                      'placeholder': 'myusername'})
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'id': 'floatingInputEmail',
                                       'placeholder': 'name@example.com'})
    )
    password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'id': 'floatingPassword',
                                          'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'id': 'floatingPasswordConfirm',
                                          'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError("A user with this email already exists.")


class LoginUserForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'id': 'floatingInputUsername',
                                      'placeholder': 'myusername'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'id': 'floatingPassword',
                                          'placeholder': 'Password'})
    )


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'floatingInputEmail',
                                       'placeholder': 'name@example.com', 'autocomplete': 'email'})
    )


class SetPasswordForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'floatingPassword',
                                          'placeholder': 'Password', "autocomplete": "new-password"})
    )

    new_password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'floatingPasswordConfirm',
                                          'placeholder': 'Confirm Password', "autocomplete": "new-password"})
    )


class CreateUrlForm(forms.ModelForm):
    full_url = forms.URLField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the link here'})
    )

    class Meta:
        model = Url
        fields = ['full_url']
