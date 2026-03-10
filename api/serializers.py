"""Serializers for the API endpoints"""

from rest_framework import serializers
from .models import Account, Category, Transaction, Budget

class AccountSerializer(serializers.ModelSerializer):
  """Serializer for Account model"""

  class Meta:
    model = Account

    fields = [
      "id", 
      "name", 
      "type", 
      "balance", 
      "currency", 
      "created_at"
    ]

    read_only_fields = ["id", "created_at"]


class CategorySerializer(serializers.ModelSerializer):
  """Serializer for Category model"""

  class Meta:
    model = Category

    fields = [
      "id",
      "name", 
      "type", 
      "colour", 
      "is_default"
    ]

    read_only_fields = ["id"]


class TransactionSerializer(serializers.ModelSerializer):
  """Serializer for Transaction model"""

  class Meta:
    model = Transaction

    fields = [
      "id", 
      "account", 
      "category", 
      "amount", 
      "type", 
      "description",
      "date",
      "created_at"
    ]

    read_only_fields = ["id", "created_at"]


class BudgetSerializer(serializers.ModelSerializer):
  """Serializer for Budget model"""

  class Meta:
    model = Budget

    fields = ["id", "category", "amount_limit", "period", "start_date"]

    read_only_fields = ["id"]