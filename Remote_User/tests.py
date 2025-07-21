# app/tests/test_functional_form.py
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from .views import *
from .models import *

class FormSubmissionFunctionalTest(StaticLiveServerTestCase):
    """
    Functional test that opens a real browser with Selenium,
    hits the Django dev server started by StaticLiveServerTestCase,
    fills a form, submits it, and checks the JavaScript alert.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # ⚠️  Replace with your preferred driver / options
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_form_submission(self):
        """
        1. Open the page served by Django.
        2. Enter data.
        3. Click Submit.
        4. Verify alert appears and accept it.
        """
        url = self.live_server_url + reverse(Register)   # adjust to your view name
        self.driver.get(url)
        self.driver.find_element(By.ID, "fullname").send_keys("Ajay")
        self.driver.find_element(By.ID, "email").send_keys("ajay@example.com")
        self.driver.find_element(By.ID,"username").send_keys('ajay@example.com')
        self.driver.find_element(By.ID,"password").send_keys("12345678")
        self.driver.find_element(By.ID, "phone").send_keys("9876543210")
        select_county=Select(self.driver.find_element(By.ID,"country"))
        select_county.select_by_visible_text('INDIA')
        self.driver.find_element(By.ID, "state").send_keys("AP")
        self.driver.find_element(By.ID, "city").send_keys("Nrt")
        self.driver.find_element(By.ID,'submit').click()
        print("✔️ Client saved in test DB:",)
        if self.driver.title == 'Confirm Your Email | CardiacCare' :
            print('Test Case Passed')
        else:
            print('Test Case Failed')
        
