from django.test import TestCase, Client, LiveServerTestCase
from .views import vehicle_data
from django.contrib.auth import get_user_model
from .models import Car
from django.contrib.auth import authenticate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

# Contains a dump of database data
# MUST BE UPDATED MANUALLY WHEN DATABASE CHANGES
fixtures = ['dumpdata.json']

class visualise_vehicle_live_tests(LiveServerTestCase):
    port = 8081
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        
    def log_in(self):
        time.sleep(1)
        selenium = self.selenium
        login = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submitBtn')
        
        login.send_keys('testuser')
        password.send_keys('12345')
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

    def setUp(self):
        self.selenium = webdriver.Firefox()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345', staffID=99, first_name='Test', last_name='Test', branchID=1, dob='1111-11-11')

    def tearDown(self):
        self.selenium.quit()
        
    def test_navigation(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/")
        vehicle_nav = selenium.find_element_by_id('vehicle-nav')
        vehicle_nav.click()
        vehicle_but = selenium.find_element_by_link_text('Vehicle Data Visualisation')
        vehicle_but.click()
        
        self.log_in()
        
        assert 'Vehicle Data Visualisation' in selenium.find_element_by_tag_name('h3').text
        assert '<title>Vehicle Visualisation | CRDMP</title>' in selenium.page_source
        assert 'Vehicle Data Visualisation</h3>' in selenium.page_source
        assert 'visualise.css' in selenium.page_source
        assert '<script src="/static/js/visualise.js"></script>' in selenium.page_source
        
    def test_canvas(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/staff/visualisevehicles")
        self.log_in()
        
        assert selenium.find_element_by_id('bodyTypeChart')
        
    def test_base_template(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/staff/visualisevehicles")
        self.log_in()
        
        assert 'Copyright Aquarius Inc' in selenium.page_source
        assert 'materialize.css' in selenium.page_source
        assert selenium.find_element_by_class_name('brand-logo')
        assert selenium.find_element_by_class_name('nav-wrapper')
        assert selenium.find_element_by_class_name('page-footer')
        assert 'materialize.min.js' in selenium.page_source
        
        
class staff_account_creation_live_tests(LiveServerTestCase):
    port = 8081
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        
    def log_in(self):
        time.sleep(1)
        selenium = self.selenium
        login = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submitBtn')
        
        login.send_keys('testadmin')
        password.send_keys('12345')
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

    def setUp(self):
        self.selenium = webdriver.Firefox()
        User = get_user_model()
        self.user1 = User.objects.create_user(username='testuser', password='123456', staffID=99, is_management=0, first_name='Test', last_name='Test', branchID=1, dob='1111-11-11')
        self.user2 = User.objects.create_user(username='testadmin', password='12345', staffID=98, is_management=1, first_name='Test', last_name='Test', branchID=2, dob='1111-11-11')

    def tearDown(self):
        self.selenium.quit()
        
    def test_navigation(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/login")
        self.log_in()
        selenium.get("http://localhost:8081/")
        vehicle_nav = selenium.find_element_by_id('account-nav')
        vehicle_nav.click()
        vehicle_but = selenium.find_element_by_link_text('Create User')
        vehicle_but.click()
        
        assert 'Sign up' in selenium.find_element_by_tag_name('h3').text
        assert '<title>Sign Up | CRDMP</title>' in selenium.page_source
        assert '<h3>Sign up</h3>' in selenium.page_source
        
    def test_manager_restrictions(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/signup")
        self.log_in()
        
        selenium.find_element_by_id('id_dob').send_keys('1900-10-10')
        selenium.find_element_by_id('id_username').send_keys('newaccount')
        selenium.find_element_by_id('id_staffID').send_keys('998')
        selenium.find_element_by_id('id_branchID').send_keys('-5')
        selenium.find_element_by_id('id_first_name').send_keys('test')
        selenium.find_element_by_id('id_last_name').send_keys('name')
        selenium.find_element_by_id('id_password1').send_keys('word1234')
        selenium.find_element_by_id('id_password2').send_keys('word1234')
        selenium.find_element_by_id('submitBtn').click()
        
        time.sleep(1)

        assert 'Signup was successful!' not in selenium.page_source
    
    def test_create_account(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/signup")
        self.log_in()
        
        selenium.find_element_by_id('id_username').send_keys('newaccount')
        selenium.find_element_by_id('id_dob').send_keys('1900-10-10')
        selenium.find_element_by_id('id_staffID').send_keys('997')
        selenium.find_element_by_id('id_branchID').send_keys('5')
        selenium.find_element_by_id('id_first_name').send_keys('test')
        selenium.find_element_by_id('id_last_name').send_keys('name')
        selenium.find_element_by_id('id_password1').send_keys('word1234')
        selenium.find_element_by_id('id_password2').send_keys('word1234')
        selenium.find_element_by_id('submitBtn').click()
        
        time.sleep(2)
        assert 'Signup was successful!' in selenium.page_source
        
    def test_new_account_login(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/signup")
        self.log_in()
        
        selenium.find_element_by_id('id_username').send_keys('newaccount')
        selenium.find_element_by_id('id_dob').send_keys('1900-10-10')
        selenium.find_element_by_id('id_staffID').send_keys('998')
        selenium.find_element_by_id('id_branchID').send_keys('5')
        selenium.find_element_by_id('id_first_name').send_keys('test')
        selenium.find_element_by_id('id_last_name').send_keys('name')
        selenium.find_element_by_id('id_password1').send_keys('word1234')
        selenium.find_element_by_id('id_password2').send_keys('word1234')
        selenium.find_element_by_id('submitBtn').click()
        
        time.sleep(2)
        selenium.find_element_by_partial_link_text('Logout').click()
        time.sleep(2)
        selenium.get("http://localhost:8081/accounts/login")
        self.log_in()
   
        assert '<h3>Available Vehicles</h3>' in selenium.page_source
   
    def test_base_template(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/signup")
        self.log_in()
        
        assert 'Copyright Aquarius Inc' in selenium.page_source
        assert 'materialize.css' in selenium.page_source
        assert selenium.find_element_by_class_name('brand-logo')
        assert selenium.find_element_by_class_name('nav-wrapper')
        assert selenium.find_element_by_class_name('page-footer')
        assert 'materialize.min.js' in selenium.page_source
   
class staff_access_account_live_tests(LiveServerTestCase):
    port = 8081
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        
    def log_in(self):
        time.sleep(1)
        selenium = self.selenium
        login = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submitBtn')
        
        login.send_keys('testuser')
        password.send_keys('12345')
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

    def setUp(self):
        self.selenium = webdriver.Firefox()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345', staffID=99, is_management=0, first_name='Test', last_name='Test', branchID=1, dob='1111-11-11')

    def tearDown(self):
        self.selenium.quit()
    
    def test_invalid_login(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/login")
        time.sleep(1)
        selenium = self.selenium
        login = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submitBtn')
        
        login.send_keys('d.@as03213')
        password.send_keys('./asd2132389232')
        submit.send_keys(Keys.RETURN)
        time.sleep(3)
        
        assert "Please enter a correct username and password" in selenium.page_source
    
    def test_valid_login(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/login")
        self.log_in()
        
        assert "<h3>Available Vehicles</h3>" in selenium.page_source
        assert "Signed in as testuser" in selenium.page_source
    
    def test_session_management(self):
        selenium = self.selenium
        selenium.get("http://localhost:8081/accounts/login")
        self.log_in()
        
        assert "<h3>Available Vehicles</h3>" in selenium.page_source
        assert "Signed in as testuser" in selenium.page_source
        
        selenium.find_element_by_id('view-rentals').click()
        time.sleep(3)
        
        assert "<h3>Rental Data</h3>" in selenium.page_source
        assert "<title>Rentals | CRDMP</title>" in selenium.page_source
        assert "Signed in as testuser" in selenium.page_source
        
        selenium.find_element_by_partial_link_text('View Stock').click()
        time.sleep(3)
        
        assert "<h3>View Stock</h3>" in selenium.page_source
        assert selenium.find_element_by_link_text("Signed in as testuser")
        
        selenium.find_element_by_partial_link_text('Vehicle Data Visualisation').click()
        time.sleep(3)
        
        assert "Vehicle Data Visualisation</h3>" in selenium.page_source
        assert "Signed in as testuser" in selenium.page_source
        
   
   
   
   
   
   
   
   