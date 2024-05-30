from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserPasswordResetView, successfully, email_confirm, user_list, block_user, unblock_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', UserCreateView.as_view(), name="register"),
    path('email-verification/', email_verification, name="email_verification"),
    path('email-confirm/<str:token>/', email_confirm, name="email_confirm"),
    path('successfully/', successfully, name="successfully"),
    path('reset-password/', UserPasswordResetView.as_view(), name="reset-password"),
    path('users/', user_list, name='user_list'),
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/block/', block_user, name='block_user'),
    path('users/<int:user_id>/unblock/', unblock_user, name='unblock_user'),
]