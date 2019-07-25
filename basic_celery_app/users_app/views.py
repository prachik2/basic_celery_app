from django.http import JsonResponse
from rest_framework import generics
from .functions import CustomLoginModelBackend

from .models import User, Token
from .serializers import CreateUserSerializer, UserSerializer, EditUserSerializer, LoginSerializer


class CreateUser(generics.CreateAPIView):
    """
    Create user
    """
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        if "token" not in request.data.keys():
            return JsonResponse({"status": 500, "message": "Token field is required", 'data': {}})
        if request.data['token'] == "":
            return JsonResponse({"status": 500, "message": "Token cannot be null", 'data': {}})

        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        linked_in_url = request.data.get('linked_in_url')
        twitter_url = request.data.get('twitter_url')
        blog_url = request.data.get('blog_url')
        status = request.data.get('status')
        username = request.data.get('username')
        token = request.data.get('token')

        try:
            token_obj = Token.objects.get(key=token)
        except:
            return JsonResponse({"status": 500, "message": "Incorrect token", 'data': {}})

        user_id = token_obj.user_id
        data = User.objects.get(id=user_id)
        if data:
            try:
                user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name,
                                       linked_in_url=linked_in_url,twitter_url=twitter_url, blog_url=blog_url, status=status)

            except:
                response1 = {"status": 500, "message": "Error in creating user object", 'data': {}}
                return JsonResponse(response1, status=500)

            try:
                user.save()
            except:
                response2 = {"status": 500, "message": "Error in saving user object", 'data': {}}
                return JsonResponse(response2, status=500)

            response3 = {'status': 200, 'message': "User Created Successfully", 'data': {}}
            return JsonResponse(response3, status=200)
        else:
            response4 = {'status': 500, 'message': "User Not Created", 'data': {}}
            return JsonResponse(response4, status=500)


class EditUser(generics.CreateAPIView):
    """
    Edit user
    """
    serializer_class = EditUserSerializer

    def create(self, request, *args, **kwargs):
        if "token" not in request.data.keys():
            return JsonResponse({"status": 500, "message": "Token field is required", 'data': {}})
        if request.data['token'] == "":
            return JsonResponse({"status": 500, "message": "Token cannot be null", 'data': {}})

        user_id = request.data.get('user_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        linked_in_url = request.data.get('linked_in_url')
        twitter_url = request.data.get('twitter_url')
        blog_url = request.data.get('blog_url')
        status = request.data.get('status')
        token = request.data.get('token')

        try:
            token_obj = Token.objects.get(key=token)
        except:
            return JsonResponse({"status": 500, "message": "Incorrect token", 'data': {}})

        token_user_id = token_obj.user_id
        data = User.objects.get(id=token_user_id)
        if data:
            try:
                user = User.objects.get(id=user_id)

            except:
                return JsonResponse({"status": 500, "message": "Incorrect user_id", 'data': {}}, status=500)

            if first_name:
                user.first_name = first_name

            if last_name:
                user.last_name = last_name

            if email:
                user.email = email

            if linked_in_url:
                user.linked_in_url = linked_in_url

            if twitter_url:
                user.twitter_url = twitter_url

            if blog_url:
                user.blog_url = blog_url

            if status:
                user.status = status

            try:
                user.save()

            except:
                return JsonResponse({"status": 500, "message": "error in editing user", 'data': {}}, status=500)

            response1 = {"status": 200, "message": "User updated Successfully.", 'data': {}}
            return JsonResponse(response1, status=200)

        else:
            response2 = {"status": 500, "message": "User not updated.", 'data': {}}
            return JsonResponse(response2, status=500)


class UserRetrieve(generics.CreateAPIView):
    """
    Retrieve user
    """
    serializer_class = EditUserSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        token = request.data.get('token')

        if "token" not in request.data.keys():
            return JsonResponse({"status": 500, "message": "Token field is required", 'data': {}})
        if request.data['token'] == "":
            return JsonResponse({"status": 500, "message": "Token cannot be null", 'data': {}})

        try:
            token_obj = Token.objects.get(key=token)
        except:
            return JsonResponse({"status": 500, "message": "Incorrect token", 'data': {}})

        token_user_id = token_obj.user_id
        data = User.objects.get(id=token_user_id)
        if data:
            if "user_id" not in request.data.keys():
                return JsonResponse({'status': 500, 'message': "user_id field is required", 'data': {}}, status=500)

            try:
                user = User.objects.get(id=user_id)
            except:
                return JsonResponse({"status": 500, "message": "Incorrect User id", 'data': {}}, status=500)

            try:
                user_data = UserSerializer(user).data
            except:
                return JsonResponse({"status": 500, "message": "Incorrect User", 'data': {}}, status=500)

            return JsonResponse({"status": 200, "message": "User Retrieved Successfully", 'data': {"user": user_data}}, status=200)
        else:
            return JsonResponse({"status": 500, "message": "User not Retrieved", 'data': {}}, status=500)


class DeleteUser(generics.CreateAPIView):
    """
    Delete user
    """
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        token = request.data.get('token')
        if "token" not in request.data.keys():
            return JsonResponse({"status": 500, "message": "Token field is required", 'data': {}})
        if request.data['token'] == "":
            return JsonResponse({"status": 500, "message": "Token cannot be null", 'data': {}})

        try:
            token_obj = Token.objects.get(key=token)
        except:
            return JsonResponse({"status": 500, "message": "Incorrect token", 'data': {}})

        token_user_id = token_obj.user_id
        data = User.objects.get(id=token_user_id)
        if data:
            if "user_id" not in request.data.keys() or request.data['user_id'] == "":
                return JsonResponse({'status': 200, 'message': 'User ID is required', 'data': data}, status=500)

            try:
                user = User.objects.get(id=request.data['user_id'], is_deleted=0)
                user.is_deleted = 1
                user.save()
                response = {'status': 200, 'message': 'User deleted Successfully', 'data': {}}
                return JsonResponse(response, status=200)

            except:
                return JsonResponse({'status': 500, 'message': 'User ID is incorrect', 'data': {}}, status=500)
        else:
            return JsonResponse({'status': 500, 'message': 'User not deleted', 'data': {}}, status=500)


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')
        response = CustomLoginModelBackend.authenticate(self, username=username, password=password)
        if response['status'] == 0:
            user_data = UserSerializer(response['user']).data
            token = Token.objects.create(user=response['user'])
            key = token.key
            data = {"user": user_data, "token": key}

            response1 = {"status": 200, "message": "Logged In Successfully", 'data': data}
            return JsonResponse(response1, status=200)

