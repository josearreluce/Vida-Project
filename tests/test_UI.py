import unittest
import logging
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestUserInterfaceClass(unittest.TestCase):

    def setUp(self):

        try:
            dir = os.path.dirname(os.path.abspath(__file__))
            self.driver = webdriver.Chrome(executable_path=dir + '/chromedriver')
        except Exception as issue:
            logging.warning('Could not start Chrome Webdriver. Is chromedriver.exe in the test directory?\n Caught Exception: %s', issue)

        self.options = webdriver.ChromeOptions()
        #cls.options.add_argument('--disable-gpu')
        #cls.options.add_argument('--headless')
        self.homepage = 'http://127.0.0.1:5000'
        try:
            logging.info('Connecting to ')
            self.driver.get(self.homepage)
        except Exception as issue:
            logging.warning('Could not connect to UI. Did you start the app?\n Caught Exception: %s', issue)
            exit(1)

    def output_errors(self):
        for error_location in self.error_logs:
            print('%s error encountered: %s', error_location, self.error_logs[error_location])

    def test_login_page(self):
        pass

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True


    """
    Homepage Test
    
    - Check that "Username" string exists
    - Check that "Password" string exists
    - Check that Two Inputs exists
    - Check that login button exists
    """


    """
    Assessment Test
    
    - Test Assessment Navigation Bar
    - Check that there is "Start Assessment" button
    - Try to input a symptom
    - Check response
    -  
    """
    def test_assessment_page(self):
        self.driver.get(self.homepage)
        pass

    def test_navigation_bar(self):
        self.driver.get(self.homepage)
        self.driver.find_element_by_link_text("Home").click()
        self.driver.find_element_by_link_text("About").click()
        self.driver.find_element_by_link_text("Profile").click()

    def tearDown(self):
        # close the browser window
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
