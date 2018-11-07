import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestUserInterfaceClass(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.options = webdriver.ChromeOptions()
        self.options.add('--disable-gpu')
        self.options.add('--headless')

        try:
            logging.info('Connecting to ')
            self.driver.get('http://127.0.0.1:5000')
        except Exception as issue:
            logging.warning('Could not connect to UI. Did you start the app? \n Caught Exception: %s', issue)
            exit(1)

    def test_login_page(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # close the browser window
        cls.driver.quit()
