from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Flowable, Spacer
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

class SVGImage(Flowable):
    """
    Custom Flowable class for rendering SVG images in ReportLab PDFs
    Inherits from Flowable to integrate with ReportLab's document building process
    
    Features:
    - Renders SVG with a circular background
    - Supports custom dimensions
    - Maintains aspect ratio
    """
    
    def __init__(self, svg_drawing, width=35, height=35):
        """
        Initialize SVG image with custom dimensions
        
        Args:
            svg_drawing: SVG drawing object from svglib
            width: Width of the image (default: 35 points)
            height: Height of the image (default: 35 points)
        """
        Flowable.__init__(self)
        self.svg_drawing = svg_drawing
        self.width = width
        self.height = height
        
    def draw(self):
        """
        Render the SVG image on the PDF canvas
        
        Process:
        1. Draws a circular red background
        2. Places the SVG image on top
        3. Handles proper positioning and state management
        """
        # Draw red circle background (matching --accent-color from base.html)
        self.canv.setFillColor(colors.HexColor('#e74c3c'))
        self.canv.circle(self.width/2, self.height/2, min(self.width, self.height)/2, fill=1)
        
        # Draw the SVG on top in white
        self.canv.saveState()  # Save current graphics state
        self.canv.translate(2, 2)  # Offset by 2 points for better centering
        renderPDF.draw(self.svg_drawing, self.canv, 0, 0)
        self.canv.restoreState()  # Restore graphics state

    def wrap(self, *args):
        """
        Define the space needed for this flowable
        
        Returns:
            tuple: (width, height) in points
        """
        return (self.width, self.height)
from .models import Expense, Category
from django.db.models import Sum
from django.utils import timezone

@login_required
def delete_expense(request, expense_id):
    """
    Delete a specific expense entry if it belongs to the requesting user.
    
    Args:
        request: HttpRequest object containing metadata about the request
        expense_id: Integer ID of the expense to delete
    
    Returns:
        HttpResponseRedirect to the expense list page with a success/error message
    
    Security:
        - Requires user authentication (@login_required)
        - Verifies expense ownership before deletion
    """
    try:
        # Attempt to get expense that belongs to the current user
        expense = Expense.objects.get(id=expense_id, user=request.user)
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
    except Expense.DoesNotExist:
        messages.error(request, 'Expense not found!')
    return redirect('expenses:expense_list')

@login_required
def calculators(request):
    """
    Display the financial calculators page.
    
    This view renders a page with various financial calculators including:
    - Basic Calculator
    - Split Bill Calculator
    - GST Calculator
    - EMI Calculator
    
    Args:
        request: HttpRequest object containing metadata about the request
    
    Returns:
        HttpResponse rendering the calculators.html template
    
    Security:
        - Requires user authentication (@login_required)
    """
    return render(request, 'expenses/calculators.html')

def signup(request):
    """
    Handle user registration.
    
    GET: Display the signup form
    POST: Process the signup form data and create a new user
    
    Features:
    - Password matching validation
    - Username uniqueness check
    - Django's built-in password validation
    - Comprehensive error messaging
    
    Args:
        request: HttpRequest object containing metadata about the request
    
    Returns:
        HttpResponse: 
        - On GET: renders signup form
        - On POST success: redirects to login page
        - On POST error: redisplays form with error messages
    """
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
    """
    Display the home page dashboard.
    
    For authenticated users, shows recent expenses.
    For anonymous users, shows general welcome page.
    
    Features:
    - Displays 5 most recent expenses for logged-in users
    - Formats currency amounts in Indian Rupee format
    
    Args:
        request: HttpRequest object containing metadata about the request
    
    Returns:
        HttpResponse rendering the home.html template with context
        containing recent expenses (if user is authenticated)
    """
    context = {}
    if request.user.is_authenticated:
        recent_expenses = Expense.objects.filter(user=request.user)[:5]
        for expense in recent_expenses:
            expense.formatted_amount = format_indian_currency(expense.amount)
        context['expenses'] = recent_expenses
    return render(request, 'expenses/home.html', context)

