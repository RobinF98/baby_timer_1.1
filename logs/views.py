from pyexpat import model
from turtle import update
from typing import Any
from urllib import request
from django import forms
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput
from requests import options
from .models import Baby
# Create your views here.


class BabyListView(LoginRequiredMixin, generic.ListView):
    model = Baby
    template_name = 'logs/index.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class BabyDetailView(generic.detail.DetailView):
    model = Baby


class BabyCreateView(generic.edit.CreateView):
    # set user field to current user

    model = Baby
    fields = [
        "baby_name",
        "birthday",
        "due_date",
    ]

    def get_form(self):
        form = super().get_form()
        form.fields["birthday"].widget = DatePickerInput()
        form.fields["due_date"].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        baby = form.save()
        return HttpResponseRedirect(reverse("home"))


class BabyUpdateView(generic.edit.UpdateView, BabyCreateView):
    model = Baby

    def get_initial(self):
        initial = super(BabyUpdateView, self).get_initial()
        print('initial data', initial)

        # retrieve current object
        baby_object = self.get_object()

        initial['baby_name'] = baby_object.baby_name
        initial['birthday'] = baby_object.birthday
        initial['due_date'] = baby_object.due_date
        return initial
