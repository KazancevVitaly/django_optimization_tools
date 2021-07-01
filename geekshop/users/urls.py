from django.urls import path

from users.views import GeekShopLogin, GeekShopRegister, GeekShopLogout, GeekShopProfile

app_name = 'users'

urlpatterns = [
    path('login/', GeekShopLogin.as_view(), name='login'),
    path('register/', GeekShopRegister.as_view(), name='register'),
    path('logout/', GeekShopLogout.as_view(), name='logout'),
    path('profile/,<int:pk>/', GeekShopProfile.as_view(), name='profile'),
]
