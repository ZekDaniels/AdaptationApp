
from django.urls import path
from user.api.views import *
urlpatterns = [
     
     path('user_classes_list', UserListView.as_view(), name="user_classes_list_api"),
    
]
 
