"""
Django admin configuration for the Expense Tracker application.
This module customizes how the models are displayed and managed in the Django admin interface.
"""

from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    
    Attributes:
        list_display (tuple): Fields to display in the categories list view
            - name: Display the category name
    """
    list_display = ('name',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Expense model with enhanced display and filtering options.
    
    Attributes:
        list_display (tuple): Fields shown in the expenses list view
            - title: Expense title
            - amount: Monetary value
            - category: Associated category
            - user: User who created the expense
        
        list_filter (tuple): Fields available for filtering in the sidebar
            - category: Filter by expense category
            - user: Filter by user who created the expense
        
        search_fields (tuple): Fields searched when using the admin search bar
            - title: Search in expense titles
            - description: Search in expense descriptions
    """
    list_display = ('title', 'amount', 'category', 'user')
    list_filter = ('category', 'user')
    search_fields = ('title', 'description')
