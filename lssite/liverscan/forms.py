from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Diagnosis
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

def create_request_diagnosis(request):
    """  Creates a Diagnosis instance given form data. """
    # required fields for all sources
    patient_initials = request.POST.get('initials')
    birthday = request.POST.get('birthday')
    doctor_assigned = request.user

    try:
        # create the report instance
        diagnosis = Diagnosis(
            patient_initials=patient_initials,
            birthday = birthday,
            doctor_assigned=doctor_assigned
        )

        diagnosis.save()

    # throw False when ValidationError occurs
    except ValidationError as e:
        return (False, e.messages)
    return (True, None)

def validate_diagnosis(request):
    """  Creates a Diagnosis instance given form data. """
    # required fields for all sources

    patient_id = request.POST.get('patient_id')
    final_diagnosis = request.POST.get('final_diagnosis')
    remarks = request.POST.get('remarks')

    print(request.POST)
    print(patient_id)
    print(final_diagnosis)
    print(remarks)

    diagnosis = Diagnosis.objects.filter(patient_id=patient_id)
    
    try:
        diagnosis = Diagnosis.objects.get(patient_id=patient_id)

        if diagnosis.final_diagnosis is None:
            diagnosis.final_diagnosis = final_diagnosis
        if diagnosis.remarks is None:
            diagnosis.remarks = remarks
        diagnosis.status = 3

        

        print("is this working chat?")

        diagnosis.save()

        return True, None

    except Diagnosis.DoesNotExist:
        return False, f"No Diagnosis found for the provided patient ID."
    except ValidationError as e:
        return False, e.messages