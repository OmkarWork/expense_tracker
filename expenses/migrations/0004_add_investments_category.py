from django.db import migrations

def add_investments_category(apps, schema_editor):
    Category = apps.get_model('expenses', 'Category')
    # Check if Investments category already exists
    if not Category.objects.filter(name='Investments').exists():
        Category.objects.create(name='Investments')

class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_add_date_time_fields'),
    ]

    operations = [
        migrations.RunPython(add_investments_category),
    ]
