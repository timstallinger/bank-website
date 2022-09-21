from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
import random
import datetime

from .models import Person, Account, Transaction

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
    username = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Benutzernamen eingeben',
            }))
    email = forms.EmailField(max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-Mail Adresse eingeben',
            }))
    phone = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Telefonnummer eingeben',
            }))
    address = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Adresse eingeben',
            }))
    birthday = forms.DateField(initial=datetime.date.today, 
    widget=forms.widgets.DateInput(
        attrs={
            'type': 'date', 'class': 'form-control','min': '1900-01-01', 'max': datetime.date.today() - datetime.timedelta(days=18*365)
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
        model = Person
        fields = ('vorname', 'nachname', 'email', 'phone', 'username', 'birthday', 'password1', 'password2', )

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
typ_to_int = {
            'sparkonto': 0,
            'girokonto': 1,
            'kreditkartenkonto': 2,
        }
konto_cntry = [
    ('DE', 'Deutschland'),
    ('CH', 'Schweiz'),
    ('ES', 'Spanien'),
    ]

class KontoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ModelForm, self).__init__(*args, **kwargs)
    
    konto_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kontonamen eingeben',
            }))
    konto_typ = forms.CharField(max_length=30, required=True, widget=forms.Select(choices=konto_typen, attrs={
        'class': 'btn btn-primary dropdown-toggle',
    }))
    konto_standort = forms.CharField(max_length=30, required=True, widget=forms.Select(choices=konto_cntry, attrs={
        'class': 'btn btn-primary dropdown-toggle',
    }))

    class Meta:
        model = Account
        fields = ('konto_name', 'konto_standort')
    def save(self, commit=True):
        konto = super(KontoForm, self).save(commit=False)
        konto.name = self.cleaned_data["konto_name"]
        konto.amount = 0
        konto.interestrate = 0
        # generate a random IBAN
        konto.iban = self.cleaned_data["konto_standort"] + str(random.randint(1000000000, 9999999999))
        
        konto.type = typ_to_int[self.cleaned_data["konto_typ"]]
        konto.owner = self.user

        if commit:
            konto.save()
        return konto

class UberweisungForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ModelForm, self).__init__(*args, **kwargs)
    # amount of money to transfer
    betrag = forms.DecimalField(max_digits=10, decimal_places=2, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Betrag eingeben',
            }))
    zielkonto = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Zielkonto eingeben',
            }))
    verwendungszweck = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Verwendungszweck eingeben',
            }))
    
    class Meta:
        model = Transaction
        fields = ('betrag', 'zielkonto', 'verwendungszweck',)

    def save(self, request, commit=True):
        konto = super(UberweisungForm, self).save(commit=False)
        konto.amount = self.cleaned_data["betrag"]
        konto.verwendungszweck = self.cleaned_data["verwendungszweck"]
        konto.sender = self.user
        konto.senderkonto =  request.POST.dict().get("senderkonto")
        konto.receiver = self.cleaned_data["zielkonto"]

        if commit:
            konto.save()
        return konto