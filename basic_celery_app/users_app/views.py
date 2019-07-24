from django.http import JsonResponse
from rest_framework import generics

from .models import User
from .serializers import CreateUserSerializer, UserSerializer, EditUserSerializer


class CreateUser(generics.CreateAPIView):
    """
    Create user
    """
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        linked_in_url = request.data.get('linked_in_url')
        twitter_url = request.data.get('twitter_url')
        blog_url = request.data.get('blog_url')
        status = request.data.get('status')
        username = request.data.get('username')

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

        user_data = UserSerializer(user).data
        print(user_data)
        response3 = {'status': 200, 'message': "User Created Successfully", 'data': {"user": user_data}}
        return JsonResponse(response3, status=200)


class EditUser(generics.CreateAPIView):
    """
    Edit user
    """
    serializer_class = EditUserSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        linked_in_url = request.data.get('linked_in_url')
        twitter_url = request.data.get('twitter_url')
        blog_url = request.data.get('blog_url')
        status = request.data.get('status')

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


class UserRetrieve(generics.CreateAPIView):
    """
    Retrieve user
    """
    serializer_class = EditUserSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
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


class DeleteUser(generics.CreateAPIView):
    """
    Delete user
    """
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        data = {}
        if "user_id" not in request.data.keys() or request.data['user_id'] == "":
            return JsonResponse({'status': 200, 'message': 'User ID is required', 'data': data}, status=500)

        try:
            user = User.objects.get(id=request.data['user_id'], is_deleted=0)
            user.is_deleted = 1
            user.save()
            response = {'status': 200, 'message': 'User deleted Successfully', 'data': {}}
            return JsonResponse(response, status=200)

        except:
            return JsonResponse({'status': 200, 'message': 'User ID is incorrect', 'data': data}, status=500)
