from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path, include
from user.forms import UserPasswordResetForm, UserSetPasswordForm
from user.views import *

urlpatterns = [
    # dashboard urls
    path("", DashboardView.as_view(), name="dashboard"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # login-logoutr-register urls
    path("login/", LoginPageView.as_view(), name="login_page"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register_page"),
    # password reset urls
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            form_class=UserPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=UserSetPasswordForm,

        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",

        ),
        name="password_reset_complete",
    ),
    path('activate/<uidb64>/<token>/',ActivationView.as_view(), name='activate_user'),  

    # path('api/', include('user.api.urls')),

]
