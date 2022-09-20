from pyexpat import model
from django.db import models
from django.utils import timezone

# Create your models here.


class Bank(models.Model):
    balance = models.FloatField()
    profit = models.FloatField()
    bic = models.CharField(max_length=11, primary_key=1)
    name = models.CharField(max_length=30)


class Account(models.Model):
    name = models.CharField(max_length=30)
    amount = models.FloatField(default=0)
    interestrate = models.FloatField(default=0)

    class Meta:
        abstract = True


class TransactionAccount(Account):
    iban = models.CharField(max_length=22, primary_key=True)
    overdraft = models.CharField(max_length=30, default=0)


class SavingsAccount(Account):
    iban = models.CharField(max_length=22, primary_key=True)


class CreditCardAccount(Account):
    cardnumber = models.CharField(max_length=16, primary_key=True)


class Card(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    cvv = models.IntegerField()
    pin = models.IntegerField()
    expiration_date = models.DateField()


class Tan(models.Model):
    tan = models.IntegerField(primary_key=True)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    time_of_transaction = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    source_account = models.CharField(max_length=22)
    destination_account = models.CharField(max_length=22)


#class Transaction(models.Model):
#    id = models.IntegerField(primary_key=True)
#    time_of_transaction = models.DateTimeField(default=timezone.now)
#    amount = models.FloatField()
#    account = models.CharField(max_length=22)


class BankStatement(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)


class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)





#class BankStatementTransaction(models.Model):
#    bank_statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)
#    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


#class AccountBankStatement(models.Model):
#    account = models.ForeignKey(Account, on_delete=models.CASCADE)
#    bank_statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)


#class AccountTransaction(models.Model):
#    account = models.ForeignKey(Account, on_delete=models.CASCADE)
#    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


#class AccountCard(models.Model):
#    account = models.ForeignKey(Account, on_delete=models.CASCADE)
#    card = models.ForeignKey(Card, on_delete=models.CASCADE)


#class AccountTan(models.Model):
#    account = models.ForeignKey(Account, on_delete=models.CASCADE)
#    tan = models.ForeignKey(Tan, on_delete=models.CASCADE)


#class UserAccount(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    Account = models.ForeignKey(Account, on_delete=models.CASCADE)


#class BankUser(models.Model):
#    Bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
#    User = models.ForeignKey(User, on_delete=models.CASCADE)

