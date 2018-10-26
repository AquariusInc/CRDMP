from django.test import TestCase, Client, LiveServerTestCase
from .views import vehicle_data
from django.contrib.auth import get_user_model
from .models import Car
from django.contrib.auth import authenticate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Contains a dump of database data
# MUST BE UPDATED MANUALLY WHEN DATABASE CHANGES
fixtures = ['dumpdata.json']

# class visualise_vehicle_tests(TestCase):
    # data_names = ['bodyTypes', 'make', 'model', 'year', 'price', 'seating', 'driveTrain']
    
    # def setUp(self):
        # User = get_user_model()
        # self.user = User.objects.create_user(username='testuser', password='12345', staffID=99, first_name='Test', last_name='Test', branchID=1, dob='1111-11-11')
 
    # def test_page_works(self):
        # c = Client()
        # c.login(username='testuser', password='12345')
        # response = c.get('/visualisevehicles')
        # self.assertEquals(response.status_code, 200)
        
    # def test_correct_template(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertEquals(response.status_code, 200)
        # self.assertTrue(all(x in response.context['js_data'] for x in self.data_names))
        
    # def test_correct_heading(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertContains(response, '<h3 class="card-panel" align="center">Vehicle Data Visualisation</h3>')
        
    # def test_contains_chartJS_scripts(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertContains(response, 'Chart.min.js')
        
    # def test_contains_custom_javascript(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertContains(response, 'visualise.js')
        
    # def test_contains_correct_tab_count(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertContains(response, 'class="tablinks"', count=len(self.data_names))   

    # def test_contains_correct_chart_container_count(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertContains(response, 'class="tabcontent"', count=len(self.data_names))  
        
    # def test_HTML_base_footer(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertContains(response, r'class="page-footer"' ) 
        
    # def test_HTML_base_header(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertContains(response, r'class="nav-wrapper"' )

    # def test_HTML_removed_template_names(self):
        # c = Client()
        # c.login(username='admin', password='word1234')
        # response = c.get('/visualisevehicles')
        # self.assertNotContains(response, r"{% extends 'base.html' %}" )    
        # self.assertNotContains(response, r"{% load static %}" )
        # self.assertNotContains(response, r"{% block content %}" )
        

class visualise_vehicle_live_tests(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345', staffID=99, first_name='Test', last_name='Test', branchID=1, dob='1111-11-11')
        
    def tearDown(self):
        self.selenium.quit()
        
    def test_auth(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/visualisevehicles')
        login = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submitBtn')
        
        login.send_keys('testuser')
        password.send_keys('12345')
        submit.send_keys(Keys.RETURN)
        
        assert 'Vehicle Data Visualisation' in selenium.page_source