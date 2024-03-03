from . import views
from django.urls import path

urlpatterns = [
    path("", views.BabyListView.as_view(), name="home"),
    path("baby/<int:pk>", views.BabyDetailView.as_view(), name="baby-detail"),
    path("add_baby", views.BabyCreateView.as_view(), name="add-baby"),
    path("edit_baby/<int:pk>", views.BabyUpdateView.as_view(), name="edit-baby"),
    path("delete_baby/<int:pk>", views.BabyDeleteView.as_view(), name="delete-baby"),
    path("logs/<int:pk>", views.LogsView.as_view(), name="logs"),
    path("logs/<int:pk>/diaper", views.DiaperCreateView.as_view(), name="add-diaper"),
    path("logs/edit_diaper/<int:pk>", views.DiaperUpdateView.as_view(), name="edit-diaper"),
    path("logs/<int:pk>/sleep", views.SleepCreateView.as_view(), name="add-sleep"),
    path("logs/delete_diaper/<int:pk>", views.DiaperDeleteView.as_view(), name="delete-object"),
    path("logs/edit_sleep/<int:pk>",views.SleepUpdateView.as_view(), name="edit-sleep")
]
