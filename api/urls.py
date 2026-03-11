from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(
  r'accounts', views.AccountViewSet, basename="account")
router.register(
  r'categories', views.CategoryViewSet, basename="category")
router.register(
  r'transactions', views.TransactionViewSet, basename="transaction")
router.register(
  r'budgets', views.BudgetViewSet, basename="budget")


urlpatterns = [
  path('', include(router.urls)),
  path("auth/register/", views.register, name="register"),
  path("auth/login/", views.login, name="login"),
  path("auth/logout/", views.logout, name="logout"),
]