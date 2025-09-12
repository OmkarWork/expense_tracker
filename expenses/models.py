from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.title} - {self.formatted_amount()}"
    
    def formatted_amount(self):
        try:
            if self.amount < 0:
                return f"-₹{abs(float(self.amount)):,.2f}"
            return f"₹{float(self.amount):,.2f}"
        except (ValueError, TypeError):
            return "₹0.00"
            
    def formatted_datetime(self):
        try:
            if self.date and self.time:
                return f"{self.date.strftime('%d %b %Y')} at {self.time.strftime('%I:%M %p')}"
            elif self.date:
                return self.date.strftime('%d %b %Y')
            else:
                return "No date"
        except (AttributeError, ValueError):
            return "No date"
