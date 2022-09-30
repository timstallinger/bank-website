import datetime
import random

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from rest_framework import status
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import TransactionSerializer
from .forms import SignUpForm, KontoForm, UberweisungForm, TagesgeldForm, KuendigungForm

from datetime import date

#TODO: Zinsen falsch

#TODO: Profil bearbeiten


def manage(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        if request.POST.get("button_declined"):
            D = request.POST.get("button_declined")
            a = Account.objects.get(iban=D)
            a.status = -1
            a.employee = Employee.objects.get(eid=request.user.id)
            a.save()
        elif request.POST.get("button_approved"):
            D = request.POST.get("button_approved")
            a = Account.objects.get(iban=D)
            a.status = 1
            a.employee = Employee.objects.get(eid=request.user.id)
            a.save()
        if request.POST.get("button_active"):
            cid = request.POST.get("button_active")
            c = Card.objects.get(id=cid)
            c.state = 1
            c.save()
        if request.POST.get("button_inactive"):
            cid = request.POST.get("button_inactive")
            c = Card.objects.get(id=cid)
            c.state = 0
            c.save()
        if request.POST.get("ov_iban"):
            iban = request.POST.get("ov_iban")
            ov = request.POST.get("ov_field")
            a = Account.objects.get(iban=iban)
            a.overdraft = ov
            a.save()
        if request.POST.get("button_confirmed"):
            id = request.POST.get("button_confirmed")
            p = Person.objects.get(id=id)
            p.confirmed = 1
            p.save()

        if request.POST.get("button_decline"):
            id = request.POST.get("button_decline")
            p = Person.objects.get(id=id)
            p.confirmed = -1
            p.save()
        if request.POST.get("amount_iban"):
            iban = request.POST.get("amount_iban")
            amount = request.POST.get("amount_field")
            a = Account.objects.get(iban=iban)
            a.amount = amount
            a.save()

        Accounts = Account.objects.all()
        Cards = Card.objects.all()
        P = Person.objects.all()

        return render(request, 'manage_accounts.html', {'user': request.user, 'accounts': Accounts, 'cards': Cards, 'P': P})

def signup(request):
    if request.user.is_authenticated:
        return redirect('/accounts/profile/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def konto_create(request):
    if request.user.is_staff:
        return redirect('/accounts/profile/')
    if not (request.user.is_authenticated and request.user.person.confirmed):
        return render(request, 'error.html', {'error': 'Sie sind nicht angemeldet oder Ihre Konto wurde noch nicht bestätigt.'})
    if request.method == 'POST':
        tagesgeld = request.POST.get("tagesgeld")
        if tagesgeld == 0 or tagesgeld == 1:
            form = KontoForm(request.user, request.POST)
        else:
            form = TagesgeldForm(request.user, request.POST)
        if form.is_valid():
            res = form.save(request)
            if res == 0:
                return render(request, 'konto_create.html', {'form': form, 'error': "Ihr Girokonto ist nicht ausreichend gedeckt!"})
            return redirect('/accounts/profile/')
    else:
        form = KontoForm(request.user)
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'konto_create.html', {'form': form, 'accounts':accounts})

def profile_data(request):
    if not (request.user.is_authenticated):
        return render(request, 'error.html', {'error': 'Sie sind nicht angemeldet.'})
    if request.GET.get('create_card'):
        i = request.GET.get('create_card')
        Acc = Account.objects.get(iban=i)
        if not Card.objects.filter(account=Acc).exists():
            Card.objects.create(
                cvv = random.randint(100, 999),
                pin=random.randint(1000, 9999),
                state=0,
                expiration_date=date.today() + datetime.timedelta(days=1826.2125), # 5 years
                account=Acc
            )


    c = Card.objects.all()
    u = request.user
    p = u

    if Person.objects.filter(id=u.id).exists():
        p = Person.objects.get(id=u.id)
        if not p.birthday:
            p = u

    L = []
    for card in c:
        L.append(card.account_id)

    a = Account.objects.filter(owner=u.id)

    for acc in a:
        acc.interest *= 100
        acc.negative_interest *= 100
        acc.amount = round(acc.amount, 2)

    T = TagesgeldAccount.objects.filter(type=2)

    return render(request, 'profile.html', {'user': u, 'person': p, 'accounts': a, 'cards': c, 'list': L, 'tagesgeld': T})

def konto_uberweisen(request):
    if request.user.is_staff:
        return redirect('/accounts/verwalten/')
    if not (request.user.is_authenticated and request.user.person.confirmed):
        return render(request, 'error.html', {'error': 'Sie sind nicht angemeldet oder Ihre Konto wurde noch nicht bestätigt.'})
    if request.method == 'POST':
        form = UberweisungForm(request.user, request.POST)
        if form.is_valid():
            suc = form.save(request)
            if type(suc) == str:
                return render(request, 'konto_uberweisen.html', {'form': form, 'error': suc})
            elif suc == 0:
                accounts = Account.objects.filter(owner=request.user)
                return render(request, 'konto_uberweisen.html', {'form': form, 'accounts': accounts, 'checked': False, 'error': "Ihr Konto ist nicht ausreichend gedeckt!"})

            else:
                return redirect('/accounts/transactions/detail/' + str(suc.id))
        else:
            form = UberweisungForm(request.user)
    else:
        form = UberweisungForm(request.user)
    # get all accounts of the user
    accounts = Account.objects.filter(owner=request.user)
    if len(accounts) == 0:
        return redirect('/accounts/konto/erstellen')
    return render(request, 'konto_uberweisen.html', {'form': form, 'accounts': accounts, 'checked': False})

def konto_kuendigen(request):
    if not (request.user.is_authenticated and request.user.person.confirmed):
        return render(request, 'error.html', {'error': 'Sie sind nicht angemeldet oder Ihre Konto wurde noch nicht bestätigt.'})
    if request.method == 'POST':
        form = KuendigungForm(request.user, request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('user_profile')
        else:
            form = KuendigungForm(request.user)
    else:
        form = KuendigungForm(request.user)
    # get all accounts of the user
    accounts = Account.objects.filter(owner=request.user)

    return render(request, 'konto_kuendigen.html', {'form': form, 'accounts': accounts, 'checked': False})


class TransactionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'transactions.html'
    page_size = 10
    def get_object(self, tid):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Transaction.objects.get(id=tid)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # TODO: What if only one of the dates is given?
        # TODO: filter by account
        
        # get time range from request
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        page = request.GET.get('page',1)
        transactions = self.get_queryset(request, startDate, endDate)

        # sort transactions by time
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        for t in transactions:
            t.timestamp = t.timestamp.strftime("%Y.%m.%d %H:%M")

        serializer = TransactionSerializer(transactions, many=True)
        
        argstr=""
        if startDate:
            argstr+="&startDate="+startDate
        if endDate:
            argstr+="&endDate="+endDate

        # calculate bank start balance and endbalance
        (start_balance, end_balance)=self.get_balance(request, startDate,endDate, transactions)

        paginator = Paginator(transactions, 10)
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)
        # round startbilance and endbalance to 2 decimal places
        start_balance = round(start_balance, 2)
        end_balance = round(end_balance, 2)
        return Response({'trans': transactions, 'startDate': startDate, 'endDate': endDate,'argstr':argstr, 'startBalance':start_balance, 'endBalance':end_balance})
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self, request, startDate=None, endDate=None):
        transactions = []
        accounts = Account.objects.filter(owner=request.user)
        for account in accounts:
            if startDate and endDate:
                sending = Transaction.objects.filter(iban_sender=account, timestamp__range=[startDate, endDate])
                receiving = Transaction.objects.filter(iban_receiver=account.iban, timestamp__range=[startDate, endDate])
            else:
                sending = Transaction.objects.filter(iban_sender=account)
                receiving = Transaction.objects.filter(iban_receiver=account.iban)
            # set sending amount negative
            for t in sending:
                t.amount = int(-t.amount)
            
            transactions += sending
            transactions += receiving
        return transactions

    def get_balance(self,request, startDate,endDate, trans_in_range):
        '''
        Calculate the start and end balance of the bank account in given time range
        '''
        if endDate == None:
            endDate = date.today()
        accountbalance = 0
        for account in Account.objects.filter(owner=request.user):
            accountbalance += account.amount
        # get all transactions since endDate
        transactions = self.get_queryset(request, endDate, date.today())
        end_balance = accountbalance
        for t in transactions:
            end_balance += t.amount
        # get all transactions since startDate
        transactions = trans_in_range
        start_balance = end_balance
        for t in transactions:
            start_balance -= t.amount
        print(start_balance, "E:",end_balance)
        return (start_balance,end_balance)


class TransactionDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'single_transaction.html'
    def get(self, request, tid, *args, **kwargs):
        '''
        Get the details of the todo item with given id
        '''
        transaction = self.get_object(tid)
        if transaction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionSerializer(transaction)
        # get sender from transaction
        sender_account = Account.objects.get(iban=transaction.iban_sender.iban).owner
        try:
            receiver_account = Account.objects.get(iban=transaction.iban_receiver).owner
        except Account.DoesNotExist:
            receiver_account = None
        time = transaction.timestamp.strftime("%Y.%m.%d, %H:%M")
        return Response({'trans': serializer.data, 'sender': sender_account, 'receiver': receiver_account, 'time':time})
    def get_object(self, tid):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Transaction.objects.get(id=tid)
        except Transaction.DoesNotExist:
            return None

    def post(self, request,tid):
        snippet = self.get_object(tid)
        print(snippet.iban_sender)
        if snippet.iban_sender.owner == request.user and (not snippet.approved or snippet.standing_order):
            snippet.delete()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return redirect('/accounts/transactions/')
