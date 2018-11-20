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
        self.user_dict = dict(username=self.username, password=self.password)

        self.profile_dict = dict(
                age=18,
                sex='male',
                weight=190,
                height=65,
                smoker=0.0,
                diabetes='None')

        self.login_page = '/'
        self.sign_up_page = '/sign_up'
        self.profile_page = '/profile'
        self.logout_page = '/logout'

    """
    Helpers to ensure user info is in the database prior to testing webform
    """
    def _delete_test_user(self):
        user_info = models.UserSchema(username=self.username, pswd=self.password)
        self.db.query(models.UserSchema).filter_by(username=self.username, pswd=self.password).delete()
        self.db.commit()

    def _add_test_user(self):
        u = models.UserSchema(username=self.username, pswd=self.password)
        self.db.add(u)
        self.db.commit()

    def _make_post(self, page, data_dict):
        return self.app.post(page, data=data_dict, follow_redirects=True)

    def _test_user_in_db(self):
        check_user = self.db.query(models.UserSchema).filter_by(username=self.username, pswd=self.password).count()
        return True if check_user >= 1 else False

    def tearDown(self):
        self.session.close()
        return


class TestSignUp(TestWebForms):

    def test_invalid_signup(self):

        # Username should not be the same as password
        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user1 = dict(username="test_username",password="test_username")
        response = self._make_post(self.sign_up_page, invalid_user1)

        self.assertIn('Invalid username and/or password.', str(response.data))

        # Username and password should be at least 5 characters but less than 50
        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user2 = dict(username="test",password="pass")
        response = self._make_post(self.sign_up_page, invalid_user2)

        self.assertIn('Invalid username and/or password.', str(response.data))

        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user1 = dict(username="test_username_that_is_too_long_12345678901234567890",
            password="test_password_that_is_too_long_12345678901234567890")
        response = self._make_post(self.sign_up_page, invalid_user1)

        self.assertIn('Invalid username and/or password.', str(response.data))

        # Username and password should contain at least 1 letter
        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user2 = dict(username="*****",password="password")
        response = self._make_post(self.sign_up_page, invalid_user2)

        self.assertIn('Invalid username and/or password.', str(response.data))


    def test_existing_user(self):
        # ensure the username will be invalid
        if not self._test_user_in_db():
            self._add_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self._make_post(self.sign_up_page, self.user_dict)

        self.assertIn('Username &#34;{}&#34; Already In Use!'.format(self.username), str(response.data))

    def test_valid_signup(self):
        # ensure username and pass are not already in the db
        if self._test_user_in_db():
            self._delete_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self._make_post(self.sign_up_page, self.user_dict)

        self.assertNotIn('Username &#34;{}&#34; Already In Use!'.format(self.username), str(response.data))


class TestLogin(TestWebForms):

    def test_invalid_login(self):
        # ensure bad_username/pass are not saved already
        if self._test_user_in_db():
            self._delete_test_user()

        self.app.get(self.login_page, follow_redirects=True)

        response = self._make_post(self.login_page, self.user_dict)

        self.assertIn("Invalid Username or Password", str(response.data))

    def test_valid_login(self):
        # ensure username and pass are saved
        if not self._test_user_in_db():
            self._add_test_user()

        self.app.get(self.login_page,follow_redirects=True)

        response = self._make_post(self.login_page, self.user_dict)

        self.assertNotIn("Invalid Username or Password", str(response.data))

    def test_login_rate_limit(self):
        # ensure username and pass are saved
        if not self._test_user_in_db():
            self._add_test_user()

        self.app.get(self.login_page,follow_redirects=True)

        # 5 Failed Attempted Login
        self.user_dict.update(password=self.password + 'oops1')
        response = self._make_post(self.login_page, self.user_dict)
        self.assertIn("Invalid Username or Password", str(response.data))

        self.user_dict.update(password=self.password + 'oops2')
        response = self._make_post(self.login_page, self.user_dict)
        self.assertIn("Invalid Username or Password", str(response.data))

        self.user_dict.update(password=self.password + 'oops3')
        response = self._make_post(self.login_page, self.user_dict)
        self.assertIn("Invalid Username or Password", str(response.data))

        self.user_dict.update(password=self.password + 'oops4')
        response = self._make_post(self.login_page, self.user_dict)
        self.assertIn("Invalid Username or Password", str(response.data))

        self.user_dict.update(password=self.password + 'oops5')
        response = self._make_post(self.login_page, self.user_dict)
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
        self.profile_dict.update(age=-1)
        response = self._make_post(self.profile_page, self.profile_dict)
        self.assertIn("Invalid Personal Information", str(response.data))

        # Invalid Sex
        self.profile_dict.update(age=22, sex='')
        response = self._make_post(self.profile_page, self.profile_dict)
        self.assertIn("Invalid Personal Information", str(response.data))

        # Invalid weight
        self.profile_dict.update(sex='female',weight=-1)
        response = self._make_post(self.profile_page, self.profile_dict)
        self.assertIn("Invalid Personal Information", str(response.data))

        # Invalid height
        self.profile_dict.update(weight=140, height=-1)
        response = self._make_post(self.profile_page, self.profile_dict)
        self.assertIn("Invalid Personal Information", str(response.data))

        # Invalid smoking info
        self.profile_dict.update(height=55, smoker=-1)
        response = self._make_post(self.profile_page, self.profile_dict)
        self.assertIn("Invalid Personal Information", str(response.data))

        # Invalid diabetes info
        self.profile_dict.update(smoker=0.5, diabetes='invalid')
        response = self._make_post(self.profile_page, self.profile_dict)
        self.assertIn("Invalid Personal Information", str(response.data))

        self.profile_dict.update(diabetes='Type II')

    def test_valid_profile(self):
        self.app.get(self.profile_page, follow_redirects=True)

        response = self._make_post(self.profile_page, self.profile_dict)
        self.assertNotIn("Invalid Personal Information", str(response.data))


class TestLogout(TestWebForms):

    def test_invalid_logout(self):
        # If not logged in, can't log out
        self.app.get(self.logout_page, follow_redirects=True)
        response = self._make_post(self.logout_page, {})
        # Check that you are taken back to home page
        self.assertIn("Login", str(response.data))

    def test_valid_logout(self):
        # Login first
        response = self.app.get(self.login_page, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self._make_post(self.login_page, self.user_dict)
        self.assertNotIn('Username &#34;{}&#34; Already In Use!'.format(self.username), str(response.data))

        self.app.get(self.logout_page, follow_redirects=True)

        response = self._make_post(self.logout_page, {})
        # Check that you are taken back to home page
        self.assertIn("Login", str(response.data))


if __name__ == '__main__':
    unittest.main()
