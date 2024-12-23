from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-group'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-group'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-group'}))
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-group'}))
    password1 = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-group'}))
    password2 = forms.CharField(label="Повторите пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-group'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')