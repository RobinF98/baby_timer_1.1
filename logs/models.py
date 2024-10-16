from email.policy import default
from random import choices
from urllib import request
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User, Permission
from datetime import datetime
# Create your models here.


class Baby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False,)
    baby_name = models.CharField("baby's name", max_length=50, blank=False,)
    birthday = models.DateField(("birthday"), blank=False,)
    due_date = models.DateField("predicted due date", blank=False,)
    notes = models.TextField(blank=True,)
    

    def __str__(self):
        return self.baby_name

    class Meta:
        ordering = ["baby_name"]
        permissions = [
            ("can_view", "Can view baby details")
        ]

    def addPermission(self):
        User.user_permissions.add(Permission.objects.get(codename="can_view"))
        # add user permissions to view the baby details here


class Diaper(models.Model):
    DIAPER_TYPE_CHOICES = {
        "WT": "Wet",
        "DY": "Dirty",
        "WD": "Wet and Dirty"
    }
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, blank=False)
    time = models.DateTimeField(default=datetime.now, blank=False)
    type = models.CharField(
        choices=DIAPER_TYPE_CHOICES,
        default="WT",
        blank=False,
        max_length=10
        )
    notes = models.TextField(blank=True,)


class Sleep(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, blank=False,)
    time = models.DateTimeField("Sleep start time", default=datetime.now, blank=False,)
    end_time = models.DateTimeField("Sleep end time", blank=False,)
    notes = models.TextField(blank=True,)


class Feed(models.Model):
    FEED_TYPE_CHOICES = {
        "Breast": {
            "LB": "Left Breast",
            "RB": "Right Breast",
        },
        "FO": "Formula",
        "SF": "Solid Food",
    }
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, blank=False,)
    start_time = models.DateTimeField("Feed start time", auto_now_add=True, blank=False,)
    end_time = models.DateTimeField("Feed end time", blank=False,)
    type = models.CharField(
        choices=FEED_TYPE_CHOICES,
        default="LB",
        blank=False,
        max_length=10,
    )
    notes = models.TextField(blank=True,)


class Medication(models.Model):
    MED_UNIT_CHOICES = {
        "g": "grams",
        "ml": "millitres",
        "oz": "ounces",
        "fl oz": "fluid ounces",
        "dp": "drops"
    }
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE,)
    med_name = models.CharField("medication", max_length=50, blank=False)
    default_dose = models.PositiveIntegerField(blank=True)
    dose_unit = models.CharField(choices=MED_UNIT_CHOICES, default="ml", blank=True, max_length=10,)
    notes = models.TextField(blank=True,)

    def __str__(self):
        return self.med_name


class MedicationEntry(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, blank=False,)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, blank=False,)
    time = models.DateTimeField(auto_now_add=True, blank=False,)
    notes = models.TextField(blank=True,)
