from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor')
    )

    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='patient')


class Diagnosis(models.Model):
    DIAGNOSIS_CHOICES = [
        ('abscess', 'Abscess'),
        ('cyst', 'Cyst'),
        ('tumor', 'Tumor'),
        ('none', 'None'),
    ]

    STATUS_CHOICES = [
        (1, "Input sent for prediction."),
        (2, "Prediction is ready."),
        (3, "Final diagnosis submitted."),
    ]

    # backend generated values
    patient_id = models.CharField(max_length=22)
    status = models.IntegerField(choices=STATUS_CHOICES)

    # foreign IDs
    doctor_assigned = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    
    # input data
    patient_initials = models.CharField(max_length=10)
    birthday = models.DateField()
    diagnosis_date = models.DateField()

    unenhanced_ct = models.ImageField(blank=True, null=True, upload_to='ct_scans/unenhanced/')
    arterial_ct = models.ImageField(blank=True, null=True, upload_to='ct_scans/arterial/')
    portal_venous_ct = models.ImageField(blank=True, null=True, upload_to='ct_scans/portal_venous/')
    
    # output of model
    initial_diagnosis = models.CharField(null=True, max_length=7, choices=DIAGNOSIS_CHOICES)
    confidence = models.DecimalField(null=True, max_digits=4, decimal_places=2)
    area = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    
    # finalization
    remarks = models.TextField(blank=True, null=True)
    final_diagnosis = models.CharField(blank=False, null=True, max_length=7, choices=DIAGNOSIS_CHOICES)

    def clean(self):
        # Ensure diagnosis date is not before birthday
        if self.diagnosis_date < self.birthday:
            raise ValidationError("Diagnosis date cannot be before the patient's birthday.")

    def save(self, *args, **kwargs):
        
        if not self.diagnosis_date:
            self.diagnosis_date = datetime.now().date()
        
        if isinstance(self.birthday, str):
            self.birthday = datetime.strptime(self.birthday, '%Y-%m-%d').date()
        if isinstance(self.diagnosis_date, str):
            self.diagnosis_date = datetime.strptime(self.diagnosis_date, '%Y-%m-%d').date()

        initials = self.patient_initials.upper()
        bday_formatted = self.birthday.strftime("%m%d%y")
        diagnosis_date_formatted = self.diagnosis_date.strftime("%m%d%y")
        self.patient_id = f"{initials}-{bday_formatted}-{diagnosis_date_formatted}"

        if not self.status:
            self.status = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Diagnose: {self.patient_id} - {self.initial_diagnosis}."