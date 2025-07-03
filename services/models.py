from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer
from .choices import FIELD_CHOICES

SERVICE_FIELD_CHOICES = [choice for choice in FIELD_CHOICES if choice[0] != 'All in One']


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
    choices = SERVICE_FIELD_CHOICES
    field = models.CharField(max_length=30, blank=False,
                             null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return f"{self.name} ({self.field}) - {self.company.user.username}"
    
    def save(self, *args, **kwargs):
        # Validate that the company is allowed to offer this service
        if self.company.field == 'All in One' or self.company.field == self.field:
            super().save(*args, **kwargs)
        else:
            raise ValueError(f"A {self.company.field} company cannot offer a {self.field} service.")