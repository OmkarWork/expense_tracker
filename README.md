# Expense Tracker

A Django-based expense tracking application that helps users manage their personal finances effectively.

## Features

- User Authentication (Login/Signup)
- Add, View, and Delete Expenses
- Categorize Expenses (Food, Transportation, Utilities, etc.)
- Date and Time Tracking for Expenses
- Indian Currency (INR) Formatting
- Sort Expenses by Different Fields
- Financial Calculators:
  - Basic Calculator
  - Split Bill Calculator
  - GST Calculator
  - EMI Calculator

## Tech Stack

- Python 3.12
- Django 5.2
- Bootstrap 5.1
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd expense_tracker
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your browser

## Usage

1. Sign up for a new account or login with existing credentials
2. Add expenses with title, amount, category, description, date, and time
3. View your expenses list and sort by different fields
4. Use various calculators for financial calculations
5. Track your total expenses
6. Delete unwanted expenses

## Project Structure

```
expense_tracker/
├── expense_tracker/        # Project settings and main URLs
├── expenses/              # Main app
│   ├── migrations/       # Database migrations
│   ├── templates/       # HTML templates
│   ├── admin.py        # Admin configuration
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   └── urls.py         # App URLs
├── manage.py            # Django management script
├── .gitignore          # Git ignore file
└── README.md           # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
