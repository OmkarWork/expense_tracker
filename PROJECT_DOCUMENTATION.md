# Expense Tracker - Project Documentation

## Table of Contents
1. [UML and ER Diagrams](#1-uml-and-er-diagrams)
2. [Introduction](#2-introduction)
3. [System Requirement Analysis](#3-system-requirement-analysis)
4. [Implementation](#4-implementation)
5. [Testing](#5-testing)
6. [Results & Challenges](#6-results--challenges)
7. [Conclusion](#7-conclusion)
8. [Future Scope](#8-future-scope)
9. [References](#9-references)

## 1. UML and ER Diagrams

### 1.1 Entity Relationship (ER) Diagram
```
+---------------+       +---------------+
|    User       |       |   Category    |
+---------------+       +---------------+
| PK: id        |       | PK: id        |
| username      |       | name          |
| password      |       |               |
+---------------+       +---------------+
        |                      |
        |                      |
        |                      |
        |              +---------------+
        +------------->|   Expense     |
                      +---------------+
                      | PK: id        |
                      | FK: user_id   |
                      | FK: category_id|
                      | title         |
                      | amount        |
                      | description   |
                      | date          |
                      | time          |
                      +---------------+
```

### 1.2 UML Class Diagram
```
+------------------+
|     Category     |
+------------------+
| - name: str      |
+------------------+
| + __str__()      |
+------------------+
         ^
         |
+------------------+
|     Expense      |
+------------------+
| - title: str     |
| - amount: decimal |
| - description: str|
| - user: User     |
| - category: Category|
| - date: Date     |
| - time: Time     |
+------------------+
| + __str__()      |
| + formatted_amount()|
| + formatted_datetime()|
+------------------+
```

## 2. Introduction

### 2.1 Project Overview
The Expense Tracker is a web-based application developed using Django framework that helps users manage their personal finances effectively. It provides a user-friendly interface for tracking daily expenses, categorizing spending, and generating detailed expense reports.

### 2.2 Problem Statement
In today's fast-paced world, managing personal finances has become increasingly challenging. Many individuals struggle to:
- Track their daily expenses effectively
- Categorize their spending
- Understand their spending patterns
- Maintain proper financial records
- Generate expense reports

### 2.3 Objectives
1. Create a secure user authentication system
2. Implement expense tracking with categorization
3. Provide Indian currency (₹) support
4. Enable expense report generation in PDF format
5. Offer financial calculators for common calculations
6. Create an intuitive and responsive user interface

## 3. System Requirement Analysis

### 3.1 Functional Requirements
1. User Management:
   - User registration
   - User authentication
   - Password validation
   - Session management

2. Expense Management:
   - Add new expenses
   - Delete existing expenses
   - Categorize expenses
   - View expense list
   - Sort expenses by different criteria
   - Calculate total expenses

3. Report Generation:
   - Generate PDF expense reports
   - Customize report layout
   - Include expense summaries

4. Financial Tools:
   - Basic calculator
   - Split bill calculator
   - GST calculator
   - EMI calculator

### 3.2 Technical Requirements
1. Software Requirements:
   - Python 3.12
   - Django 5.2.5
   - ReportLab 4.4.3
   - Other Python packages (listed in requirements.txt)

2. Development Tools:
   - Visual Studio Code
   - Git for version control
   - SQLite for development database

3. Browser Support:
   - Chrome (latest)
   - Firefox (latest)
   - Safari (latest)
   - Edge (latest)

## 4. Implementation

### 4.1 Technology Stack
- Backend: Python 3.12, Django 5.2.5
- Database: SQLite3
- Frontend: HTML5, CSS3, Bootstrap 5.1
- PDF Generation: ReportLab
- Additional Libraries: 
  - svglib for SVG handling
  - pypdf for PDF manipulation
  - python-dotenv for environment variables

### 4.2 Core Components

1. Models:
   - Category: Stores expense categories
   - Expense: Stores expense details with user and category relations

2. Views:
   - Authentication views (login, logout, signup)
   - Expense management views (add, list, delete)
   - Report generation view
   - Calculator views

3. Templates:
   - Base template with common layout
   - Expense forms and lists
   - Calculator interfaces
   - PDF report templates

### 4.3 Key Features Implementation

1. Currency Formatting:
```python
def formatted_amount(self):
    try:
        if self.amount < 0:
            return f"-₹{abs(float(self.amount)):,.2f}"
        return f"₹{float(self.amount):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"
```

2. PDF Generation:
```python
def render_to_pdf(template_src, context_dict={}):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    # ... PDF generation logic ...
    return response
```

## 5. Testing

### 5.1 Unit Testing
1. Model Testing:
   - Category model creation and string representation
   - Expense model creation and formatting methods
   - Currency formatting edge cases

2. View Testing:
   - Authentication flows
   - Expense CRUD operations
   - PDF generation

### 5.2 Integration Testing
1. User Workflows:
   - Registration to expense addition
   - Expense management workflow
   - Report generation process

2. Security Testing:
   - Authentication required views
   - User data isolation
   - Form validation

### 5.3 Performance Testing
1. Database Queries:
   - Expense listing with filters
   - PDF generation with large datasets

2. Response Times:
   - Page load times
   - PDF generation time

## 6. Results & Challenges

### 6.1 Results
1. Successful Implementation:
   - Secure user authentication system
   - Efficient expense tracking
   - PDF report generation
   - Financial calculators
   - Mobile-responsive design

2. Performance Metrics:
   - Quick expense addition process
   - Fast PDF generation
   - Efficient data retrieval

### 6.2 Challenges Faced
1. Technical Challenges:
   - Indian Rupee symbol rendering in PDF
   - PDF layout optimization
   - Date/time formatting
   - Currency precision handling

2. Solutions Implemented:
   - Custom currency formatting
   - PDF template optimization
   - Proper exception handling
   - Input validation improvements

## 7. Conclusion
The Expense Tracker project successfully delivers a comprehensive solution for personal expense management. The implementation meets all initial objectives and provides:
- Secure user authentication
- Efficient expense tracking
- Detailed expense reporting
- Useful financial calculators
- User-friendly interface

The project demonstrates practical application of:
- Django web framework
- Database design
- PDF generation
- User interface design
- Security implementation

## 8. Future Scope
1. Feature Enhancements:
   - Multi-currency support
   - Budget planning tools
   - Expense analytics dashboard
   - Income tracking
   - Investment portfolio management

2. Technical Improvements:
   - API development for mobile apps
   - Cloud database migration
   - Performance optimization
   - Advanced analytics
   - Machine learning for expense predictions

3. Integration Possibilities:
   - Bank account integration
   - Payment gateway integration
   - Export to accounting software
   - Mobile app development
   - Email notifications

## 9. References

1. Django Documentation:
   - https://docs.djangoproject.com/en/5.2/
   - Used for framework implementation

2. ReportLab Documentation:
   - https://www.reportlab.com/docs/reportlab-userguide.pdf
   - Referenced for PDF generation

3. Bootstrap Documentation:
   - https://getbootstrap.com/docs/5.1/
   - Used for frontend design

4. Python Documentation:
   - https://docs.python.org/3.12/
   - Core language reference

5. Additional Resources:
   - MDN Web Docs (https://developer.mozilla.org/)
   - Django Rest Framework docs (https://www.django-rest-framework.org/)
   - Git Documentation (https://git-scm.com/doc)