import unittest
import requests


class AuthViewsTestCase(unittest.TestCase):

    def test_register(self):
        data = {
            "user_name": "test",
            "password": "test_password"
        }
        response = requests.post("http://127.0.0.1:5000/auth/register",
                                 json=data)

        self.assertTrue(response.status_code == 200)

    def test_login(self):
        data = {
            "user_name": "test",
            "password": "test_password"
        }
        response = requests.post("http://127.0.0.1:5000/auth/login",
                                 json=data)

        print(response.headers)
        print(response.content)
        # self.assertTrue(response.status_code == 200)