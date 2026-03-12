
from rest_framework import viewsets, permissions
from .models import Account, Category, Transaction, Budget
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer, BudgetSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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
