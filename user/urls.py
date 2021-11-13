from django.contrib.auth.views import LogoutView
from django.urls import path, include
from user.views import *
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('login/', LoginPageView.as_view(), name="login_page"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register_page"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]
