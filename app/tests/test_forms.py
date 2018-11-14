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
        self.session = models.DatabaseConnection()
        self.session.open()

    def tearDown(self):
        self.session.close()
        return

    def __login(self, username, password):
        return self.app.post('/', data=dict(
            username=username,
            pswd=password
        ), follow_redirects=True)

    def test_users(self):
        self.app.get('/',follow_redirects=False)
        output = self.__login('will', 'password')
        print(output.data)
        u = models.User(username='invalid_user', pswd='invalid_password')
        #out2 = self.app.get('/',follow_redirects=True)
        #print(out2.data)
        return output.data

if __name__ == '__main__':
    unittest.main()
