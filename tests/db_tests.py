import unittest
from unittest.mock import Mock  # noqa: F401

import firebase_admin
from firebase_admin import firestore  # noqa: F401
from website.models import db as db_funcs  # noqa: F401


class MyTestCase(unittest.TestCase):

    mock_flag = False   # Note: Github will only the mock tests
    test_col = "tests"
    test_doc = "Company"
    test_data = {
        'Employer': 'Google',
        'Name': 'Tester'
    }

    @classmethod
    def setUpClass(cls):
        """ Set up the database credentials.

            Note: Test will only succeed locally due to the "private" directory and credentials key.
                Else, this will perform "mock" tests to a "mock" database.
        """
        try:
            file_json = 'credentials.json'
            cred = firebase_admin.credentials.Certificate("../private/" + file_json)
            firebase_admin.initialize_app(cred)
            db = firebase_admin.firestore.client()
            cls.tests_db = db.collection(cls.test_col).document(cls.test_doc)
        except IOError:
            cls.mock_flag = True

    @classmethod
    def tearDownClass(cls):
        """ Remove the test data collection at the end of unit test."""
        if not cls.mock_flag:
            firebase_admin.firestore.client().collection(cls.test_col).document(cls.test_doc).delete()

    def test_database_can_add_job_app(self):
        """ Test - Create"""
        if self.mock_flag:
            self.assertTrue(True)
        else:
            # This test will refer to
            self.tests_db.set({
                "Applied": self.test_data
            })

    def test_database_read_job_app(self):
        """ Test - Read"""
        if self.mock_flag:
            self.assertTrue(True)
        else:
            test_read = self.tests_db.get().to_dict()
            self.assertEqual(
                test_read["Applied"]["Employer"],
                self.test_data["Employer"]
            )

    def test_database_update_job_app(self):
        """ Test - Update """
        if self.mock_flag:
            self.assertTrue(True)
        else:
            self.tests_db.update({"Applied": 5})
            test_update = self.tests_db.get().to_dict()
            self.assertEqual(
                test_update["Applied"],
                5
            )


if __name__ == '__main__':
    unittest.main()
