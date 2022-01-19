
from django.urls import path, include
from adaptation.api.views import AdaptationClassDetailAPIView, AdaptationCreateAPIView, AdaptationUpdateAPIView, FacultyListView, ScienceListView, StudentClassCreateAPI, StudentClassListAPIView, StudentClassUpdateAPI
from adaptation.views import *
urlpatterns = [
     path('adaptation', AdaptationCreateAPIView.as_view(), name="adaptation_create_api"),
     path('adaptation/<int:pk>', AdaptationUpdateAPIView.as_view(), name="adaptation_update_api"),
     
     path('adaptation_class/<int:pk>', AdaptationClassDetailAPIView.as_view(), name="adaptation_class_detail_api"),
     

     path('student_classes_list', StudentClassListAPIView.as_view(), name="student_classes_list_api"),
     path('student_class', StudentClassCreateAPI.as_view(), name="student_class_create_api"),
     path('student_class/<int:pk>', StudentClassUpdateAPI.as_view(), name="student_class_update_api"),
     
     path('faculty_list', FacultyListView.as_view(), name="faculty_list_api"),
     path('science_list', ScienceListView.as_view(), name="science_list_api"),
]
 
