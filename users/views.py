from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from services.models import RequestedService, Service


def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type', 'customer')
        if user_type == 'customer':
            form = CustomerSignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/')
        else:  # company
            form = CompanySignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/')
    
    return render(request, 'users/register.html')

def customer_register(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomerSignUpForm()
    return render(request, 'users/register_customer.html', {'form': form})

def company_register(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CompanySignUpForm()
    return render(request, 'users/register_company.html', {'form': form})

def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def profile_view(request):
    user = request.user
    if user.is_customer:
        try:
            customer = user.customer_profile
            services = RequestedService.objects.filter(customer=customer)
            return render(request, 'users/profile.html', {
                'user': user,
                'customer': customer,
                'services': services
            })
        except Customer.DoesNotExist:
            return render(request, 'users/profile.html', {'error': 'Customer profile not found'})
    elif user.is_company:
        try:
            company = user.company_profile
            services = company.services.all()  # from Service model
            return render(request, 'users/profile.html', {
                'user': user,
                'company': company,
                'services': services
            })
        except Company.DoesNotExist:
            return render(request, 'users/profile.html', {'error': 'Company profile not found'})
    else:
        return redirect('/')

def company_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_company:
        return redirect('service-list')
    
    company = user.company_profile
    services = Service.objects.filter(company=company)
    return render(request, 'users/company_profile.html', {
        'company': company,
        'services': services
    })
