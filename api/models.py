from django.db import models

from django.db import models

class User(models.Model):
  """User model represents a user in the system"""

  username      = models.CharField(max_length=150, unique=True)
  email         = models.EmailField(unique=True)
  password_hash = models.CharField(max_length=255)
  is_active     = models.BooleanField(default=True)
  created_at    = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.username


class Account(models.Model):
  """Account model represents a financial start/endpoint for transactions"""

  ACCOUNT_TYPES = [
    ("checking", "Checking"),
    ("savings", "Savings"),
    ("cash", "Cash"),
  ]

  user       = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="accounts")
  name       = models.CharField(max_length=150)
  type       = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
  balance    = models.FloatField(default=0.0)
  currency   = models.CharField(max_length=10, default="GBP")
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Category(models.Model):
  """Type of transaction, either credit or debit"""
  
  CATEGORY_TYPES = [
    ("income", "Income"),
    ("expense", "Expense"),
  ]

  user       = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="categories")
  name       = models.CharField(max_length=150)
  type       = models.CharField(max_length=20, choices=CATEGORY_TYPES)
  colour     = models.CharField(max_length=7, default="#000000")
  is_default = models.BooleanField(default=False)

  def __str__(self):
    return self.name


class Transaction(models.Model):
  """Transaction model represents a financial transaction"""

  TRANSACTION_TYPES = [
    ("income", "Income"),
    ("expense", "Expense"),
  ]

  account     = models.ForeignKey(
    Account, on_delete=models.CASCADE, related_name="transactions")
  category    = models.ForeignKey(
    Category, on_delete=models.SET_NULL, null=True, blank=True)
  amount      = models.FloatField()
  type        = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
  description = models.CharField(max_length=255, blank=True, null=True)
  date        = models.DateTimeField()
  created_at  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.type} - {self.amount}"


class Budget(models.Model):
  """Budget"""
  
  PERIOD_TYPES = [
    ("monthly", "Monthly"),
    ("weekly", "Weekly"),
  ]

  user         = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="budgets")
  category     = models.ForeignKey(Category, on_delete=models.CASCADE)
  amount_limit = models.FloatField()
  period       = models.CharField(max_length=20, choices=PERIOD_TYPES)
  start_date   = models.DateTimeField()

  def __str__(self):
    return f"{self.category} - {self.period}"