def format_indian_currency(amount):
    """
    Formats a numerical amount into Indian currency format with Rs. symbol
    
    Args:
        amount: A numerical value (int/float) or string that can be converted to float
        
    Returns:
        str: Formatted string in the format "(Rs. X,XXX.XX)"
             For negative amounts: "-(Rs. X,XXX.XX)"
    
    Example:
        format_indian_currency(1234.56) -> "(Rs. 1,234.56)"
        format_indian_currency(-1234.56) -> "-(Rs. 1,234.56)"
        format_indian_currency("invalid") -> "(Rs. 0.00)"
    """
    try:
        # Convert input to float (handles both string and numeric inputs)
        amount = float(amount)
        
        # Handle negative amounts
        if amount < 0:
            return f"-(Rs. {abs(amount):,.2f})"  # Use abs() to show positive number after minus sign
        
        # Handle positive amounts
        return f"(Rs. {amount:,.2f})"  # .2f ensures 2 decimal places
    
    except (ValueError, TypeError):
        # Return default format if conversion fails
        return "(Rs. 0.00)"

@login_required
def expense_list(request):
    """
    Display a list of all expenses for the current user.
    
    Features:
    - Dynamic sorting by multiple fields
    - Total expenses calculation
    - Currency formatting for amounts
    - Category filtering options
    
    Args:
        request: HttpRequest object containing metadata about the request
        - Optional query parameter 'sort' for specifying sort field
    
    Returns:
        HttpResponse rendering the expense_list.html template with context:
        - expenses: QuerySet of Expense objects
        - total: Formatted total amount
        - categories: Available expense categories
        - current_sort: Current sort field
    
    Security:
        - Requires user authentication (@login_required)
        - Only shows expenses belonging to the current user
    """
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
    """
    Handle expense creation.
    
    GET: Display the add expense form
    POST: Process the form data and create a new expense
    
    Features:
    - Category selection
    - Optional description
    - Date and time fields with current defaults
    - Error handling for invalid inputs
    
    Args:
        request: HttpRequest object containing metadata about the request
        
    Form Fields:
        - title: Name/description of the expense
        - amount: Monetary value
        - category: Selected expense category
        - description: Optional detailed notes
        - date: Date of expense (defaults to today)
        - time: Time of expense (defaults to now)
    
    Returns:
        HttpResponse: 
        - On GET: renders add_expense form
        - On POST success: redirects to expense list
        - On POST error: redisplays form with error messages
    
    Security:
        - Requires user authentication (@login_required)
    """
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

import os
from PIL import Image
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from django.conf import settings

def render_to_pdf(template_src, context_dict={}):
    """
    Generates a PDF document from a template and context data
    
    Args:
        template_src: Template path (not used in current implementation)
        context_dict: Dictionary containing data for PDF generation
                     Required keys: 'user', 'expenses', 'total', 'today'
    
    Returns:
        HttpResponse: PDF file as a response with appropriate content type
    """
    # Create a buffer to receive PDF data
    buffer = BytesIO()
    
    # Import necessary modules for PDF generation
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    from reportlab.lib.fonts import addMapping
    
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=50, bottomMargin=50, leftMargin=40, rightMargin=40)
    elements = []
    
    # Create logo SVG content with white fill
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-currency-exchange" viewBox="0 0 16 16">
  <path d="M0 5a5 5 0 0 0 4.027 4.905 6.5 6.5 0 0 1 .544-2.073C3.695 7.536 3.132 6.864 3 5.91h-.5v-.426h.466V5.05q-.001-.07.004-.135H2.5v-.427h.511C3.236 3.24 4.213 2.5 5.681 2.5c.316 0 .59.031.819.085v.733a3.5 3.5 0 0 0-.815-.082c-.919 0-1.538.466-1.734 1.252h1.917v.427h-1.98q-.004.07-.003.147v.422h1.983v.427H3.93c.118.602.468 1.03 1.005 1.229a6.5 6.5 0 0 1 4.97-3.113A5.002 5.002 0 0 0 0 5m16 5.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0m-7.75 1.322c.069.835.746 1.485 1.964 1.562V14h.54v-.62c1.259-.086 1.996-.74 1.996-1.69 0-.865-.563-1.31-1.57-1.54l-.426-.1V8.374c.54.06.884.347.966.745h.948c-.07-.804-.779-1.433-1.914-1.502V7h-.54v.629c-1.076.103-1.808.732-1.808 1.622 0 .787.544 1.288 1.45 1.493l.358.085v1.78c-.554-.08-.92-.376-1.003-.787zm1.96-1.895c-.532-.12-.82-.364-.82-.732 0-.41.311-.719.824-.809v1.54h-.005zm.622 1.044c.645.145.943.38.943.796 0 .474-.37.8-1.02.86v-1.674z"/>
