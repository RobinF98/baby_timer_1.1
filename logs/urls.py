from . import views
from django.urls import path

urlpatterns = [
    path("", views.BabyListView.as_view(), name="home"),
    path("baby/<int:pk>", views.BabyDetailView.as_view(), name="baby-detail"),
    path("add_baby", views.BabyCreateView.as_view(), name="add_baby")
]
