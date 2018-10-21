from django.test import TestCase, Client
from django.test.client import RequestFactory
from .views import vehicle_data
from django.contrib.auth import get_user_model
from .models import Car
from django.contrib.auth import authenticate

class visualise_vehicle_data_tests(TestCase):
    data_names = ['bodyTypes', 'make', 'model', 'year', 'price', 'seating', 'driveTrain']

    # Fixtures
    # Contain a dump of database data
    # Should be updated manually
    fixtures = ['dumpdata.json']
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        User = get_user_model()
        user = User.objects.create(username='testuser', password='12345')
        #Car.objects.create(id=1, make='BMW', model='M3', series='bleh', year=1945, priceNew=30000, engineSize=200, fuelSystem='petrol', tankCapacity=200.0, power=150.0, seatingCapacity=4, standardTransmission='6AMS', bodyType='4 SEDAN', drive='RWD', wheelBase=20.0)
        #Car.objects.create(id=2, make='Mazda', model='E-type', series='yuck', year=1995, priceNew=20000, engineSize=150, fuelSystem='petrol', tankCapacity=200.0, power=150.0, seatingCapacity=7, standardTransmission='3GMS', bodyType='2 Coupe', drive='FWD', wheelBase=30.0)
 
    def test_page_works(self):
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get('/visualisevehicles')
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(all(x in response.context['js_data'] for x in self.data_names))
        
    def test_correct_heading(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertContains(response, '<h3>Vehicle Data Visualisation</h3>')
        
    def test_contains_chartJS_scripts(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertContains(response, 'Chart.min.js')
        
    def test_contains_custom_javascript(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertContains(response, 'visualise_vehicle.js')
        
    def test_contains_correct_tab_count(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertContains(response, 'class="tablinks"', count=len(self.data_names))   

    def test_contains_correct_chart_container_count(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertContains(response, 'class="tabcontent"', count=len(self.data_names))  
        
    def test_HTML_base_footer(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertContains(response, r'class="page-footer"' ) 
        
    def test_HTML_base_header(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertContains(response, r'class="nav-wrapper"' )

    def test_HTML_removed_template_names(self):
        c = Client()
        response = c.get('/visualisevehicles')
        self.assertNotContains(response, r"{% extends 'base.html' %}" )    
        self.assertNotContains(response, r"{% load static %}" )
        self.assertNotContains(response, r"{% block content %}" )
        
    def test_request(self):
        request = self.factory.get('/visualisevehicles')
        response = vehicle_data(request)
        self.assertEquals(response.status_code, 200)
        
    def test_database_import(self):
        c = Client()
        response = c.get('/visualisevehicles')
        print(response.context)
        
        
        

       
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   