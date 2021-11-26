from django.urls import path, include
from adaptation.views import *
app_name = "adaptation"

urlpatterns = [
    path('', ProtoAdaptionCreateView.as_view(), name="adaptation_create"),
    path('api/', include('adaptation.api.urls')),
]