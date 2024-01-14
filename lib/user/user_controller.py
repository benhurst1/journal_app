from lib.user.user import User

class UserController:
    def create_user_object(self, username, email, password):
        user = User(username, email, password)
        return user
