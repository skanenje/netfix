from django.shortcuts import render
from users.models import Customer
from services.models import RequestedService

from users.models import User, Company
from services.models import Service


def home(request):
    return render(request, 'main/home.html', {'user': request.user})


def customer_profile(request, name):
    try:
        user = User.objects.get(username=name)
        customer = Customer.objects.get(user=user)
    except (User.DoesNotExist, Customer.DoesNotExist):
        # Handle the case where the user or customer doesn't exist
        return render(request, 'users/profile.html', {'error': 'Customer not found'})

    services = RequestedService.objects.filter(customer=customer)
    return render(request, 'users/profile.html', {
        'user': user,
        'customer': customer,
        'services': services
    })


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})
