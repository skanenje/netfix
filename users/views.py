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
            error_message = 'Registration failed. Please try again.'
            if 'UNIQUE constraint failed' in str(e):
                if 'email' in str(e):
                    error_message = 'An account with this email already exists.'
                elif 'username' in str(e):
                    error_message = 'This username is already taken.'
            return JsonResponse({'success': False, 'errors': {'__all__': [error_message]}})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'__all__': ['An unexpected error occurred. Please try again.']}})
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
            
            try:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('main:home')
                    else:
                        form.add_error(None, 'Your account has been deactivated. Please contact support.')
                else:
                    # Check if user exists to provide more specific error
                    from .models import User
                    try:
                        User.objects.get(email=email)
                        form.add_error('password', 'Incorrect password. Please try again.')
                    except User.DoesNotExist:
                        form.add_error('email', 'No account found with this email address.')
            except Exception as e:
                form.add_error(None, 'Login failed. Please try again.')
        else:
            # Add field-specific errors if form validation failed
            if not form.cleaned_data.get('email'):
                form.add_error('email', 'Email is required.')
            if not form.cleaned_data.get('password'):
                form.add_error('password', 'Password is required.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    
    # Handle customer profile
    if user.is_customer:
        try:
            customer = user.customer_profile
            services = RequestedService.objects.filter(customer=customer).order_by('-date_requested')
            user_age = (timezone.now().date() - customer.date_of_birth).days // 365
            return render(request, 'users/profile.html', {
                'user': user,
                'customer': customer,
                'services': services,
                'user_age': user_age
            })
        except Customer.DoesNotExist:
            # Create a basic profile page for users without customer profile
            return render(request, 'users/profile.html', {
                'user': user,
                'error': 'Customer profile incomplete. Please contact support.',
                'services': []
            })
    
    # Handle company profile
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
            # Create a basic profile page for users without company profile
            return render(request, 'users/profile.html', {
                'user': user,
                'error': 'Company profile incomplete. Please contact support.',
                'services': []
            })
    
    # Handle users without proper type flags
    else:
        return render(request, 'users/profile.html', {
            'user': user,
            'error': 'Profile type not set. Please contact support.',
            'services': []
        })

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