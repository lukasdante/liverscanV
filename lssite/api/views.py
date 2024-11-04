from rest_framework import generics
from .serializers import CustomUserSerializer, DiagnosisSerializer
from liverscan.models import CustomUser, Diagnosis

# serializer view for the entire list of Diagnoses
class CustomUserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class DiagnosisList(generics.ListCreateAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

# serializer view for a specific Audit Report instance
class DiagnosisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer