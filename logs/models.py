from email.policy import default
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

# Create your models here.


class Baby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baby_name = models.CharField("baby's name", max_length=50, blank=False,)
    birthday = models.DateField(("birthday"), blank=False,)
    due_date = models.DateField("predicted due date",blank=False,)

    def __str__(self):
        return self.baby_name

    class Meta:
        ordering = ["baby_name"]


class Diaper(models.Model):
    DIAPER_TYPE_CHOICES = {
        "WT": "Wet",
        "DY": "Dirty",
        "WD": "Wet and Dirty"
    }
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE,)
    time = models.DateTimeField(auto_now_add=True, blank=False,)
    type = models.CharField(
        max_length=2,
        choices=DIAPER_TYPE_CHOICES,
        default="WT",
        blank=False,
        )
    notes = models.TextField(blank=True,)


class Sleep(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE,)
    start_time = models.DateTimeField("Sleep start time", auto_now_add=True, blank=False,)
    end_time = models.DateTimeField("Sleep end time", blank=False,)
    notes = models.TextField(blank=True,)


class Feed(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE,)
    start_time = models.DateTimeField("Feed start time", auto_now_add=True, blank=False,)
    end_time = models.DateTimeField("Feed end time", blank=False,)