from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from services.models import RequestedService, Service

def register(request):
    customer_form = CustomerSignUpForm()
    company_form = CompanySignUpForm()
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        try:
            if user_type == 'customer':
                form = CustomerSignUpForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect': '/'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
            elif user_type == 'company':
                form = CompanySignUpForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect': '/'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except IntegrityError as e:
            return JsonResponse({'success': False, 'errors': {'__all__': ['Registration failed. Please try again.']}})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'__all__': ['An unexpected error occurred.']}})
    return render(request, 'users/register.html', {
        'customer_form': customer_form,
        'company_form': company_form
    })

def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    try:
        if user.is_customer:
            try:
                customer = user.customer_profile
                services = RequestedService.objects.filter(customer=customer).order_by('-requested_date')
                user_age = (timezone.now().date() - customer.date_of_birth).days // 365
                return render(request, 'users/profile.html', {
                    'user': user,
                    'customer': customer,
                    'services': services,
                    'user_age': user_age
                })
            except Customer.DoesNotExist:
                messages.error(request, 'Customer profile not found.')
                return render(request, 'users/profile.html', {'error': 'Customer profile not found'})
        elif user.is_company:
            try:
                company = user.company_profile
                services = company.services.all().order_by('-created_date')
                return render(request, 'users/profile.html', {
                    'user': user,
                    'company': company,
                    'services': services
                })
            except Company.DoesNotExist:
                messages.error(request, 'Company profile not found.')
                return render(request, 'users/profile.html', {'error': 'Company profile not found'})
        else:
            messages.error(request, 'Invalid user type.')
            return redirect('main:home')
    except Exception as e:
        messages.error(request, 'Unable to load profile. Please try again.')
        return redirect('main:home')

def company_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id, is_company=True)
        company = user.company_profile
        services = company.services.all().order_by('-created_date')
        return render(request, 'users/profile.html', {
            'user': user,
            'company': company,
            'services': services
        })
    except (User.DoesNotExist, Company.DoesNotExist):
        return render(request, 'users/profile.html', {'error': 'Company not found'})