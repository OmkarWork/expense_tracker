"""
URL configuration for expense_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from expenses import views as expense_views

# Main URL patterns for the entire project
urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # Include all URLs from the expenses app under the root path
    path('', include(('expenses.urls', 'expenses'), namespace='expenses')),
    
    # User authentication views
    path('login/', auth_views.LoginView.as_view(
        template_name='expenses/login.html',
        redirect_authenticated_user=True,  # Redirect if user is already logged in
        next_page='expenses:home'  # Redirect to home page after login
    ), name='login'),
    
    # User logout view
    path('logout/', auth_views.LogoutView.as_view(
        template_name='expenses/logged_out.html',
        next_page='expenses:home'  # Redirect to home page after logout
    ), name='logout'),
    
    # User registration view
    path('signup/', expense_views.signup, name='signup'),
]
