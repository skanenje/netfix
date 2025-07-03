# services/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User
from .models import Service, RequestedService
from .forms import ServiceForm, RequestServiceForm  # Renamed CreateNewService → ServiceForm
def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/single_service.html', {'service': service})

@login_required
def create_service(request):
    user = request.user

    # Make sure the user is a company
    if not hasattr(user, 'company_profile'):
        return redirect('service-list')

    company = user.company_profile

    if request.method == 'POST':
        form = ServiceForm(request.POST, company=company)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = company
            service.save()
            return redirect('service-list')
    else:
        form = ServiceForm(company=company)

    return render(request, 'services/create.html', {'form': form})

def service_by_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})

@login_required
def request_service(request, id):
    service = get_object_or_404(Service, id=id)
    user = request.user

    # Make sure user is a customer
    if not hasattr(user, 'customer_profile'):
        return redirect('service-detail', id=id)

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            # Save the requested service (you'll need a RequestedService model)
            RequestedService.objects.create(
                customer=user.customer_profile,
                service=service,
                address=form.cleaned_data['address'],
                hours_requested=form.cleaned_data['hours_requested']
            )
            return redirect('service-detail', id=id)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service
    })