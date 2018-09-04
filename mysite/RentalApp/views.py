from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def customers_table(request):
    return render(request, 'customers_table.html')


def rental_table(request):
    return render(request, 'rental_table.html')


def customer_data(request):
    return render(request, 'visualise_customer_data.html')


def rental_data(request):
    return render(request, 'visualise_rental_data.html')


def vehicle_data(request):
    return render(request, 'visualise_vehicle_data.html')