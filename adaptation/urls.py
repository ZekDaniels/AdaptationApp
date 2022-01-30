from django.urls import path, include
from adaptation.views import *
app_name = "adaptation"

urlpatterns = [
    path('', AdaptationCreateView.as_view(), name="adaptation_create"),
    path('<int:id>', AdaptationManageView.as_view(), name="adaptation_manage"),
    path('adaptation_list', AdaptationList.as_view(), name="adaptation_list"),
    path('api/', include('adaptation.api.urls')),
]