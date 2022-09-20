from pyexpat import model
from django.db import models
from django.utils import timezone

# Create your models here.


class Bank(models.Model):
    balance = models.FloatField()
    profit = models.FloatField()
    bic = models.CharField(max_length=11, primary_key=1)
    name = models.CharField(max_length=30)


class Employee(models.Model):
    eid = models.IntegerField(primary_key=True)




class Account(models.Model):
    name = models.CharField(max_length=30)
    amount = models.FloatField(default=0)
    interestrate = models.FloatField(default=0)
    status = models.IntegerField(default=0)
    employee = models.ForeignKey(Employee, default=None, on_delete=models.RESTRICT)

    class Meta:
        abstract = True


class TransactionAccount(Account):
    iban = models.CharField(max_length=22, primary_key=True)
    overdraft = models.CharField(max_length=30, default=0)


class SavingsAccount(Account):
    iban = models.CharField(max_length=22, primary_key=True)


class CreditCardAccount(Account):
    cardnumber = models.CharField(max_length=16, primary_key=True)


class DebitCard(models.Model):
    id = models.IntegerField(primary_key=True)
    pin = models.IntegerField()
    state = models.IntegerField()
    expiration_date = models.DateField(default=timezone.now)


class CertificateOfDepositsAccount(Account):
    duration = models.IntegerField()


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
    account = models.CharField(max_length=22)


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
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=30)





class BankStatementTransaction(models.Model):
    bank_statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


class SavingsAccountBankStatement(models.Model):
    account = models.ForeignKey("SavingsAccount", on_delete=models.CASCADE)
    bank_statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)


class TransactionAccountBankStatement(models.Model):
    account = models.ForeignKey("TransactionAccount", on_delete=models.CASCADE)
    bank_statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)


class AccountBankStatement(models.Model):
    account = models.ForeignKey("SavingsAccount", on_delete=models.CASCADE)
    bank_statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)


#class StandingOrders(models.Model):



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





#class Contact(models.Model):
#    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
#    user2 = models.ForeignKey(User, on_delete=models.CASCADE)

