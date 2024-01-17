from email.policy import default
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

# Create your models here.


class baby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baby_name = models.CharField("baby's name", max_length=50)
    birthday = models.DateField(("birthday"))
    due_date = models.DateField("predicted due date")

    def __str__(self):
        return self.baby_name

    class Meta:
        ordering = ["baby_name"]


class diaper(models.Model):
    DIAPER_TYPE_CHOICES = {
        "WT": "Wet",
        "DY": "Dirty",
        "WD": "Wet and Dirty" 
    }
    baby = models.ForeignKey(baby, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=2,
        choices=DIAPER_TYPE_CHOICES,
        default="WT",
        )
    notes = models.TextField()
