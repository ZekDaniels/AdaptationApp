from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from user.forms import UserPasswordResetFormForm
from user.views import *
urlpatterns = [
    # dashboard urls
    path('', DashboardView.as_view(), name="dashboard"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    
    # login-logoutr-register urls
    path('login/', LoginPageView.as_view(), name="login_page"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register_page"),
    
    # password reset urls
     path(
         "password_reset/",
          PasswordResetView.as_view(
         template_name="registration/password_reset_done.html",
         form_class=UserPasswordResetFormForm
         ),
          
          name="password_reset"
     ),
     path("password_reset_sent/", PasswordResetDoneView.as_view(), name="password_reset_done"),
     path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
     path("password_reset_complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
