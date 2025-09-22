"""
This module defines the database models for the Expense Tracker application.
It includes models for expense categories and individual expenses, with proper
relationships and formatting methods for display purposes.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """
    Represents a category for classifying expenses.
    
    A category is a simple model with just a name field, used to organize
    expenses into logical groups like 'Food', 'Transportation', etc.
    
    Attributes:
        name (CharField): The name of the category, limited to 50 characters.
    """
    name = models.CharField(max_length=50, help_text='Name of the expense category')

    def __str__(self):
        """Returns a string representation of the category."""
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'  # Proper pluralization in admin interface

class Expense(models.Model):
    """
    Represents an individual expense entry in the system.
    
    This is the main model of the application, storing all expense-related
    information including amount, category, date/time, and user reference.
    
    Attributes:
        title (CharField): Title/name of the expense, limited to 100 characters
        amount (DecimalField): Monetary amount with up to 10 digits and 2 decimal places
        description (TextField): Optional detailed description of the expense
        user (ForeignKey): Reference to the Django User who created the expense
        category (ForeignKey): Optional reference to expense Category
        date (DateField): Date of the expense, defaults to current date
        time (TimeField): Time of the expense, defaults to current time
    """
    title = models.CharField(max_length=100, help_text='Title of the expense')
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Amount in Indian Rupees (₹)'
    )
    description = models.TextField(
        blank=True,
        help_text='Optional detailed description of the expense'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text='User who created this expense'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text='Category of the expense'
    )
    date = models.DateField(
        default=timezone.now,
        help_text='Date when the expense occurred'
    )
    time = models.TimeField(
        default=timezone.now,
        help_text='Time when the expense occurred'
    )

    class Meta:
        ordering = ['-date', '-time']  # Sort expenses by newest first

    def __str__(self):
        """Returns a string representation combining title and formatted amount."""
        return f"{self.title} - {self.formatted_amount()}"
    
    def formatted_amount(self):
        """
        Formats the expense amount in Indian currency format with ₹ symbol.
        
        Returns:
            str: Formatted amount string (e.g., "₹1,234.56" or "-₹1,234.56")
                Returns "₹0.00" if amount is invalid.
        
        Examples:
            >>> expense = Expense(amount=1234.56)
            >>> expense.formatted_amount()
            '₹1,234.56'
            >>> expense = Expense(amount=-1234.56)
            >>> expense.formatted_amount()
            '-₹1,234.56'
        """
        try:
            if self.amount < 0:
                return f"-₹{abs(float(self.amount)):,.2f}"
            return f"₹{float(self.amount):,.2f}"
        except (ValueError, TypeError):
            return "₹0.00"
            
    def formatted_datetime(self):
        """
        Formats the expense date and time in a human-readable format.
        
        Returns:
            str: Formatted date and time string in the format:
                "DD Mon YYYY at HH:MM AM/PM" if both date and time exist
                "DD Mon YYYY" if only date exists
                "No date" if neither exists or if format is invalid
        
        Examples:
            >>> from datetime import date, time
            >>> expense = Expense(date=date(2025, 9, 22), time=time(14, 30))
            >>> expense.formatted_datetime()
            '22 Sep 2025 at 02:30 PM'
        """
        try:
            if self.date and self.time:
                return f"{self.date.strftime('%d %b %Y')} at {self.time.strftime('%I:%M %p')}"
            elif self.date:
                return self.date.strftime('%d %b %Y')
            else:
                return "No date"
        except (AttributeError, ValueError):
            return "No date"
