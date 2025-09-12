# EXPENSE TRACKER
### A Mini Project Report

**Submitted in partial fulfillment of the requirements for the**
**[Your Course Name, e.g., Bachelor of Technology in Computer Science]**

**Submitted By:**
[Your Name]
[Your Roll Number]
[Your Department]

**Under the Guidance of:**
[Faculty Name]
[Designation]

[College Name]
[University Name]
[Academic Year: 2025-26]

---

## Abstract

The Expense Tracker is a web-based application developed to address the growing need for personal financial management among students and professionals. This project implements a user-friendly system for tracking daily expenses, categorizing spending, and performing financial calculations. Built using modern web technologies, it demonstrates the practical application of database management, web development, and user interface design principles.

## 1. Introduction

### 1.1 Problem Statement
In today's fast-paced world, managing personal finances has become increasingly challenging. Many individuals struggle to track their expenses effectively, leading to poor financial management. This project aims to provide a solution through a digital expense tracking system.

### 1.2 Project Objectives
- Create a user-friendly expense tracking system
- Implement secure user authentication
- Provide category-based expense organization
- Include essential financial calculators
- Enable efficient expense data management
- Support Indian currency format

## 2. Literature Review

The development of this project involved studying various existing expense tracking solutions and financial management systems. Key findings include:
- The importance of intuitive user interfaces in financial applications
- The need for secure data handling in personal finance management
- The significance of categorization in expense tracking
- The value of integrated financial calculators

## 3. System Analysis and Design

### 3.1 Technology Stack
- **Backend Framework:** Django 5.2
- **Programming Language:** Python 3.12
- **Database:** SQLite3
- **Frontend:** Bootstrap 5.1
- **Template Engine:** Django Templates

### 3.2 System Architecture

#### 3.2.1 Data Models

#### User Model
- Utilizes Django's built-in `User` model
- Handles authentication and user management
- Fields: username, email, password

#### Category Model
```python
class Category:
- name (CharField, max_length=50)
- Meta: verbose_name_plural = 'Categories'
```

#### Expense Model
```python
class Expense:
- title (CharField, max_length=100)
- amount (DecimalField, max_digits=10, decimal_places=2)
- description (TextField, optional)
- user (ForeignKey to User)
- category (ForeignKey to Category)
- date (DateField)
- time (TimeField)
- Meta: ordering = ['-date', '-time']
```

### 2.2 Core Functionalities

#### User Management
- Secure registration and login system
- Session management
- Password hashing and security

#### Expense Management
- Create, Read, Update, Delete (CRUD) operations
- Automatic date and time tracking
- Indian currency (₹) formatting
- Category-based organization

#### Financial Calculators
1. Basic Calculator
2. Split Bill Calculator
3. GST Calculator
4. EMI Calculator

## 3. Implementation Details

### 3.1 Security Features
- CSRF protection
- User authentication middleware
- Form validation
- Secure password storage

### 3.2 Data Organization
- Expenses are sorted by date and time (newest first)
- Category-based filtering
- User-specific data isolation

### 3.3 Currency Handling
- Decimal precision for accurate calculations
- Indian Rupee (₹) formatting
- Proper handling of negative amounts

## 4. Deployment and Maintenance

### 4.1 Installation Requirements
1. Python 3.12 or higher
2. Django 5.2
3. Virtual environment
4. SQLite3 database

### 4.2 Setup Process
1. Clone repository
2. Create and activate virtual environment
3. Install dependencies
4. Run migrations
5. Create superuser (optional)
6. Start development server

### 4.3 Database Migrations
Current migrations:
1. Initial setup
2. Initial categories
3. Date-time fields addition
4. Investments category addition

## 5. Implementation and Results

### 5.1 Implementation Screenshots
[Include 2-3 key screenshots of your application here]

### 5.2 Test Cases and Results
1. User Registration and Login
   - Test Status: Successful
   - Validation: Proper error handling and security measures implemented

2. Expense Management
   - Test Status: Successful
   - CRUD operations working as expected

3. Calculator Functions
   - Test Status: Successful
   - All calculations providing accurate results

## 6. Conclusion and Future Scope

### 6.1 Conclusion
The Expense Tracker project successfully implements a comprehensive solution for personal expense management. The system meets all initial objectives and provides a robust platform for users to manage their finances effectively. The implementation of features like category-based organization and financial calculators adds significant value to the basic expense tracking functionality.

### 6.2 Future Scope
1. Data Export Features
2. Budget Planning Tools
3. Expense Analytics Dashboard
4. Mobile Application
5. Multi-currency Support

## References

1. Django Documentation - https://docs.djangoproject.com/
2. Bootstrap Documentation - https://getbootstrap.com/docs/
3. Python Documentation - https://docs.python.org/
4. [Other relevant references]

---

**Note:** This project was developed as part of the academic curriculum and demonstrates the practical application of web development concepts using Python and Django framework.
