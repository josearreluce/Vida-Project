import unittest
import sys
sys.path.append('../../')

from app import models
from app import app, db


class TestWebForms(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.session = models.DatabaseConnection()
        self.session.open()
        self.db = db.session

        self.login_page = '/'
        self.sign_up_page = '/sign_up'
        self.profile_page = '/profile'
        self.logout_page = '/logout'

        # Basic Username, password, and profile info
        self.username = 'test_username'
        self.password = 'test_password'
        self.user_dict = dict(username=self.username, password=self.password, password2=self.password)

        self.profile_dict = dict(
                age=18,
                sex='male',
                weight=190,
                height=65,
                smoker=0.0,
                diabetes='None')

    """
    Helpers to ensure user info is in the database prior to testing webform
    """
    def _delete_test_user(self):
        u = models.UserSession(username=self.username)
        u.set_password(self.password)
        u.query.filter_by(username=u.username).delete()
        self.db.commit()

    def _add_test_user(self):
        u = models.UserSession(username=self.username)
        u.set_password(self.password)
        self.db.add(u)
        self.db.commit()

    def _make_post(self, page, data_dict):
        return self.app.post(page, data=data_dict, follow_redirects=True)

    def _test_user_in_db(self):
        u = models.UserSession(username=self.username)
        u.set_password(self.password)
        check_user = u.query.filter_by(username=self.username).count()
        if check_user and u.check_password(self.password):
            return True
        else:
            return False

    def tearDown(self):
        self.session.close()
        return


class TestSignUp(TestWebForms):

    def test_invalid_signup(self):
        if self._test_user_in_db():
            self._delete_test_user()

        # Username should not be the same as password
        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user1 = dict(username="test_username",password="test_username",password2="test_username")
        response = self._make_post(self.sign_up_page, invalid_user1)

        self.assertIn('Username Cannot Equal Password!', str(response.data))

        # Username and password should be at least 5 characters but less than 50
        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user2 = dict(username="test",password="pass",password2="pass")
        response = self._make_post(self.sign_up_page, invalid_user2)
        self.assertIn('Invalid Username or Password.', str(response.data))

        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user1 = dict(username="test_username_that_is_too_long_12345678901234567890",
            password="test_password_that_is_too_long_12345678901234567890",
            password2="test_password_that_is_too_long_12345678901234567890")
        response = self._make_post(self.sign_up_page, invalid_user1)

        self.assertIn('Invalid Username or Password.', str(response.data))

        # Username and password should contain at least 1 letter
        self.app.get(self.sign_up_page, follow_redirects=True)
        invalid_user2 = dict(username="*****",password="password")
        response = self._make_post(self.sign_up_page, invalid_user2)

        self.assertIn('Invalid Username or Password.', str(response.data))


    def test_existing_user(self):
        # ensure the username will be invalid
        if not self._test_user_in_db():
            self._add_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self._make_post(self.sign_up_page, self.user_dict)

        self.assertIn('Username Already In Use!', str(response.data))

    def test_valid_signup(self):
        # ensure username and pass are not already in the db
        if self._test_user_in_db():
            self._delete_test_user()

        self.app.get(self.sign_up_page, follow_redirects=True)
        response = self._make_post(self.sign_up_page, self.user_dict)

        self.assertNotIn('Username Already In Use!', str(response.data))


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

        # Ensure no errors were thrown
        self.assertNotIn("Invalid Username or Password", str(response.data))

        # Ensure sucessful redirect
        self.assertIn("Start Assessment", str(response.data))

        # Ensure Home page no longer shows the Login Form
        response = self.app.get(self.login_page, follow_redirects=True)
        self.assertIn("We are Vida, your personalized healthcare advisor.", str(response.data))


class TestLoginLimit(TestWebForms):
    # Required to be a different class since this will block all other login testing
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

        # This ensures that brute force attacks will not be possible
        # by limiting the number of attempted logins
        self.assertIn("Maximum Failed Logins Reached. Please Restart Flask", str(response.data))



class TestProfile(TestWebForms):
    # 10 < age < 150
    # sex 'male' or 'female'
    # 40lbs < weight < 1500lbs
    # 30in <  height < 110
    # 0.0 packs < smoke packs a day < 4.0 packs
    # Blood pressure range (100/50 to 150/100)
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
        response = self.app.get(self.logout_page, follow_redirects=True)
        # We don't allow users to go to log out if they aren't logged in
        # 401 Is an unauthorized status code
        self.assertEqual(response.status_code, 401)


    def test_valid_logout(self):
        # Login first
        response = self.app.get(self.login_page, follow_redirects=True)

        response = self._make_post(self.login_page, self.user_dict)
        self.assertNotIn('Username Already In Use!', str(response.data))

        self.app.get(self.logout_page, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        response = self.app.get(self.login_page, follow_redirects=True)
        # Check that you are taken back to home page
        # And that the home page now displays a login form once again
        self.assertIn("Login", str(response.data))


if __name__ == '__main__':
    unittest.main()
