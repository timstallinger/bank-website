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
    phone.label = "Telefonnummer"
    address_plz = forms.IntegerField(required=True,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Postleitzahl eingeben',
                                            }))
    address_plz.label = "Postleitzahl"
    address_city = forms.CharField(max_length=30, required=True,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Stadt eingeben',
                                  }))
    address_city.label = "Stadt"
    address_street = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Straße eingeben',
                                    }))
    address_street.label = "Straße"
    birthday = forms.DateField(initial=datetime.date.today,
                               widget=forms.widgets.DateInput(
                                   attrs={
                                       'type': 'date', 'class': 'form-control', 'min': '1900-01-01',
                                       'max': datetime.date.today() - datetime.timedelta(days=18 * 365)
                                   }))
    birthday.label = "Geburtsdatum"
    password1 = forms.CharField(max_length=30, required=True,
                                help_text='Mindestens 8 Zeichen lang und darf nicht zu einfach sein.',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Passwort eingeben',
                                    }))
    password1.label = "Passwort"
    password2 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Passwort bestätigen',
                                    }))
    password2.label = "Passwort bestätigen"

    class Meta:
        model = Person
        fields = ('vorname', 'nachname', 'email', 'phone', 'username', 'birthday', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data["vorname"]
        user.last_name = self.cleaned_data["nachname"]
        user.email = self.cleaned_data["email"]
        user.address_plz = self.cleaned_data["address_plz"]
        user.address_city = self.cleaned_data["address_city"]
        user.address_street = self.cleaned_data["address_street"]
        user.phone_number = self.cleaned_data["phone"]
        check_user = self.cleaned_data["username"]
        check_user = Person.objects.filter(username=check_user)
        if check_user.exists():
            raise forms.ValidationError("Dieser Username ist bereits vergeben.")
        user.confirmed = 0

        # Generate iBan for Girokonto
        blz_fill = 100100500000000000
        account_nr = random.randint(1, 9999999999)
        temp_iban = blz_fill + account_nr
        checksum = 98 - (int(str(temp_iban) + str(131400)) % 97)

        if checksum < 10:
            iban = f"DE{checksum}{temp_iban}"
        else:
            iban = f"DE{checksum}{temp_iban}"

        # Create Giro Account for user
        giro_account = Account()
        giro_account.name = "Girokonto für " + user.first_name + " " + user.last_name
        giro_account.iban = iban
        giro_account.owner = user
        giro_account.type = 1
        giro_account.amount = 50
        giro_account.status = 1
        giro_account.overdraft = 0
        giro_account.interest = 0
        giro_account.negative_interest = 0.073

        if commit:
            user.save()
            giro_account.save()
        return user


#region dicts
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
#endregion


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
    tagesgeld_dauer = forms.CharField(max_length=30, required=False,
                                      widget=forms.Select(choices=tagesgeld_options, attrs={
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
        konto.iban = self.gen_iban(self.cleaned_data["konto_standort"])
        konto.status = 1

        konto.type = typ_to_int[self.cleaned_data["konto_typ"]]
        konto.owner = self.user

        if konto.type == 0:
            konto.interest = 0.0365
            konto.negative_interest = 0
        if konto.type == 1:
            konto.interest = 0
            konto.negative_interest = 0.073
        elif konto.type == 2:
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
        konto.iban = self.gen_iban(self.cleaned_data["konto_standort"])

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
    empfangername.label = "Empfängername"
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
        'class': "form-control",
    }))
    zeit_input.label = "Dauerauftrag Zeitabstand in Tagen"

    class Meta:
        model = Transaction
        fields = ('betrag', 'zielkonto', 'verwendungszweck',)

    def save(self, request, commit=True):
        iban_sender = request.POST.dict().get("senderkonto")
        iban_sender = Account.objects.get(pk=iban_sender)

        if iban_sender.status == -1:
            return "Ihr Konto wurde blockiert."

        transaction = super(UberweisungForm, self).save(commit=False)
        transaction.amount = self.cleaned_data["betrag"]
        if transaction.amount <= 0:
            return "Sie können keinen negativen Betrag überweisen."
        transaction.reference = request.POST.dict().get("verwendungszweck")
        transaction.iban_sender = iban_sender
        transaction.iban_receiver = self.cleaned_data["zielkonto"]
        transaction.name_receiver = self.cleaned_data["empfangername"]
        transaction.standing_order = self.cleaned_data["dauerauftrag"]
        transaction.timestamp = timezone.now()
        if transaction.standing_order:
            transaction.standing_order_days = self.cleaned_data["zeit_input"]
        transaction.approved = True
        if iban_sender.amount + iban_sender.overdraft < transaction.amount:
            # Falls Konto nicht ausreichend gedeckt ist, abbrechen
            return "Ihr Konto ist nicht ausreichend gedeckt."
        iban_sender.amount -= float(transaction.amount)

        # Wenn das Zielkonto auf unserer Datenbank existiert, bekommt der Empfänger das Geld
        # Ansonsten wird das Geld nicht überwiesen, aber die Transaktion wird erstellt
        try:
            receiver = Account.objects.get(iban=transaction.iban_receiver)
        except Account.DoesNotExist:
            receiver = iban_sender
        receiver.amount += float(transaction.amount)

        # check transfer from savings account
        if iban_sender.type == 0:
            possible_accounts = Account.objects.filter(owner=iban_sender.owner)
            if receiver not in possible_accounts:
                commit = False
                return "Sie können von einem Sparkonto nur auf eigene Konten überweisen."

        if commit:
            transaction.save()
            iban_sender.save()
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
        iban_sender = request.POST.dict().get("senderkonto")
        iban_sender = Account.objects.get(pk=iban_sender)

        transaction = super(KuendigungForm, self).save(commit=False)
        transaction.amount = iban_sender.amount
        transaction.reference = f"Auflösung von Konto {iban_sender.iban}"
        transaction.iban_sender = iban_sender
        transaction.iban_receiver = self.cleaned_data["zielkonto"]
        transaction.name_receiver = ""
        transaction.standing_order = 0
        transaction.timestamp = timezone.now()

        iban_sender.status = 0

        # Wenn das Zielkonto auf unserer Datenbank existiert, bekommt der Empfänger das Geld
        # Ansonsten wird das Geld nicht überwiesen, aber die Transaktion wird erstellt
        try:
            receiver = Account.objects.get(iban=transaction.iban_receiver)
        except Account.DoesNotExist:
            receiver = iban_sender

        iban_sender.amount -= float(transaction.amount)
        receiver.amount += float(transaction.amount)
        # wenn dauer des cd_accounts erfuellt wurde -> interest mit ausschütten
        if iban_sender.time_period <= 0:
            transaction.amount += iban_sender.interest_amount
            receiver.amount += iban_sender.interest_amount
            iban_sender.interest_amount = 0



        # check if cancelation of cd_account
        if iban_sender.type == 2:

            # cancelation only possible if transaction account exists to send money to
            possible_accounts = Account.objects.filter(owner=iban_sender.owner, type=1)
            if receiver not in possible_accounts:
                commit = False
        else:
            commit = False

        if commit:
            transaction.save()
            iban_sender.save()
            receiver.save()
