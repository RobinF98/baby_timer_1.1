from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import baby
# Create your views here.


class BabyList(generic.ListView):
    model = baby
    template_name = 'logs/index.html'

    def get_queryset(self):
        return baby.objects.filter(user=self.request.user)

# class BabyCreate(generic.edit.CreateView):
#     model = baby
