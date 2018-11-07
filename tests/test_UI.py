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
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')

        self.homepage = 'http://127.0.0.1:5000'

        try:
            dir = os.path.dirname(os.path.abspath(__file__))
            self.driver = webdriver.Chrome(executable_path=dir + '/chromedriver', options=options)
        except Exception as issue:
            logging.warning('Could not start Chrome Webdriver. Is chromedriver.exe in the test directory?\n Caught Exception: %s', issue)
            exit(1)

        try:
            logging.info('Connecting to ')
            self.driver.get(self.homepage)
        except Exception as issue:
            logging.warning('Could not connect to UI. Did you start the app?\n Caught Exception: %s', issue)
            exit(1)

    def __check_page(self):
        self.assertNotEqual('404 Not Found', self.driver.title)
        self.driver.execute_script("window.history.go(-1)")

    def __check_navigation_bar(self):
        home = self.driver.find_element_by_link_text("Home")
        about = self.driver.find_element_by_link_text("About")
        profile = self.driver.find_element_by_link_text("Profile")
        start_assessment = self.driver.find_element_by_link_text("Start Assessment")

        home.click()
        self.__check_page()

        about.click()
        self.__check_page()

        profile.click()
        self.__check_page()

        start_assessment.click()
        self.__check_page()

    """
    Homepage Test
    
    - Check that "Username" string exists
    - Check that "Password" string exists
    - Check that Two Inputs exists
    - Check that login button exists
    """
    def test_homepage_nav_bar(self):
        # Navigate to assessment page
        self.driver.get(self.homepage)
        self.__check_navigation_bar()

    def test_login(self):
        pass

    """
    Assessment Test
    
    - Test Assessment Navigation Bar
    - Check that there is "Start Assessment" button
    - Try to input a symptom
    - Check response
    -  
    """
    def test_assessment_page_nav_bar(self):
        # Navigate to assessment page
        assessment_page = self.homepage + "/Start%20Assessment"
        self.driver.get(assessment_page)
        self.__check_navigation_bar()

    def test_assessment(self):
        pass
        #self.driver.get(self.homepage)

    def tearDown(self):
        # close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
