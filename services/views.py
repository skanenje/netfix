from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count
from users.models import Company, Customer
from .models import Service, RequestedService
from .forms import ServiceForm, RequestServiceForm

def service_list(request):
    services = Service.objects.all().order_by('-created_date')
    return render(request, 'services/list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/single_service.html', {'service': service})

@login_required
def create_service(request):
    if not request.user.is_company:
        return HttpResponseForbidden("Only companies can create services.")
    company = request.user.company_profile
    if request.method == 'POST':
        form = ServiceForm(request.POST, company=company)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = company
            service.save()
            return redirect('services_list')
    else:
        form = ServiceForm(company=company)
    return render(request, 'services/create.html', {'form': form})

def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field).order_by('-created_date')
    return render(request, 'services/field.html', {'services': services, 'field': field})

@login_required
def request_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if not request.user.is_customer:
        return HttpResponseForbidden("Only customers can request services.")
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            request_service = form.save(commit=False)
            request_service.customer = request.user.customer_profile
            request_service.service = service
            request_service.save()
            return redirect('service_detail', pk=pk)
    else:
        form = RequestServiceForm()
    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service
    })

def most_requested(request):
    services = Service.objects.annotate(
        request_count=Count('requestedservice')
    ).order_by('-request_count')
    return render(request, 'services/list.html', {'services': services})