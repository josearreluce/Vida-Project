import os
import unittest

import sys
sys.path.append('../../')
#sys.path.append("../app")
'''
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
'''
#from app import *
from app.models import User, DatabaseConnection

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        return

    def __login(self, username, password):
        return self.app.post('/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_users(self):
        u = User(username='gaucan', password='gau')

        #rv = self.login('gaucan','gau')
        rv = self.app.get('/',follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
