from django.urls import path
from .views import CustomUserList, DiagnosisList, DiagnosisDetail

urlpatterns = [
    path('users/', CustomUserList.as_view(), name='user_list'),
    path('diagnoses/', DiagnosisList.as_view(), name='diagnoses_list'),
    path('diagnoses/<int:pk>/', DiagnosisDetail.as_view(), name='diagnosis_detail'),
]