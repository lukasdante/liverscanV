from django.contrib import admin
from .models import User, Diagnosis


# Register your models here.
admin.site.register(User)
admin.site.register(Diagnosis)