from pyexpat import model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import CheckConstraint, Q, F


class Bank(models.Model):
    balance = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    blz = models.IntegerField(default=100100500000000000, primary_key=1)
    name = models.CharField(default="MGB", max_length=30)

class Person(User):
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    address_plz = models.IntegerField(default=0)
    address_city = models.CharField(max_length=100)
    address_street = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True)
    birthday = models.DateField()
    contacts = models.ManyToManyField('self', blank=True)
    confirmed = models.IntegerField(default=0)

class Employee(models.Model):
    eid = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Account(models.Model):
    # aid = models.IntegerField(primary_key=True, auto_created=True)
    iban = models.CharField(primary_key=True, max_length=34)
    type = models.IntegerField()
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    amount = models.FloatField(default=0)
    interest = models.FloatField(default=0)
    negative_interest = models.FloatField(default=0.073)
    status = models.IntegerField(default=0)
    employee = models.ForeignKey(Employee, default=None, on_delete=models.DO_NOTHING, blank=True, null=True)
    overdraft = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        over = float(self.overdraft) + float(self.amount)
        if over < 0:
            # Rollback
            raise ValueError("Overdraft limit exceeded")
    class Meta:
        # check that amount + overdraft >= 0
        constraints = [
            CheckConstraint(check=Q(overdraft__gte=0), name='overdraft_positive'),
        ]

class TagesgeldAccount(Account):
    time_period = models.IntegerField(default=0)
    interest_amount = models.FloatField
    time_of_creation = models.DateTimeField(default=timezone.now)


class DebitCard(models.Model):
    pin = models.IntegerField()
    state = models.BooleanField(default=1)
    expiration_date = models.DateField(default=timezone.now)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Card(models.Model):
    cvv = models.IntegerField()
    pin = models.IntegerField()
    state = models.BooleanField(default=1)
    expiration_date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Tan(models.Model):
    tan = models.IntegerField(primary_key=True)
    state = models.BooleanField(default=1)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Transaction(models.Model):
    standing_order = models.BooleanField(default=0)
    standing_order_days = models.IntegerField(null=True, default=None,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    iban_sender = models.ForeignKey(Account, on_delete=models.RESTRICT, related_name='iban_sender')
    iban_receiver = models.CharField(max_length=34)
    name_receiver = models.CharField(max_length=30,null=True, default=None,blank=True)
    reference = models.CharField(max_length=140, null=True, default=None,blank=True)
    approved = models.BooleanField(default=0)
    approved_by = models.ForeignKey(Employee, on_delete=models.RESTRICT, null=True, blank=True, default=None)
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(amount__gt=0),
                name = 'check_amount',
            ),
        ]

class BankStatement(models.Model):
    time = models.DateTimeField(default=timezone.now)


class ExternalTransaction(Transaction):
    sending_bank = models.ForeignKey(Bank, on_delete=models.RESTRICT)