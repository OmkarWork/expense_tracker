from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('calculators/', views.calculators, name='calculators'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('generate-bill/', views.generate_bill, name='generate_bill'),
    # NEW BILL ROUTES


]
