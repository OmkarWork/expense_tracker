"""
Django application configuration for the Expense Tracker app.
This module defines the application configuration class for the expenses app.
"""

from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    """
    Configuration class for the expenses application.
    
    This class defines basic application settings and configurations.
    
    Attributes:
        default_auto_field (str): Specifies the type of auto-field to use for model primary keys.
            Using BigAutoField for better scalability with large datasets.
        
        name (str): The Python package name of the application.
            This must match the name of the app's directory.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'
