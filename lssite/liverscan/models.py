from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor')
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birthday = models.DateField()
    user_type = models.CharField(max_length=7)
    patient_id = models.CharField(max_length=50, unique=True, blank=True)  # Allow blank since we'll autogenerate it

    def save(self, *args, **kwargs):
        # Generate base patient_id
        base_patient_id = (self.first_name.lower().strip() + self.last_name.lower().strip() + 
                           self.birthday.strftime('%m%d%y'))

        # Initialize temporary patient_id
        temp_patient_id = base_patient_id
        counter = 1

        # Check for collisions and update temp_patient_id if necessary
        while User.objects.filter(patient_id=temp_patient_id, user_type="patient").exists():
            # Append a counter to make it unique
            temp_patient_id = f"{base_patient_id}_{counter}"
            counter += 1

        # Set the unique patient_id
        self.patient_id = temp_patient_id

        # Call the original save() method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.patient_id})"


class Diagnosis(models.Model):
    DIAGNOSIS_CHOICES = [
        ('abscess', 'Abscess'),
        ('cyst', 'Cyst'),
        ('tumor', 'Tumor'),
        ('none', 'None'),
    ]

    patient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='diagnoses')  # Linking to Patient
    doctor_assigned = models.ForeignKey(User, on_delete=models.PROTECT)
    
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