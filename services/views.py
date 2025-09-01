from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count
from django.contrib import messages
from django.db import IntegrityError
from users.models import Company, Customer
from .models import Service, RequestedService
from .forms import ServiceForm, RequestServiceForm

def service_list(request):
    try:
        services = Service.objects.all().order_by('-created_date')
        return render(request, 'services/list.html', {'services': services})
    except Exception as e:
        messages.error(request, 'Unable to load services. Please try again later.')
        return render(request, 'services/list.html', {'services': [], 'error': str(e)})

def service_detail(request, pk):
    try:
        service = get_object_or_404(Service, pk=pk)
        return render(request, 'services/single_service.html', {'service': service})
    except Exception as e:
        messages.error(request, 'Service not found or unable to load.')
        return redirect('services:services_list')

@login_required
def create_service(request):
    if not request.user.is_company:
        messages.error(request, "Only companies can create services.")
        return redirect('services:services_list')
    
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        messages.error(request, "Company profile not found.")
        return redirect('services:services_list')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, company=company)
        if form.is_valid():
            try:
                service = form.save(commit=False)
                service.company = company
                service.save()
                messages.success(request, f'Service "{service.name}" created successfully!')
                return redirect('services:services_list')
            except (IntegrityError, ValueError) as e:
                messages.error(request, f'Error creating service: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm(company=company)
    return render(request, 'services/create.html', {'form': form})

def service_field(request, field):
    try:
        field = field.replace('-', ' ').title()
        services = Service.objects.filter(field=field).order_by('-created_date')
        return render(request, 'services/field.html', {'services': services, 'field': field})
    except Exception as e:
        messages.error(request, 'Unable to load services for this category.')
        return redirect('services:services_list')

@login_required
def request_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if not request.user.is_customer:
        messages.error(request, "Only customers can request services.")
        return redirect('services:service_detail', pk=pk)
    
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect('services:service_detail', pk=pk)
    
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            try:
                service_request = form.save(commit=False)
                service_request.customer = customer
                service_request.service = service
                service_request.save()
                messages.success(request, f'Service "{service.name}" requested successfully!')
                return redirect('services:service_detail', pk=pk)
            except Exception as e:
                messages.error(request, f'Error requesting service: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RequestServiceForm()
    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service
    })

def most_requested(request):
    try:
        services = Service.objects.annotate(
            request_count=Count('requestedservice')
        ).order_by('-request_count')
        return render(request, 'services/list.html', {'services': services, 'page_title': 'Most Requested Services'})
    except Exception as e:
        messages.error(request, 'Unable to load most requested services.')
        return redirect('services:services_list')