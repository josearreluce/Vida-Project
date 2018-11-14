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
        self.db = self.session.db

        self.username = 'test_username'
        self.password = 'test_password'

        self.login_page = '/'
        self.sign_up_page = '/sign_up'


    def __delete_test_user(self):
            user_info = models.User(username=self.username, pswd=self.password)
            self.db.query(models.User).filter_by(username=self.username, pswd=self.password).delete()
            self.db.commit()

    def __add_test_user(self):
            u = models.User(username=self.username, pswd=self.password)
            self.db.add(u)
            self.db.commit()

    def __make_post(self, page, username, password):
        return self.app.post(page, data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def __test_user_in_db(self):
        check_user = self.db.query(models.User).filter_by(username=self.username, pswd=self.password).count()
        return True if check_user >= 1 else False

    def test_invalid_signup(self):
        # ensure the username will be invalid
        if not self.__test_user_in_db():
            self.__add_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self.__make_post(
                self.sign_up_page,
                self.username,
                self.password)


        self.assertIn('Username &#34;{}&#34; Already In Use!'.format(self.username), str(response.data))

    def test_valid_signup(self):
        # ensure username and pass are not already in the db
        if self.__test_user_in_db():
            self.__delete_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self.__make_post(
                self.sign_up_page,
                self.username,
                self.password)

        self.assertNotIn('Username &#34;{}&#34; Already In Use!'.format(self.username), str(response.data))

    def test_invalid_login(self):
        # ensure bad_username/pass are not saved already
        if self.__test_user_in_db():
            self.__delete_test_user()

        self.app.get(self.login_page, follow_redirects=True)
        response = self.__make_post(
                self.login_page,
                self.username,
                self.password)

        self.assertIn("Invalid Username or Password", str(response.data))

    def test_valid_login(self):
        # ensure username and pass are saved
        if not self.__test_user_in_db():
            self.__add_test_user()

        self.app.get(self.login_page,follow_redirects=True)
        response = self.__make_post(
                self.login_page,
                self.username,
                self.password)

        self.assertNotIn("Invalid Username or Password", str(response.data))

    def tearDown(self):
        self.session.close()
        return

if __name__ == '__main__':
    unittest.main()
