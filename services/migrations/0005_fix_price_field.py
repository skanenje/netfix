# Generated migration to fix price field name and other inconsistencies

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_requestedservice_id_alter_service_id'),
    ]

    operations = [
        # Rename price_hour to price_per_hour
        migrations.RenameField(
            model_name='service',
            old_name='price_hour',
            new_name='price_per_hour',
        ),
        # Rename date to created_date for consistency
        migrations.RenameField(
            model_name='service',
            old_name='date',
            new_name='created_date',
        ),
        # Update the field to match current model
        migrations.AlterField(
            model_name='service',
            name='price_per_hour',
            field=models.DecimalField(
                decimal_places=2, 
                max_digits=10, 
                validators=[django.core.validators.MinValueValidator(0)],
                default=0.00
            ),
        ),
        # Update created_date field
        migrations.AlterField(
            model_name='service',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        # Update field choices to match current model
        migrations.AlterField(
            model_name='service',
            name='field',
            field=models.CharField(
                max_length=30, 
                choices=[
                    ('Air Conditioner', 'Air Conditioner'),
                    ('Carpentry', 'Carpentry'),
                    ('Electricity', 'Electricity'),
                    ('Gardening', 'Gardening'),
                    ('Home Machines', 'Home Machines'),
                    ('Housekeeping', 'Housekeeping'),
                    ('Interior Design', 'Interior Design'),
                    ('Locks', 'Locks'),
                    ('Painting', 'Painting'),
                    ('Plumbing', 'Plumbing'),
                    ('Water Heaters', 'Water Heaters')
                ]
            ),
        ),
        # Remove rating field if it exists (not in current model)
        migrations.RemoveField(
            model_name='service',
            name='rating',
        ),
    ]