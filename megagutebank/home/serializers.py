from rest_framework import serializers
from .models import Account, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "standing_order", "standing_order_days", "time_of_transaction", "amount", "sending_account", "receiving_account", "receiving_name", "usage", "approved"]
        