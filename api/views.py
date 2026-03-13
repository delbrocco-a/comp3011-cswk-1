from rest_framework import viewsets, permissions
from .models import Account, Category, Transaction, Budget
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer, BudgetSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime
import calendar
import requests


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request) -> Response:
  """
  User registration:
    Input:
      - username
      - password
      - email address
    Output:
      - Response: BAD | CREATED
  """

  ### allow any to register
  ### get required sign-up details
  username = request.data.get("username")
  password = request.data.get("password")
  email    = request.data.get("email", "")

  ## validate get data

  ## check ¬null for username & password
  if not username or not password:
    return Response(
      {"error": "Username and password required"},
        status=status.HTTP_400_BAD_REQUEST
    )

  ### check username doesn't already exist
  if User.objects.filter(username=username).exists():
      return Response(
        {"error": "Username already taken"},
        status=status.HTTP_400_BAD_REQUEST
      )

  ## success - create user

  user = User.objects.create_user(
    username=username, password=password, email=email)
  token, _ = Token.objects.get_or_create(user=user)

  return Response({"token": token.key}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request) -> Response:
  """
  User Login:
    Input:
      - username
      - password
    Output:
      - response (auth)
  """

  ### allow any to login
  ### get username & password
  username = request.data.get("username")
  password = request.data.get("password")

  ## authenticate details
  user = authenticate(username=username, password=password)
  if not user:
    return Response(
      {"error": "Invalid credentials"},
      status=status.HTTP_401_UNAUTHORIZED
    )

  ## success - authenticate session

  token, _ = Token.objects.get_or_create(user=user)

  return Response({"token": token.key}, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout(request) -> Response:
  """Logout: remove authentic session"""
  ### only authorised sessions can logout
  request.user.auth_token.delete()
  return Response({"message": "Logged out"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def summary(request) -> Response:
  """GET /api/analytics/summary/?month=2026-03"""

  ### retrieve month in user request
  month_str = request.query_params.get("month")
  
  try: ### get month, if none: 400 bad req
    year, month = map(int, month_str.split("-"))
  except (ValueError, AttributeError):
    return Response(
      {"error": "Invalid month format. Use YYYY-MM"}, 
      status=status.HTTP_400_BAD_REQUEST
    )

  ### retrieve all transactions in given month
  transactions = Transaction.objects.filter(
    account__user=request.user,
    date__year=year,
    date__month=month
  )

  ### perform totals and difference of totals
  total_income   = transactions.filter(type="income").aggregate(
    Sum("amount"))["amount__sum"] or 0
  total_expenses = transactions.filter(type="expense").aggregate(
    Sum("amount"))["amount__sum"] or 0
  net_savings    = total_income - total_expenses

  return Response({
    "month"         : month_str,
    "total_income"  : total_income,
    "total_expenses": total_expenses,
    "net_savings"   : net_savings
  }, status=status.HTTP_200_OK)


@api_view(["GET"])
def spending_by_category(request) -> Response:
  """GET /api/analytics/spending-by-category/?month=2026-03"""

  ### prepare all expenditure transactions for listing
  transactions = Transaction.objects.filter(
    account__user=request.user,
    type="expense"
  )

  ### check month field for refinement of breakdown
  month_str = request.query_params.get("month")

  if month_str:
    try: ### optional month label
      year, month = map(int, month_str.split("-"))
    except (ValueError, AttributeError):
      return Response(
        {"error": "Invalid month format. Use YYYY-MM"},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    ### limit scope to month
    transactions = transactions.filter(date__year=year, date__month=month)

  ### list spending by category
  breakdown = transactions.values(
    "category__name").annotate(total=Sum("amount")).order_by("-total")

  return Response({
    "month"    : month_str,
    "breakdown": list(breakdown)
  }, status=status.HTTP_200_OK)


@api_view(["GET"])
def trends(request) -> Response:
  """GET /api/analytics/trends/?months=6"""

  try: ### iterate over the number of months requested
    num_months = int(request.query_params.get("months", 6))
  except ValueError:
    return Response(
      {"error": "months must be an integer"},
      status=status.HTTP_400_BAD_REQUEST
    )

  result = []
  now = timezone.now()

  for i in range(num_months - 1, -1, -1):
    ### from current month (and year), go back through each month
    month = (now.month - i - 1) % 12 + 1
    year  = now.year - (
      (i - now.month + 1) // 12 + (1 if i >= now.month else 0))

    ### append all transactions in given month
    transactions = Transaction.objects.filter(
      account__user=request.user,
      date__year=year,
      date__month=month
    )

    ### collect all income & expense for each month
    income   = transactions.filter(
      type="income").aggregate(Sum("amount"))["amount__sum"] or 0
    expenses = transactions.filter(
      type="expense").aggregate(Sum("amount"))["amount__sum"] or 0

    result.append({
      "month"   : f"{year}-{month:02d}",
      "income"  : income,
      "expenses": expenses,
      "net"     : income - expenses
    })

  return Response({"trends": result}, status=status.HTTP_200_OK)


@api_view(["GET"])
def budget_status(request) -> Response:
  """GET /api/analytics/budget-status/"""

  ### acquire budget user requested
  budgets = Budget.objects.filter(user=request.user)
  result  = []

  ## loop through and get all budget details
  for budget in budgets:
    now   = timezone.now()

    spent = Transaction.objects.filter(
      account__user=request.user,
      category=budget.category,
      type="expense",
      date__year=now.year,
      date__month=now.month
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    percent_used = (
      spent / budget.amount_limit * 100) if budget.amount_limit > 0 else 0

    result.append({
      "category"    : budget.category.name,
      "limit"       : budget.amount_limit,
      "spent"       : spent,
      "remaining"   : budget.amount_limit - spent,
      "percent_used": round(percent_used, 1),
      "status"      : "over" if spent > budget.amount_limit else "under"
    })

  return Response({"budgets": result}, status=status.HTTP_200_OK)


@api_view(["GET"])
def currency_summary(request) -> Response:
  """GET /api/analytics/currency-summary/?base=GBP"""

  ### api is uk based
  base = request.query_params.get("base", "GBP")
  
  ### open API required no key for use
  rates = requests.get(f"https://open.er-api.com/v6/latest/{base}").json()
  
  accounts = Account.objects.filter(user=request.user)
  result = []

  ### grab all accounts, and summarise with gbp as base currency
  for account in accounts:
    rate = rates["rates"].get(account.currency, 1)
    result.append({
      "account"          : account.name,
      "original_balance" : account.balance,
      "original_currency": account.currency,
      "converted_balance": round(account.balance / rate, 2),
      "base_currency"    : base
    })
  
  return Response({'summary': result, 'base': base})


class AccountViewSet(viewsets.ModelViewSet):
  """Handle account crud operations"""

  serializer_class = AccountSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self) -> Account:
    return Account.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
  """Handle category crud operations"""

  serializer_class = CategorySerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self) -> Category:
    return Category.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
  """Handle transaction crud operations"""

  serializer_class = TransactionSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self) -> Transaction:
    return Transaction.objects.filter(account__user=self.request.user)

  def perform_create(self, serializer):
    serializer.save()


class BudgetViewSet(viewsets.ModelViewSet):
  """Handle budget crud operations"""

  serializer_class = BudgetSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self) -> Budget:
    return Budget.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)