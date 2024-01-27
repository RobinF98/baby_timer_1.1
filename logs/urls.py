from . import views
from django.urls import path

urlpatterns = [
    path("", views.BabyList.as_view(), name="home"),
]
