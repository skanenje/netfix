from django.db import models
from django.core.validators import MinValueValidator
from users.models import Company, Customer
from .choices import SERVICE_FIELD_CHOICES

class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_per_hour = models.DecimalField(
        decimal_places=2, 
        max_digits=10, 
        validators=[MinValueValidator(0)],
        default=0.00
    )
    field = models.CharField(max_length=30, blank=False, null=False, choices=SERVICE_FIELD_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"{self.name} ({self.field}) - {self.company.user.username}"

    def save(self, *args, **kwargs):
        # Validate that the company is allowed to offer this service
        if self.company.field == 'All in One' or self.company.field == self.field:
            super().save(*args, **kwargs)
        else:
            raise ValueError(
                f"A {self.company.field} company cannot offer a {self.field} service."
            )

class RequestedService(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requested_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.TextField()
    hours_needed = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    requested_date = models.DateTimeField(auto_now_add=True)

    @property
    def calculated_cost(self):
        return self.service.price_per_hour * self.hours_needed

    def __str__(self):
        return f"{self.service.name} for {self.customer.user.username}"