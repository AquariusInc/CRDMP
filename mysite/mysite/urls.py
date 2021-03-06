"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import RentalApp.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/', views.home, name='home'),
    path('staff/customers', views.customers_table, name="customers_table"),
    path('staff/rentals', views.rental_table, name="rentals_table"),
    path('staff/visualisecustomers', views.customer_data),
    path('staff/customerhistory', views.customer_history),
    path('staff/visualiserentals', views.rental_data),
    path('staff/viewstock', views.view_stock),
    path('staff/visualisevehicles', views.vehicle_data),
    path('staff/readcentral', views.read_central_db),
    path('', views.vehicles_table),
    path('vehiclerecommend', views.vehicle_recommend),
    path('staff/readstore', views.read_store_data),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/successful', views.signup_success, name='successful signup'),
    path('accounts/', include('django.contrib.auth.urls'), name='login')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
