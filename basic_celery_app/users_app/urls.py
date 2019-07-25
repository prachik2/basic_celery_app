from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path('create/', views.CreateUser.as_view(), name='create_user'),
    path('edit/', views.EditUser.as_view(), name='edit_user'),
    path('retrieve/', views.UserRetrieve.as_view(), name='retrieve_user'),
    path('delete/', views.DeleteUser.as_view(), name='delete_user'),

    path('login/', views.Login.as_view(), name='login'),
]
