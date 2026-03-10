from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Account, Category, Transaction, Budget
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer, BudgetSerializer


class AccountViewSet(viewsets.ModelViewSet):
  """Handle account crud operations"""

  serializer_class = AccountSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Account.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
  """Handle category crud operations"""

  serializer_class = CategorySerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Category.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
  """Handle transaction crud operations"""

  serializer_class = TransactionSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Transaction.objects.filter(account__user=self.request.user)

  def perform_create(self, serializer):
    serializer.save()


class BudgetViewSet(viewsets.ModelViewSet):
  """Handle budget crud operations"""

  serializer_class = BudgetSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Budget.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
