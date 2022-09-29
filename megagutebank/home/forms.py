from sqlite3 import IntegrityError
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
import random
import datetime

from .models import Person, Account, TagesgeldAccount, Transaction

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
        error_messages={'invalid': 'Bitte geben Sie eine gültige E-Mail-Adresse ein.'},
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
        fields = ('vorname', 'nachname', 'email', 'phone','username', 'birthday', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data["vorname"]
        user.last_name = self.cleaned_data["nachname"]
        user.email = self.cleaned_data["email"]
        user.address = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone"]
        check_user = self.cleaned_data["username"]
        check_user = Person.objects.filter(username=check_user)
        if check_user.exists():
            raise forms.ValidationError("Dieser Username ist bereits vergeben.")
        user.confirmed = False
        if commit:
            user.save()
        return user


konto_typen = [
    ('sparkonto', 'Sparkonto'),
    ('girokonto', 'Girokonto'),
    ('Tagesgeldkonto', 'Tagesgeldkonto'),
    ]
typ_to_int = {
        'sparkonto': 0,
        'girokonto': 1,
        'Tagesgeldkonto': 2,
    }
konto_cntry = [
    ('DE', 'Deutschland'),
    ('CH', 'Schweiz'),
    ('ES', 'Spanien'),
    ]
dauerauftrag_options = [
    ('days', 'Tage'),
    ('months', 'Monate'),
    ('years', 'Jahre'),
    ]
tagesgeld_options = [
    ('1', '1 Jahr'),
    ('3', '3 Jahre'),
    ('5', '5 Jahre'),
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
    tagesgeld_dauer = forms.CharField(max_length=30, required=False, widget=forms.Select(choices=tagesgeld_options, attrs={
        'class': 'btn btn-primary dropdown-toggle',
    }))
    tagesgeld_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, 
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Betrag eingeben',
            }))
    
    class Meta:
        model = Account
        fields = ('konto_name', 'konto_standort')

    def gen_iban(self, cntry):
        blz_fill = 100100500000000000
        account_nr = random.randint(1, 9999999999)
        temp_iban = blz_fill + account_nr
        checksum = 98 - (int(str(temp_iban) + str(131400)) % 97)

        if checksum < 10:
            iban = f"{cntry}0{checksum}{temp_iban}"
        else:
            iban = f"{cntry}{checksum}{temp_iban}"
        return iban

    def save(self, commit=True):
        konto = super(KontoForm, self).save(commit=False)
        konto.name = self.cleaned_data["konto_name"]
        konto.amount = 0
        konto.interestrate = 0
        # generate valid iban
        konto.iban = self.cleaned_data["konto_standort"] + str(10010005) + str(random.randint(1000000000, 9999999999))

        self.gen_iban(self.cleaned_data["konto_standort"])

        konto.type = typ_to_int[self.cleaned_data["konto_typ"]]
        konto.owner = self.user

        if konto.type == 0:
            konto.interest = 0.0365
            konto.negative_interest = 0.073
        elif konto.type == 1:
            if konto.time_period == 1:
                konto.interest = 0.050
            if konto.time_period == 3:
                konto.interest = 0.070
            if konto.time_period == 5:
                konto.interest = 0.100

        if commit:
            konto.save()
        return konto

