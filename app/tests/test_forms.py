import unittest
import sys
sys.path.append('../../')

from app import models
from app import app


class TestWebForms(unittest.TestCase):
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
        self.profile_page = '/profile'

    def _delete_test_user(self):
            user_info = models.User(username=self.username, pswd=self.password)
            self.db.query(models.User).filter_by(username=self.username, pswd=self.password).delete()
            self.db.commit()

    def _add_test_user(self):
            u = models.User(username=self.username, pswd=self.password)
            self.db.add(u)
            self.db.commit()

    def _make_post(self, page, username, password):
        return self.app.post(page, data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def _test_user_in_db(self):
        check_user = self.db.query(models.User).filter_by(username=self.username, pswd=self.password).count()
        return True if check_user >= 1 else False

    def tearDown(self):
        self.session.close()
        return


class TestSignUp(TestWebForms):
    def test_invalid_signup(self):
        # ensure the username will be invalid
        if not self._test_user_in_db():
            self._add_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self._make_post(self.sign_up_page, self.username, self.password)

        self.assertIn('Username &#34;{}&#34; Already In Use!'.format(self.username), str(response.data))

    def test_valid_signup(self):
        # ensure username and pass are not already in the db
        if self._test_user_in_db():
            self._delete_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self._make_post(self.sign_up_page, self.username, self.password)

        self.assertNotIn('Username &#34;{}&#34; Already In Use!'.format(self.username), str(response.data))


class TestLogin(TestWebForms):
    def test_invalid_login(self):
        # ensure bad_username/pass are not saved already
        if self._test_user_in_db():
            self._delete_test_user()

        self.app.get(self.login_page, follow_redirects=True)

        response = self._make_post(self.login_page, self.username, self.password)

        self.assertIn("Invalid Username or Password", str(response.data))

    def test_valid_login(self):
        # ensure username and pass are saved
        if not self._test_user_in_db():
            self._add_test_user()

        self.app.get(self.login_page,follow_redirects=True)

        response = self._make_post(self.login_page, self.username, self.password)

        self.assertNotIn("Invalid Username or Password", str(response.data))

    def test_login_rate_limit(self):
        # ensure username and pass are saved
        if not self._test_user_in_db():
            self._add_test_user()

        self.app.get(self.login_page,follow_redirects=True)

        # 5 Failed Attempted Login
        response = self._make_post(self.login_page, self.username, self.password + 'oops1')
        self.assertIn("Invalid Username or Password", str(response.data))

        response = self._make_post(self.login_page, self.username, self.password + 'oops2')
        self.assertIn("Invalid Username or Password", str(response.data))

        response = self._make_post(self.login_page, self.username, self.password + 'oops3')
        self.assertIn("Invalid Username or Password", str(response.data))

        response = self._make_post(self.login_page, self.username, self.password + 'oops4')
        self.assertIn("Invalid Username or Password", str(response.data))

        response = self._make_post(self.login_page, self.username, self.password + 'oops5')
        self.assertIn("Maximum Login Attempts Reached, Please Try Again Later", str(response.data))


class TestProfile(TestWebForms):
    # 10 < age < 150
    # sex 'male' or 'female'
    # 40lbs < weight < 1500lbs
    # 30in <  height < 110
    # 0.0 packs < smoke packs a day < 4.0 packs
    # diabetes: Type I, Type II, None

    def test_invalid_profiles(self):
        self.app.get(self.profile_page, follow_redirects=True)

        # Invalid Age
        response = self._make_post(self.profile_page, 1, 'male', 190, 65, 70, 0, 'None')
        self.assertIn("Invalid Personal Information", str(response.data))

        # Invalid Sex
        response = self._make_post(self.profile_page, 19, '', 190, 65, 70, 0, 'None')
        self.assertIn("Invalid Personal Information", str(response.data))

        # Invalid weight
        response = self._make_post(self.profile_page, 19, 'male', -1, 65, 70, 0, 'Type I')
        self.assertNotIn("Invalid Personal Information", str(response.data))

        # Invalid height
        response = self._make_post(self.profile_page, 19, 'male', -1, -1, 70, 0, 'Type I')
        self.assertNotIn("Invalid Personal Information", str(response.data))

        # Invalid smoking info
        response = self._make_post(self.profile_page, 1, 'male', 190, 65, 70, -1, 'None')
        self.assertNotIn("Invalid Personal Information", str(response.data))

        # Invalid diabetes info
        response = self._make_post(self.profile_page, 1, 'male', 190, 65, 70, 0.0, 'Yes')
        self.assertNotIn("Invalid Personal Information", str(response.data))


    def test_valid_profile(self):
        self.app.get(self.profile_page, follow_redirects=True)

        # Invalid Age
        response = self._make_post(self.profile_page, 33, 'male', 270, 67, 70, 0.5, 'None')
        self.assertNotIn("Invalid Personal Information", str(response.data))


if __name__ == '__main__':
    unittest.main()
