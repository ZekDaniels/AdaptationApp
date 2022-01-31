
from django.urls import path, include
from adaptation.api.views import *
from adaptation.views import *
urlpatterns = [
     
     path('adaptations_list', AdaptationListView.as_view(), name="adaptations_list_api"),
     path('adaptation', AdaptationCreateAPIView.as_view(), name="adaptation_create_api"),
     path('adaptation/<int:pk>', AdaptationUpdateAPIView.as_view(), name="adaptation_update_api"),
     path('adaptation/<int:pk>/closed', AdaptationClosedUpdateAPIView.as_view(), name="adaptation_closed_api"),
     
     path('adaptation_class/<int:pk>', AdaptationClassDetailAPIView.as_view(), name="adaptation_class_detail_api"),
     
     path('adaptation_class_confirmation', AdaptationClassConfirmationCreateAPIView.as_view(), name="adaptation_class_confirmation_api"),
     path('adaptation_class_confirmation/<int:pk>', AdaptationClassConfirmationDestroyAPIView.as_view(), name="adaptation_class_confirmation_delete_api"),

     path('student_classes_list', StudentClassListAPIView.as_view(), name="student_classes_list_api"),
     path('student_class', StudentClassCreateAPI.as_view(), name="student_class_create_api"),
     path('student_class/<int:pk>', StudentClassUpdateAPI.as_view(), name="student_class_update_api"),
     
     path('faculty_list', FacultyListView.as_view(), name="faculty_list_api"),
     path('science_list', ScienceListView.as_view(), name="science_list_api"),
]
 
