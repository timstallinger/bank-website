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
from .forms import SignUpForm, KontoForm, UberweisungForm

from datetime import date


def signup(request):
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
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def konto_create(request):
    if request.method == 'POST':
        form = KontoForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            form = KontoForm(request.user)
    else:
        form = KontoForm(request.user)
    return render(request, 'konto_create.html', {'form': form})

def profile_data(request):
    u = request.user
    p = u

    if Person.objects.filter(id=u.id).exists():
        p = Person.objects.get(id=u.id)
        if not p.birthday:
            p = u

    a = Account.objects.filter(owner=u.id)

    return render(request, 'profile.html', {'user': u, 'person': p, 'accounts': a})

def konto_uberweisen(request):
    if request.method == 'POST':
        form = UberweisungForm(request.user, request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('user_profile')
        else:
            form = UberweisungForm(request.user)
    else:
        form = UberweisungForm(request.user)
    # get all accounts of the user
    accounts = Account.objects.filter(owner=request.user)

    return render(request, 'konto_uberweisen.html', {'form': form, 'accounts': accounts, 'checked': False})


def transactions(request):
    trans = []
    # get all of users accounts
    accounts = Account.objects.filter(owner=request.user)
    # get all transactions of user
    for account in accounts:
        for t in Transaction.objects.filter(sending_account=account):
            t.amount = -t.amount
            trans.append(t)
        for t in Transaction.objects.filter(receiving_account=account.iban):
            trans.append(t)
    trans.sort(key=lambda x: x.time_of_transaction, reverse=True)

    return render(request, 'standing_transactions.html', {'gesendet': trans})


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
        transactions.sort(key=lambda x: x.time_of_transaction, reverse=True)
        for t in transactions:
            t.time_of_transaction = t.time_of_transaction.strftime("%Y.%m.%d %H:%M")

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
        return Response({'trans': transactions, 'startDate': startDate, 'endDate': endDate,'argstr':argstr, 'startBalance':start_balance, 'endBalance':end_balance})
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self, request, startDate=None, endDate=None):
        transactions = []
        accounts = Account.objects.filter(owner=request.user)
        for account in accounts:
            if startDate and endDate:
                sending = Transaction.objects.filter(sending_account=account, time_of_transaction__range=[startDate, endDate])
                receiving = Transaction.objects.filter(receiving_account=account.iban, time_of_transaction__range=[startDate, endDate])
            else:
                sending = Transaction.objects.filter(sending_account=account)
                receiving = Transaction.objects.filter(receiving_account=account.iban)
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
        sender_account = Account.objects.get(iban=transaction.sending_account.iban).owner
        try:
            receiver_account = Account.objects.get(iban=transaction.receiving_account).owner
        except Account.DoesNotExist:
            receiver_account = None
        time = transaction.time_of_transaction.strftime("%Y.%m.%d, %H:%M")
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
        print(snippet.sending_account)
        if snippet.sending_account.owner == request.user and (not snippet.approved or snippet.standing_order):
            snippet.delete()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return redirect('/accounts/transactions/')
