import unittest
import logging
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time
import sys
sys.path.append('../../')

from app import app

class TestPages(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_all_pages(self):
        """
        Tests that each page exists (or doesn't yet exist for iteration 2)
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/assessment')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/sign_up')
        self.assertEqual(response.status_code, 200)

        # Page does not yet exist
        response = self.app.get('/profile')
        self.assertNotEqual(response.status_code, 200)

        # Page does not yet exist
        response = self.app.get('/logout')
        self.assertNotEqual(response.status_code, 200)

    def tearDown(self):
        return


class TestUserInterfaceClass(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')

        self.homepage = 'http://127.0.0.1:5000'

        try:
            dir = os.path.dirname(os.path.abspath(__file__))
            self.driver = webdriver.Chrome(executable_path=dir + '/chromedriver', options=options)
            self.driver.implicitly_wait(15)
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
        """
        checks that a 404 error was not encountered
        """
        self.assertNotEqual('404 Not Found', self.driver.title)

    def __check_navigation_bar(self, page):
        """
        checks each of the nav bar items and ensure they are clickable,
        after one check, this method goes back to the page being tested
        before trying the next method
        """
        self.driver.get(page)
        home = self.driver.find_element_by_link_text("Home")
        home.click()
        self.__check_page()
        time.sleep(5)

        self.driver.get(page)
        profile = self.driver.find_element_by_link_text("Profile")
        profile.click()
        self.__check_page()
        time.sleep(5)

        self.driver.get(page)
        start_assessment = self.driver.find_element_by_link_text("Start Assessment")
        start_assessment.click()
        self.__check_page()
        time.sleep(5)

        self.driver.get(page)
        sign_up = self.driver.find_element_by_link_text("Sign Up")
        sign_up.click()
        self.__check_page()
        time.sleep(5)

    def test_homepage_nav_bar(self):
        self.__check_navigation_bar(self.homepage)

    def test_assessment_page_nav_bar(self):
        self.__check_navigation_bar(self.homepage+'/assessment')

    def test_sign_up_page_nav_bar(self):
        self.__check_navigation_bar(self.homepage+'/sign_up')

    def test_assessment_page(self):
        """
        THIS ONLY CONFIRMS THAT FEATURES ARE CLICKABLE,
        NOT THAT THE ALGORITHM/OUTPUT IS CORRECT
        """
        self.driver.get(self.homepage+'/assessment')
        self.driver.find_element_by_id("symptom-search").click()
        self.driver.find_element_by_id("symptom-search").clear()
        self.driver.find_element_by_id("symptom-search").send_keys("sy")
        self.driver.find_element_by_id("Symptom_2").click()

        self.driver.find_element_by_css_selector("svg.graph-svg").click()
        self.driver.find_element_by_id("symptom-input").click()
        self.driver.find_element_by_id("symptom-input").clear()
        self.driver.find_element_by_id("symptom-input").send_keys("yes")
        self.driver.find_element_by_id("symptom-input").send_keys(Keys.ENTER)

        self.driver.find_element_by_id("symptom-input").click()
        self.driver.find_element_by_id("symptom-input").clear()
        self.driver.find_element_by_id("symptom-input").send_keys("no")
        self.driver.find_element_by_id("symptom-input").send_keys(Keys.ENTER)

    def tearDown(self):
        # close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
