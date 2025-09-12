from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_initial_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='expense',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
