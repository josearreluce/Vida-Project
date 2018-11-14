import unittest
import sys
sys.path.append('../../')
from app import models
from app import app

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
            pswd=password
        ), follow_redirects=True)

    def test_users(self):
        u = models.User(username='gaucan', pswd='gau')

        #rv = self.login('gaucan','gau')
        rv = self.app.get('/',follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
