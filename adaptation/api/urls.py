
from django.urls import path, include
from adaptation.api.views import AdaptationCreateAPIView, AdaptationUpdateAPIView, FacultyListView, ScienceListView, StudentClassCreateAPI
from adaptation.views import *
urlpatterns = [
     path('adaptation', AdaptationCreateAPIView.as_view(), name="adaptation_create_api"),
     path('adaptation/<int:pk>', AdaptationUpdateAPIView.as_view(), name="adaptation_update_api"),
     
     path('student_class', StudentClassCreateAPI.as_view(), name="student_class_create_api"),
     
     path('faculty_list', FacultyListView.as_view(), name="faculty_list_api"),
     path('science_list', ScienceListView.as_view(), name="science_list_api"),
]
 
