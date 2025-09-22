"""
URL configuration for the expenses app.

This module defines all URL patterns specific to the expense tracking functionality.
Each URL is mapped to a specific view function that handles the corresponding request.
The app_name provides a namespace for URL reversing.
"""

from django.urls import path
from . import views

app_name = 'expenses'  # Namespace for URL pattern names

# URL patterns for the expenses application
urlpatterns = [
    # Home page displaying dashboard
    path('', views.home, name='home'),
    
    # List all expenses with sorting and filtering options
    path('list/', views.expense_list, name='expense_list'),
    
    # Add new expense form
    path('add/', views.add_expense, name='add_expense'),
    
    # Financial calculators page
    path('calculators/', views.calculators, name='calculators'),
    
    # Delete specific expense by ID
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    
    # Generate PDF bill of expenses
    path('generate-bill/', views.generate_bill, name='generate_bill'),


]
