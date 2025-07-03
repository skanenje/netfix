from django import forms
from users.models import Company, Customer
from .models import Service


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, company=None, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)

        # Set choices based on the company's field
        if company:
            if company.field == 'All in One':
                from .choices import SERVICE_FIELD_CHOICES
                self.fields['field'].choices = SERVICE_FIELD_CHOICES
            else:
                self.fields['field'].choices = [(company.field, company.field)]
                self.fields['field'].initial = company.field
                self.fields['field'].widget = forms.HiddenInput()  # Auto-select for non All-in-One companies

        # Add placeholders
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