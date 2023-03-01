from app.project_evaluation.manager import UserManager
from test.test_basics import BasicsTestCase


class UserManagerTestCase(BasicsTestCase):

    def test_add_user(self):
        UserManager.add_user(user_name="test", password="test_password")

        self.assertTrue(UserManager.get_user(user_name="test") is not None)

    def test_delete_user(self):
        UserManager.delete_user(user_name="test")

        self.assertTrue(UserManager.get_user(user_name="test") is None)
