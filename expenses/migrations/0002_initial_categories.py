from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('expenses', 'Category')
    categories = [
        'Food',
        'Transportation',
        'Entertainment',
        'Shopping',
        'Bills',
        'Healthcare',
        'Education',
        'Investments',
        'Other'
    ]
    for category_name in categories:
        Category.objects.create(name=category_name)

def remove_initial_categories(apps, schema_editor):
    Category = apps.get_model('expenses', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories, remove_initial_categories),
    ]
