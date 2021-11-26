
from django.urls import path, include
from adaptation.api.views import FacultyListView, ScienceListView
from adaptation.views import *
urlpatterns = [
     path('faculty_list', FacultyListView.as_view(), name="faculty_list_api"),
     path('science_list', ScienceListView.as_view(), name="science_list_api")
]
 
