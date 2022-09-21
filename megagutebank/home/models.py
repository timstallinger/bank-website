from pyexpat import model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Bank(models.Model):
    balance = models.FloatField()
    profit = models.FloatField()
    bic = models.CharField(max_length=11, primary_key=1)
    name = models.CharField(max_length=30)


class Employee(models.Model):
    eid = models.IntegerField(primary_key=True)


class Person(User):
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True)
    birthday = models.DateField()
    contacts = models.ManyToManyField('self', blank=True)


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
    employee = models.ForeignKey(Employee, default=None, on_delete=models.RESTRICT, null=True)


class DebitCard(models.Model):
    pin = models.IntegerField()
    state = models.BooleanField(default=1)
    expiration_date = models.DateField(default=timezone.now)


class Card(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    cvv = models.IntegerField()
    pin = models.IntegerField()
    state = models.BooleanField(default=1)
    expiration_date = models.DateField()


class Tan(models.Model):
    tan = models.IntegerField(primary_key=True)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    standing_order = models.BooleanField(default=0)
    period_of_time = models.TimeField
    time_of_transaction = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    sending_account = models.CharField(max_length=34)
    sender = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    receiving_account = models.CharField(max_length=34)
    usage = models.CharField(max_length=140, null=True)


class BankStatement(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)


