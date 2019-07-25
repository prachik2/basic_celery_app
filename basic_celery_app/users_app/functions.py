from .models import User


class CustomLoginModelBackend(object):
    """ Authenticate user by username or email """
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(is_active=True, username=username)
            if user.check_password(password):
                response3 = {"status": 0, "message": "User Exist", "user": user}
                return response3
            else:
                response1 = {"status": 1, "message": "Incorrect password"}
                return response1

        except User.DoesNotExist:
            response2 = {"status": 2, "message": "User with this username does not exist or is inactive"}
            return response2

