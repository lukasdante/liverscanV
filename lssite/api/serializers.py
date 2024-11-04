from rest_framework import serializers
from liverscan.models import CustomUser, Diagnosis

# serializer for Audit Reports
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'role'
        ]

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = [
            'id', 'patient_id', 'status', 'doctor_assigned', 'patient_initials',
            'birthday', 'diagnosis_date', 'unenhanced_ct', 'arterial_ct',
            'portal_venous_ct', 'initial_diagnosis', 'confidence', 'area',
            'remarks', 'final_diagnosis'
        ]