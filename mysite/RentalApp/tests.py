from django.test import TestCase, Client, LiveServerTestCase
from .views import vehicle_data
from django.contrib.auth import get_user_model
from .models import Car
from django.contrib.auth import authenticate
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import time

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


# class visualise_vehicle_live_tests(LiveServerTestCase):
#     def setUp(self):
#         self.selenium = webdriver.Firefox()
#         User = get_user_model()
#         self.user = User.objects.create_user(username='testuser', password='12345', staffID=99, first_name='Test', last_name='Test', branchID=1, dob='1111-11-11')
#
#     def tearDown(self):
#         self.selenium.quit()
#
#     def test_auth(self):
#         selenium = self.selenium
#         selenium.get('http://127.0.0.1:8000/visualisevehicles')
#         login = selenium.find_element_by_id('id_username')
#         password = selenium.find_element_by_id('id_password')
#         submit = selenium.find_element_by_id('submitBtn')
#
#         login.send_keys('testuser')
#         password.send_keys('12345')
#         submit.send_keys(Keys.RETURN)
#
#         assert 'Vehicle Data Visualisation' in selenium.page_source


# class CustomerTableTests(LiveServerTestCase):
#     def setUp(self):
#         self.selenium = webdriver.Firefox()
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/accounts/login/')
#         login = selenium.find_element_by_id('id_username')
#         password = selenium.find_element_by_id('id_password')
#         submit = selenium.find_element_by_id('submitBtn')
#
#         login.send_keys('admin')
#         password.send_keys('word1234')
#         submit.send_keys(Keys.RETURN)
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#
#     def tearDown(self):
#         self.selenium.quit()
#
#     def test_navigation_from_home(self):
#         selenium = self.selenium
#         selenium.get('http://127.0.0.1:8000/')
#         customer_menu = selenium.find_element_by_id('customer-nav')
#         customer_menu.click()
#         customer_table = selenium.find_element_by_id('view-customers')
#         customer_table.click()
#
#         assert 'Customer Data' in selenium.page_source
#
#     def test_dropdown_appears(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#
#         assert 'select' in selenium.page_source
#
#     def test_search_by_id(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('11116')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(5)
#
#         assert 'Clinton' in selenium.page_source
#
#     def test_search_by_name(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[3]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('Clinton')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '11116' in selenium.page_source
#
#     def test_search_by_address(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[5]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('7943 Cunha Ct.')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '11116' in selenium.page_source
#
#     def test_search_by_phone(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[4]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('1 (11) 543 535-012')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '11055' in selenium.page_source
#
#     def test_search_by_occupation(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[6]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('Retiree')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '11119' in selenium.page_source
#
#     def test_search_by_gender(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[7]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('F')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '11219' in selenium.page_source
#
#     def test_number_of_order_history_buttons(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         count = selenium.find_elements_by_xpath("//a[@class='btn order-history-link']")
#
#         assert len(count) == 25
#
#     def test_pages_of_25(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/customers')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         count_page_1 = selenium.find_elements_by_xpath("//a[@class='btn order-history-link']")
#
#         selenium.find_element_by_id('next-button').click()
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         count_page_2 = selenium.find_elements_by_xpath("//a[@class='btn order-history-link']")
#
#         assert len(count_page_1) == 25 and len(count_page_2) == 25

