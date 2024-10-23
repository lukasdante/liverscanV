from django.contrib import admin
from .models import CustomUser, Diagnosis


# Register your models here.
admin.site.register(Diagnosis)
admin.site.register(CustomUser)