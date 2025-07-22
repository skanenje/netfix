from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

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
                messages.success(request, 'Registration successful!')
                return redirect('/')
            else:
                return render(request, 'users/register.html', {
                    'customer_form': form,
                    'company_form': CompanySignUpForm(),
                    'user_type': user_type
                })
        else:
            form = CompanySignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('/')
            else:
                return render(request, 'users/register.html', {
                    'customer_form': CustomerSignUpForm(),
                    'company_form': form,
                    'user_type': user_type
                })
    
    return render(request, 'users/register.html', {
        'customer_form': CustomerSignUpForm(),
        'company_form': CompanySignUpForm()
    })


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    if user.is_customer:
        customer = user.customer_profile
        services = RequestedService.objects.filter(customer=customer)
        return render(request, 'users/profile.html', {
            'user': user,
            'customer': customer,
            'services': services
        })
    elif user.is_company:
        company = user.company_profile
        services = company.service_set.all()
        return render(request, 'users/profile.html', {
            'user': user,
            'company': company,
            'services': services
        })
    return redirect('/')


def company_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_company:
        return redirect('/')
    
    company = user.company_profile
    services = Service.objects.filter(company=company)
    return render(request, 'users/company_profile.html', {
        'company': company,
        'services': services
    })
