import unittest
import sys
sys.path.append('../../')

from app import models

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.special_username = 'this_is_for_testing_databaseconnection'

    def test_teardown_method(self):
        with models.DatabaseConnection() as db:
            count = db.query(models.UserSchema).filter_by(username=self.special_username).count()
            self.assertEqual(count, 1)

    def test_open_connection_method(self):
        test_session = models.DatabaseConnection()
        # Check that the connection to the database has not been opened yet
        self.assertEqual(test_session.db, None)
        test_session.open()

        self.assertNotEqual(test_session.db, None)

        count = test_session.db.query(models.UserSchema).filter_by(username=self.special_username).count()
        self.assertEqual(count, 1)



class TestUserSchema(unittest.TestCase):
    def setUp(self):
        # ensure clean test enviroment
        self.username = 'test_username'
        self.password = 'test_password'
        with models.DatabaseConnection() as db:
            count = db.query(models.UserSchema).filter_by(username=self.username).count()
            if count >= 1:
                user_info = models.UserSchema(username=self.username, pswd=self.password)
                db.query(models.UserSchema).filter_by(username=self.username).delete()
                db.commit()

    def test_user_schema(self):
        with models.DatabaseConnection() as db:
            user_info = models.UserSchema(username=self.username, pswd=self.password)
            check_user = db.query(models.UserSchema).filter_by(username=self.username).count()
            # Check that user does not exist
            self.assertEqual(check_user, 0)

            db.add(user_info)
            db.commit()

            # Check that both Username and Password are in the db
            check_user_after = db.query(models.UserSchema).filter_by(username=self.username, pswd=self.password).count()
            # Check that user now exists
            self.assertEqual(check_user_after, 1)
            # User is deleted, since it is created for testing purposes
            db.query(models.UserSchema).filter_by(username=self.username).delete()


if __name__ == '__main__':
    unittest.main()
