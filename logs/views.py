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

    # def get_success_url(self):
    # #     return HttpResponseRedirect(reverse("home"))
    # def post(self, request):
    #     baby = BabyCreateView.save()
    #     return HttpResponseRedirect(reverse("home"))
