from django.urls import path, include
from adaptation.views import *
app_name = "adaptation"

urlpatterns = [
    path('', AdaptationCreateView.as_view(), name="adaptation_create"),
    path('<int:id>/', AdaptationManageView.as_view(), name="adaptation_manage"),
    path('result/', AdaptationResultView.as_view(), name="adaptation_result"),
    path('result/<int:pk>', AdaptationResultView.as_view(), name="adaptation_result_admin"),
    path('basic_pdf', AdaptationBasicPDFView.as_view(), name="adaptation_basic_pdf"),
    path('complex_pdf', AdaptationComplexPDFView.as_view(), name="adaptation_complex_pdf"),

    path('adaptation_list/', AdaptationList.as_view(), name="adaptation_list"),
    path('<int:id>/confirmation', AdaptationConfirmationView.as_view(), name="adaptation_confirmation"),
    path('api/', include('adaptation.api.urls')),
]