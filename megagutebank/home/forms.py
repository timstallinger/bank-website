from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Account, SavingsAccount

class SignUpForm(UserCreationForm):
    vorname = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Vornamen eingeben',
            }))
    nachname = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nachnamen eingeben',
            }))
    email = forms.EmailField(max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-Mail Adresse eingeben',
            }))
    username = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Benutzernamen eingeben',
            }))
    password1 = forms.CharField(max_length=30, required=True, help_text='Mindestens 8 Zeichen lang und darf nicht zu einfach sein.',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Passwort eingeben',
            }))
    password2 = forms.CharField(max_length=30, required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Passwort bestätigen',
            }))
    class Meta:
        model = User
        fields = ('vorname', 'nachname', 'email', 'username', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data["vorname"]
        user.last_name = self.cleaned_data["nachname"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


konto_typen = [
    ('sparkonto', 'Sparkonto'),
    ('girokonto', 'Girokonto'),
    ('kreditkartenkonto', 'Kreditkartenkonto'),
    ]

class KontoForm(ModelForm):
    konto_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kontonamen eingeben',
            }))
    konto_typ = forms.CharField(max_length=30, required=True, widget=forms.Select(choices=konto_typen, attrs={
        'class': 'btn btn-primary dropdown-toggle',
    }))

    class Meta:
        model = SavingsAccount
        fields = ('konto_name', )
    def save(self, commit=True):
        konto = super(KontoForm, self).save(commit=False)
        kontotyp = self.cleaned_data["konto_typ"]
        konto.name = self.cleaned_data["konto_name"]
        konto.amount = 0
        konto.interestrate = 0
        if commit:
            konto.save()
        return konto