class TagesgeldForm(KontoForm):
    class Meta:
        model = TagesgeldAccount
        fields = ('konto_name', 'konto_standort', 'tagesgeld_dauer')
    def save(self, commit=True):
        konto = super(TagesgeldForm, self).save(commit=False)
        konto.name = self.cleaned_data["konto_name"]
        amount = self.cleaned_data["tagesgeld_amount"]
        if not amount:
            konto.amount = 0
        else:
            konto.amount = amount
        konto.interestrate = 0
        konto.time_period = self.cleaned_data["tagesgeld_dauer"]
        # generate valid iban
        konto.iban = self.cleaned_data["konto_standort"] + str(10010005) + str(random.randint(1000000000, 9999999999))

        self.gen_iban(self.cleaned_data["konto_standort"])

        konto.type = typ_to_int[self.cleaned_data["konto_typ"]]
        konto.owner = self.user
        giro = None
        if konto.type == 0:
            konto.interest = 0.0365
            konto.negative_interest = 0.073
        elif konto.type == 1:
            konto.interest = 0
        elif konto.type == 2:
            # Tagesgeldkonto
            giro = Account.objects.get(owner=self.user, type=1)
            if giro.amount < konto.amount:
                return 0
            giro.amount -= float(konto.amount)
            konto.interest = 0
        
        if commit:
            konto.save()
            if giro:
                giro.save()
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
    betrag.label = 'Betrag in Euro'
    zielkonto = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Zielkonto eingeben',
            }))
    empfangername = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Empfängername eingeben',
            }))
    empfangername.label="Empfängername"
    verwendungszweck = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Verwendungszweck eingeben',
            }))
    dauerauftrag = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'style': 'margin-top: 30px;',
    }))
    zeit_input = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class':"form-control",
    }))
    zeit_input.label="Dauerauftrag Zeitabstand in Tagen"

    class Meta:
        model = Transaction
        fields = ('betrag', 'zielkonto', 'verwendungszweck',)

    def save(self, request, commit=True):
        sending_account = request.POST.dict().get("senderkonto")
        sending_account = Account.objects.get(pk=sending_account)

        transaction = super(UberweisungForm, self).save(commit=False)
        transaction.amount = self.cleaned_data["betrag"]
        transaction.usage = self.cleaned_data["verwendungszweck"]
        transaction.sending_account = sending_account
        transaction.receiving_account = self.cleaned_data["zielkonto"]
        transaction.receiving_name = self.cleaned_data["empfangername"]
        transaction.standing_order = self.cleaned_data["dauerauftrag"]
        transaction.time_of_transaction = timezone.now()
        if transaction.standing_order:
            transaction.standing_order_days = self.cleaned_data["zeit_input"]

        if sending_account.amount + sending_account.overdraft < transaction.amount:
            # Falls Konto nicht ausreichend gedeckt ist, abbrechen
            return 0
        sending_account.amount -= float(transaction.amount)

        # Wenn das Zielkonto auf unserer Datenbank existiert, bekommt der Empfänger das Geld
        # Ansonsten wird das Geld nicht überwiesen, aber die Transaktion wird erstellt
        try:
            receiver = Account.objects.get(iban=transaction.receiving_account)
        except Account.DoesNotExist:
            receiver = sending_account
        receiver.amount += float(transaction.amount)

        # check transfer from savings account
        '''if sending_account.type == 0:
            possible_accounts = Account.objects.filter(owner=sending_account.owner, type=1)
            if receiver not in possible_accounts:
                commit = False
                return 0'''

        if commit:
            transaction.save()
            sending_account.save()
            receiver.save()
            return transaction


class KuendigungForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ModelForm, self).__init__(*args, **kwargs)

    # amount of money to transfer

    zielkonto = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Zielkonto eingeben',
                                    }))

    class Meta:
        model = Transaction
        fields = ()

    def save(self, request, commit=True):
        sending_account = request.POST.dict().get("senderkonto")
        sending_account = Account.objects.get(pk=sending_account)

        transaction = super(KuendigungForm, self).save(commit=False)
        transaction.amount = sending_account.amount
        transaction.usage = f"Auflösung von Konto {sending_account.iban}"
        transaction.sending_account = sending_account
        transaction.receiving_account = self.cleaned_data["zielkonto"]
        transaction.receiving_name = ""
        transaction.standing_order = 0
        transaction.time_of_transaction = timezone.now()

        sending_account.amount -= float(transaction.amount)
        sending_account.status = 0

        # Wenn das Zielkonto auf unserer Datenbank existiert, bekommt der Empfänger das Geld
        # Ansonsten wird das Geld nicht überwiesen, aber die Transaktion wird erstellt
        try:
            receiver = Account.objects.get(iban=transaction.receiving_account)
        except Account.DoesNotExist:
            receiver = sending_account
        receiver.amount += float(transaction.amount)

        # check if cancelation of cd_account
        if sending_account.type == 2:

            # cancelation only possible if transaction account exists to send money to
            possible_accounts = Account.objects.filter(owner=sending_account.owner, type=1)
            if receiver not in possible_accounts:
                commit = False
        else:
            commit = False

        if commit:
            transaction.save()
            sending_account.save()
            receiver.save()
