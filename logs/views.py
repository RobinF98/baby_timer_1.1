from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Baby
# Create your views here.


class BabyListView(generic.ListView):
    model = Baby
    template_name = 'logs/index.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

# class BabyCreate(generic.edit.CreateView):
#     model = baby


class BabyDetailView(generic.detail.DetailView):
    model = Baby
