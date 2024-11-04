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
    print(request.user)

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
