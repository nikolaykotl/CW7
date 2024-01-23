from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserDetailView, UserUpdateView, \
    UserCreateView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('user/create/', UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(),
         name='user_update'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_view'),

]
