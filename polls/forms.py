from django import forms
from django.core.exceptions import ValidationError

from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({'password2': 'Пароли не совпадают'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('avatar', 'username')

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UpdateForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватарка', required=False)
    username = forms.CharField(label='Логин', required=False)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password or password2:
            if password != password2:
                raise ValidationError({'password2': 'Пароли не совпадают'})

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('avatar', 'username')