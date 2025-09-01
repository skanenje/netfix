from django import forms
from .models import Service
from .choices import SERVICE_FIELD_CHOICES
from users.models import Company

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price_per_hour', 'field']

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            if company.field == 'All in One':
                self.fields['field'].choices = SERVICE_FIELD_CHOICES
            else:
                fixed_choice = (company.field, company.field)
                self.fields['field'].choices = [fixed_choice]
                self.fields['field'].initial = company.field
                self.fields['field'].widget = forms.HiddenInput()

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter Service Name', 'autocomplete': 'off'
        })
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_per_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

    def clean_price_per_hour(self):
        price = self.cleaned_data['price_per_hour']
        if price <= 0:
            raise forms.ValidationError("Price per hour must be positive.")
        return price

class RequestServiceForm(forms.ModelForm):
    class Meta:
        model = RequestedService
        fields = ['address', 'hours_needed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter full address where service is needed'})
        self.fields['hours_needed'].widget.attrs['placeholder'] = 'Enter hours needed'