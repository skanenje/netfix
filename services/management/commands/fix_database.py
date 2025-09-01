from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix database schema issues'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if the table exists and what columns it has
            cursor.execute("PRAGMA table_info(services_service);")
            columns = cursor.fetchall()
            
            self.stdout.write("Current services_service table structure:")
            for column in columns:
                self.stdout.write(f"  {column[1]} ({column[2]})")
            
            # Check if price_per_hour column exists
            column_names = [col[1] for col in columns]
            if 'price_per_hour' not in column_names:
                if 'price_hour' in column_names:
                    self.stdout.write("Found 'price_hour' column, need to rename to 'price_per_hour'")
                    self.stdout.write("Please run: python manage.py migrate")
                else:
                    self.stdout.write("Neither 'price_per_hour' nor 'price_hour' found!")
            else:
                self.stdout.write("✓ price_per_hour column exists")