</svg>'''
    
    # Save SVG to temporary file
    svg_file = BytesIO(svg_content.encode('utf-8'))
    drawing = svg2rlg(svg_file)
    
    # Create header
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    
    # Scale the drawing for better visibility
    drawing.scale(1.2, 1.2)
    
    # Create table for logo and EXPO text side by side
    header_table = Table([
        [SVGImage(drawing), Paragraph("EXPO", header_style)]
    ], colWidths=[35, None])
    
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 30))  # Add 30 points of vertical space after logo
    elements.append(Paragraph(f"Expense Bill", styles['Heading1']))
    elements.append(Spacer(1, 20))  # Add 20 points of vertical space after title
    elements.append(Paragraph(f"User: {context_dict['user'].username}", styles['Normal']))
    elements.append(Paragraph(f"Generated: {context_dict['today']}", styles['Normal']))
    elements.append(Spacer(1, 20))  # Add 20 points of vertical space before table
    
    # Create table data
    table_data = [['Date', 'Time', 'Title', 'Category', 'Description', 'Amount (Rs.)']]
    
    for expense in context_dict['expenses']:
        table_data.append([
            expense.formatted_date,
            expense.formatted_time,
            expense.title,
            expense.category.name if expense.category else '-',
            expense.description or '-',
            expense.formatted_amount
        ])
    
    # Add total row
    table_data.append(['', '', '', '', 'Total Amount', context_dict['total']])
    
    # Set column widths proportionally
    col_widths = [80, 80, 100, 80, 150, 80]
    
    # Create table and style it
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Body style
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
        ('TOPPADDING', (0, 1), (-1, -2), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f8f9fa')]),
        
        # Total row style
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, -1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        
        # Grid style
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),  # Right align all amounts
        ('ALIGN', (-2, -1), (-1, -1), 'RIGHT'),  # Right align total row text
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 30))  # Add 30 points of vertical space after table
    
    # Add footer
    footer_style = ParagraphStyle(
        'CustomFooter',
        parent=styles['Normal'],
        textColor=colors.gray,
        fontSize=10,
        spaceAfter=30,
        fontName='Helvetica',
        alignment=1  # Center alignment
    )
    elements.append(Paragraph("<br/><br/>Thank you for using Expense Tracker", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response.write(pdf)
    return response

@login_required
def generate_bill(request):
    """
    View function to generate a PDF bill of user's expenses
    
    Process:
    1. Retrieves user's expenses from database
    2. Formats all dates, times and amounts
    3. Calculates total amount
    4. Generates PDF using render_to_pdf function
    
    Returns:
        HttpResponse: PDF file as response
    """
    # Get current user's expenses ordered by date and time (newest first)
    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-time')

    # Calculate total amount of all expenses
    # Uses aggregate with Sum, returns 0 if no expenses found
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
