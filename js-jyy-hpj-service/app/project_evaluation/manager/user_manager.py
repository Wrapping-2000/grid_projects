from werkzeug.security import generate_password_hash
from app.project_evaluation.manager.models import User
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return UserManager.get_user_from_id(user_id)


class UserManager:

    @staticmethod
    def add_user(user_name, password):
        u = User(user_name=user_name,
                 password_hash=generate_password_hash(password))
        u.save()

    @staticmethod
    def get_user(user_name):
        return User.objects(user_name=user_name).first()

    @staticmethod
    def get_user_from_id(user_id):
        return User.objects(id=user_id).first()

    @staticmethod
    def delete_user(user_name):
        user = UserManager.get_user(user_name)
        if user:
            user.delete()
            return True

        return False
