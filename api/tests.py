"""Test suite ran on github actions"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


REGO_PATH = "/api/auth/register/"
AUTH_PATH = "/api/auth/login/"
ACCT_PATH = "/api/accounts/"

USER_SIGN_UP = {
  "username": "testuser",
  "password": "testpass123",
  "email"   : "test@test.com"
}

USER_SIGN_IN = {
  "username": "testuser",
  "password": "testpass123",
}

BAD_SIGN_IN = {
  "username": "wronguser",
  "password": "wrongpass"
}

ACCOUNT = {
  "name": "Cash",
  "type": "debit",
  "balance": 1000.0,
  "currency": "GBP"
}

BAD_ACCOUNT = {
  "name": "Cash",
  "type": "debit",
  "balance": "baddata",
  "currency": "GBP"
}

BAD_DATA = {
  "data": "baddata"
}


class AuthTests(TestCase):
  """Authentification functionality"""

  def setUp(self):
    self.client = APIClient()

  def test_register(self) -> None:
    """Basic sign up functionality testing"""

    ### post basic sign-up info
    response = self.client.post(REGO_PATH, USER_SIGN_IN)

    ### require 201 success response
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn("token", response.data)

  def test_login(self) -> None:
    """Basic sign in (from sign up) functionality"""

    ### pretend we already have the user from registry testing
    User.objects.create_user(
      username=USER_SIGN_IN["username"], 
      password=USER_SIGN_IN["password"]
    )

    ### post basic sign-in info
    response = self.client.post(AUTH_PATH, USER_SIGN_IN)

    ### require 200 all correct response
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("token", response.data)

  def test_login_invalid_credentials(self) -> None:
    """Check validity of sign in"""

    ### post bad sign-in attempt
    response = self.client.post(AUTH_PATH, BAD_SIGN_IN)

    ### require 401 bad authentification response
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountTests(TestCase):
  """User account functionality"""

  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(
      username=USER_SIGN_IN["username"], 
      password=USER_SIGN_IN["password"]
    )
    self.client.force_authenticate(user=self.user)

  def test_create_account(self) -> None:
    """Test valid account creation"""

    ### post general cash account
    response = self.client.post(ACCT_PATH, ACCOUNT)

    ### require 201 success response
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_create_bad_account(self) -> None:
    """Test bad account data creation"""

    ### post bad data, require 400 bad request response
    response = self.client.post(ACCT_PATH, BAD_DATA)
    self.assertEqual(
      response.status_code, status.HTTP_400_BAD_REQUEST)

    ### post almost valid account, require 400 still
    response = self.client.post(ACCT_PATH, BAD_ACCOUNT)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


  def test_unauth_create_account(self) -> None:
    """Test unauthorised account creation"""

    ### force non-user
    self.client.force_authenticate(user=None)

    ### attempt valid post
    response = self.client.post(ACCT_PATH, ACCOUNT)

    ### require 401 unauthorised response
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


  def test_list_accounts(self):
    """Test account list functionality"""

    ### get accounts, require 200 all correct response
    response = self.client.get(ACCT_PATH)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_unauthenticated_access(self):
    """Test unauthorised list request"""
    
    ### force non-user
    self.client.force_authenticate(user=None)

    ### get accounts, require 401 unauthorised response
    response = self.client.get('/api/accounts/')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)