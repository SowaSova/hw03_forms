from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),

    path('signup/', views.SignUp.as_view(), name='signup'),

    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),

    path('password_reset_form/',
         views.PasswordReset.as_view(
             template_name='users/password_reset_form.html'),
         name='prf'),

    path('password_change_form/',
         LoginView.as_view(template_name='users/password_change_form.html'),
         name='pcf'),

    path('password_reset_done/', LoginView.as_view(template_name='users/password_reset_done.html'),
         name='prd')

]