#
# class RentalTableTests(LiveServerTestCase):
#     def setUp(self):
#         self.selenium = webdriver.Firefox()
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/accounts/login/')
#         login = selenium.find_element_by_id('id_username')
#         password = selenium.find_element_by_id('id_password')
#         submit = selenium.find_element_by_id('submitBtn')
#
#         login.send_keys('admin')
#         password.send_keys('word1234')
#         submit.send_keys(Keys.RETURN)
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#
#     def tearDown(self):
#         self.selenium.quit()
#
#     def test_navigation_from_home(self):
#         selenium = self.selenium
#         selenium.get('http://127.0.0.1:8000/')
#         customer_menu = selenium.find_element_by_id('rental-nav')
#         customer_menu.click()
#         customer_table = selenium.find_element_by_id('view-rentals')
#         customer_table.click()
#
#         assert 'Rental Data' in selenium.page_source
#
#     def test_dropdown_appears(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#
#         assert 'select' in selenium.page_source
#
#     def test_search_by_id(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[2]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('37')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '11013' in selenium.page_source
#
#     def test_search_by_car_id(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[3]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('15165')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '377' in selenium.page_source
#
#     def test_search_by_customer_id(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[4]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('11312')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(2)
#         assert '377' in selenium.page_source
#
#     def test_search_by_pickup_store_id(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[5]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('12')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(5)
#         assert '377' in selenium.page_source
#
#     def test_search_by_return_store_id(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[6]/span").click()
#         search_bar = selenium.find_element_by_id('search_box')
#         search_bar.send_keys('17')
#         search_bar.send_keys(Keys.RETURN)
#         time.sleep(5)
#         assert '377' in selenium.page_source
#
#     def test_pages_of_25(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         count_page_1 = selenium.find_elements_by_xpath("//a[@class='link-to-customer']")
#
#         selenium.find_element_by_id('next-button').click()
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#         count_page_2 = selenium.find_elements_by_xpath("//a[@class='link-to-customer']")
#
#         assert len(count_page_1) == 25 and len(count_page_2) == 25
#
#     def test_base_template(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/staff/rentals')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'table-id')))
#
#         assert 'page-footer' in selenium.page_source and 'nav-wrapper' in selenium.page_source
#
#
# class VehicleTableTestsLoggedOut(LiveServerTestCase):
#     def setUp(self):
#         self.selenium = webdriver.Firefox()
#
#     def tearDown(self):
#         self.selenium.quit()
#
#     def test_logged_out_access(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#
#         assert 'Available Vehicles' in selenium.page_source
#
#
# class VehicleTableTestsLoggedIn(LiveServerTestCase):
#     def setUp(self):
#         self.selenium = webdriver.Firefox()
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/accounts/login/')
#         login = selenium.find_element_by_id('id_username')
#         password = selenium.find_element_by_id('id_password')
#         submit = selenium.find_element_by_id('submitBtn')
#
#         login.send_keys('admin')
#         password.send_keys('word1234')
#         submit.send_keys(Keys.RETURN)
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#
#     def tearDown(self):
#         self.selenium.quit()
#
#     def test_homepage(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#
#         assert 'Available Vehicles' in selenium.page_source
#
#     def test_car_prices(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         try:
#             selenium.find_element_by_xpath("//div[contains(@class, 'car-price')]")
#         except NoSuchElementException:
#             raise
#         return True
#
#     def test_filter_modal(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         selenium.find_element_by_id('filter-button').click()
#         element = selenium.find_element_by_xpath("//div[@class='modal-content']")
#         time.sleep(3)
#         if element.is_displayed():
#             return True
#         else:
#             self.assertRaises(NoSuchElementException)
#
#     def test_store_dropdown(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         selenium.find_element_by_id('filter-button').click()
#         selenium.find_element_by_xpath('//*[@class="modal-content"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         first_item = selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[2]/span").text
#
#         assert first_item == "Alexandria"
#
#     def test_slider_exists(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         selenium.find_element_by_id('filter-button').click()
#         element = selenium.find_element_by_id('seat-number')
#         time.sleep(3)
#         assert element.is_displayed()
#
#     def test_checkboxes_exists(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         selenium.find_element_by_id('filter-button').click()
#         element = selenium.find_elements_by_class_name('transmission-checkbox')
#         time.sleep(3)
#         assert len(element) == 3
#
#     def test_make_dropdown(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         selenium.find_element_by_id('filter-button').click()
#         selenium.find_element_by_xpath('//*[@class="modal-content"]/div/form/div[5]/div[1]/div').click()
#         time.sleep(2)
#         first_item = selenium.find_element_by_xpath("//div[@id='make-div']/div/ul/li[2]/span").text
#
#         assert first_item == "LAND ROVER"
#
#     def test_model_dropdown(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         selenium.find_element_by_id('filter-button').click()
#         selenium.find_element_by_xpath('//*[@class="modal-content"]/div/form/div[5]/div[2]/div').click()
#         time.sleep(2)
#         first_item = selenium.find_element_by_xpath("//div[@id='model-div']/div/ul/li[2]/span").text
#         assert first_item == "DISCOVERY 3"
#
#     def test_filter_results(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         selenium.find_element_by_id('filter-button').click()
#         selenium.find_element_by_xpath('//*[@class="modal-content"]/div/form/div/div[1]/div').click()
#         time.sleep(2)
#         first_item = selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[17]/span").text
#         selenium.find_element_by_xpath('//*[@class="modal-content"]/div/form/div[5]/div[1]/div').click()
#         time.sleep(2)
#         selenium.find_element_by_xpath("//div[@id='make-div']/div/ul/li[2]/span").click()
#         selenium.find_element_by_id('submit-button').click()
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'clear-button')))
#
#         assert 'LAND ROVER DISCOVERY 3' in selenium.page_source
#
#     def test_cards_with_images(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         assert 'card-image' in selenium.page_source
#
#     def test_info_reveal(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         first_info_button = selenium.find_elements_by_class_name('info')[0]
#         first_info_button.click()
#         element = selenium.find_element_by_xpath('//*[@id="vehicle_list"]/div[1]/div[1]/div/div[3]/div[1]')
#         assert element.is_displayed()
#
#     def test_pages_of_24(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/')
#         delay = 10
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         count_page_1 = selenium.find_elements_by_xpath("//div[@class='car-image-div']")
#
#         selenium.find_element_by_id('next-button').click()
#         WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))
#         count_page_2 = selenium.find_elements_by_xpath("//div[@class='car-image-div']")
#
#         assert len(count_page_1) == 24 and len(count_page_2) == 24
#
#
class VehicleRecommendTestsLoggedOut(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()

    def tearDown(self):
        self.selenium.quit()

    def test_logged_out_access(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/vehiclerecommend')

        assert 'Vehicle Recommendation' in selenium.page_source


class VehicleRecommendTests(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        selenium = self.selenium
        selenium.get('http://localhost:8000/accounts/login/')
        login = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submitBtn')

        login.send_keys('admin')
        password.send_keys('word1234')
        submit.send_keys(Keys.RETURN)
        delay = 10
        WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'filter-button')))

    def tearDown(self):
        self.selenium.quit()

    def test_navigation_from_home(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        customer_menu = selenium.find_element_by_id('vehicle-nav')
        customer_menu.click()
        customer_table = selenium.find_element_by_id('vehicle-recommend')
        customer_table.click()

        assert 'Vehicle Recommendation' in selenium.page_source

    def test_store_dropdown(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/vehiclerecommend')
        delay = 10
        WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'recommend-submit')))
        selenium.find_element_by_xpath('//*[@id="background"]/div/form/div/div[1]/div').click()
        time.sleep(2)
        first_item = selenium.find_element_by_xpath("//div[@class='select-wrapper']/ul/li[2]/span").text

        assert first_item == "Alexandria"

    def test_slider_exists(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/vehiclerecommend')
        delay = 10
        WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'recommend-submit')))
        element = selenium.find_element_by_id('seat-number')
        time.sleep(3)
        assert element.is_displayed()

    def test_checkboxes_exists(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/vehiclerecommend')
        delay = 10
        WebDriverWait(selenium, delay).until(EC.presence_of_element_located((By.ID, 'recommend-submit')))
        element = selenium.find_elements_by_class_name('transmission-checkbox')
        time.sleep(3)
        assert len(element) == 3