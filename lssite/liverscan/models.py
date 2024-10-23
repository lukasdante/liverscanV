from django.db import models
from django.contrib.auth.models import AbstractUser

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

    patient = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='diagnoses')  # Linking to Patient
    doctor_assigned = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    
    unenhanced_ct = models.ImageField(upload_to='ct_scans/unenhanced/')
    arterial_ct = models.ImageField(upload_to='ct_scans/arterial/')
    portal_venous_ct = models.ImageField(upload_to='ct_scans/portal_venous/')
    initial_diagnosis = models.CharField(max_length=7, choices=DIAGNOSIS_CHOICES)
    date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    area_of_focal_liver_lesion = models.DecimalField(max_digits=5, decimal_places=2)  # In cm²
    final_diagnosis = models.CharField(max_length=7, choices=DIAGNOSIS_CHOICES)


    def __str__(self):
        return f"Diagnose: {self.patient.first_name} {self.patient.last_name} - {self.initial_diagnosis}"