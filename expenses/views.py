from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

from django.conf import settings
from .models import Expense, Category
from django.db.models import Sum
from django.utils import timezone

@login_required
def delete_expense(request, expense_id):
    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
    except Expense.DoesNotExist:
        messages.error(request, 'Expense not found!')
    return redirect('expenses:expense_list')

@login_required
def calculators(request):
    return render(request, 'expenses/calculators.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'expenses/signup.html')

        try:
            # Check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return render(request, 'expenses/signup.html')

            # Validate password
            validate_password(password1)
            
            # Create user
            user = User.objects.create_user(username=username, password=password1)
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'expenses/signup.html')

def home(request):
    context = {}
    if request.user.is_authenticated:
        recent_expenses = Expense.objects.filter(user=request.user)[:5]
        for expense in recent_expenses:
            expense.formatted_amount = format_indian_currency(expense.amount)
        context['expenses'] = recent_expenses
    return render(request, 'expenses/home.html', context)

def format_indian_currency(amount):
    """Format amount in Indian numbering system"""
    try:
        amount = float(amount)
        if amount < 0:
            return f"-₹{abs(amount):,.2f}"
        return f"₹{amount:,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

@login_required
def expense_list(request):
    # Get the sort parameter from request, default to '-date'
    sort_by = request.GET.get('sort', '-date')
    valid_sort_fields = ['amount', '-amount', 'title', '-title', 'category', '-category', 'date', '-date']
    if sort_by not in valid_sort_fields:
        sort_by = '-date'

    expenses = Expense.objects.filter(user=request.user).order_by(sort_by)
    
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    formatted_total = format_indian_currency(total)
    categories = Category.objects.all()
    
    # Format amounts
    for expense in expenses:
        expense.formatted_amount = format_indian_currency(expense.amount)
    
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'total': formatted_total,
        'categories': categories,
        'current_sort': sort_by
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        description = request.POST.get('description', '')
        date = request.POST.get('date', timezone.now().date().isoformat())
        time = request.POST.get('time', timezone.now().time().strftime('%H:%M'))

        try:
            category = Category.objects.get(id=category_id) if category_id else None
            expense = Expense.objects.create(
                title=title,
                amount=amount,
                category=category,
                description=description,
                user=request.user,
                date=date,
                time=time
            )
            messages.success(request, 'Expense added successfully!')
            return redirect('expenses:expense_list')
        except Exception as e:
            messages.error(request, f'Error adding expense: {str(e)}')
    
    now = timezone.now()
    categories = Category.objects.all()
    return render(request, 'expenses/add_expense.html', {
        'categories': categories,
        'today': now.date(),
        'now': now
    })


# ------------------ BILL GENERATOR ------------------

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return result

@login_required
def generate_bill(request):
    # get only current user's expenses and order them
    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-time')

    # aggregate total (raw decimal)
    total_raw = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # prepare formatted fields for template
    for exp in expenses:
        # formatted amount like "₹1,234.56"
        exp.formatted_amount = format_indian_currency(exp.amount)

        # formatted date/time for display
        try:
            exp.formatted_date = exp.date.strftime('%d %b %Y')
        except Exception:
            exp.formatted_date = str(exp.date) if exp.date else '-'
        try:
            exp.formatted_time = exp.time.strftime('%I:%M %p')
        except Exception:
            exp.formatted_time = str(exp.time) if exp.time else '-'

    # formatted total for display
    formatted_total = format_indian_currency(total_raw)

    context = {
        'expenses': expenses,
        'total': formatted_total,   # string like "₹1,234.56"
        'user': request.user,
        'today': timezone.now().date()
    }
    return render_to_pdf('expenses/bill.html', context)
