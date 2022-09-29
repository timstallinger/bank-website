from rest_framework import serializers
from .models import Account, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "standing_order", "standing_order_days", "timestamp", "amount", "iban_sender", "iban_receiver", "name_receiver", "reference", "approved"]
        