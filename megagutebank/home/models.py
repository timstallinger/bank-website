from pyexpat import model
from django.db import models
from django.utils import timezone

# Create your models here.


class Bank(models.Model):
    balance = models.FloatField()
    profit = models.FloatField()
    bic = models.CharField(max_length=11, primary_key=1)
    name = models.CharField(max_length=50)


class Account(models.Model):
    name = models.CharField(max_length=30)
    amount = models.FloatField(default=0)
    interestrate = models.FloatField(default=1)

    class Meta:
        abstract = True


class SavingsAccount(Account):
    iban = models.CharField(max_length=22, primary_key=True)


class CheckingAccount(Account):
    iban = models.CharField(max_length=22, primary_key=True)


class Kreditkartenkonto(Account):
    cardnumber = models.CharField(max_length=16, primary_key=True)


class Card(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    cvv = models.IntegerField(max_length=3)
    pin = models.IntegerField(max_length=8)
    expiration_date = models.DateField()


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    time_of_transaction = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    source_account = models.CharField(max_length=22)
    destination_account = models.CharField(max_length=22)


class BankStatement(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)


class BankStatementConsistsOf(models.Model):
    bank_statement = models.ForeignKey(BankStatement)
    transaction = models.ForeignKey(Transaction)

