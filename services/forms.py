# services/forms.py

from django import forms
from .models import Service
from .choices import SERVICE_FIELD_CHOICES
from users.models import Company


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price_hour', 'field']

    def __init__(self, *args, company=None, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)

        # Set choices based on the company's field
        if company:
            if company.field == 'All in One':
                self.fields['field'].choices = SERVICE_FIELD_CHOICES
            else:
                fixed_choice = (company.field, company.field)
                self.fields['field'].choices = [fixed_choice]
                self.fields['field'].initial = fixed_choice
                self.fields['field'].widget = forms.HiddenInput()

        # Add placeholders and UX improvements
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter Service Name', 'autocomplete': 'off'})
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'


class RequestServiceForm(forms.Form):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Service Address',
        required=True
    )
    hours_requested = forms.IntegerField(
        min_value=1,
        label='Hours Needed',
        help_text='How many hours do you expect this service to take?',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Enter full address where service is needed'