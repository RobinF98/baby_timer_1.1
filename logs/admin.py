from django.contrib import admin
from .models import Baby, Diaper, Sleep, Feed, Medication, MedicationEntry

# Register your models here.

admin.site.register(Baby)
admin.site.register(Diaper)
admin.site.register(Sleep)
admin.site.register(Feed)
admin.site.register(Medication)
admin.site.register(MedicationEntry)
