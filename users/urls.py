from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_edit/<int:pk>', views.user_edit, name='user_edit'),
    path('user_remove/<int:pk>', views.user_remove, name='user_remove'),
    path('password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]


