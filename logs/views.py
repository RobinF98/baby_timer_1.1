# from turtle import update
# from typing import Any
# from urllib import request
from django import forms
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput, TimePickerInput
from django.core.exceptions import ValidationError
# from requests import options
from operator import attrgetter
from itertools import chain
from .models import Baby, Diaper, Sleep

# Create your views here.


class BabyListView(LoginRequiredMixin, generic.ListView):
    model = Baby
    template_name = "logs/index.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class BabyDetailView(generic.detail.DetailView):
    model = Baby

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baby_list"] = Baby.objects.filter(user=self.object.user.id)
        return context


class BabyCreateView(generic.edit.CreateView):
    # set user field to current user

    model = Baby
    template_name = "logs/generic_form.html"

    fields = [
        "baby_name",
        "birthday",
        "due_date",
        "notes",
    ]

    def get_form(self):
        form = super().get_form()
        form.fields["birthday"].widget = DatePickerInput()
        form.fields["due_date"].widget = DatePickerInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_baby"] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(reverse("home"))


class BabyUpdateView(generic.edit.UpdateView):
    model = Baby
    template_name = "logs/generic_form.html"

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

    def get_initial(self):
        initial = super(BabyUpdateView, self).get_initial()

        # retrieve current object
        baby_object = self.get_object()

        initial["baby_name"] = baby_object.baby_name
        initial["birthday"] = baby_object.birthday
        initial["due_date"] = baby_object.due_date
        return initial

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("home"))


class BabyDeleteView(generic.edit.DeleteView):
    model = Baby
    template_name = "baby_detail.html"
    success_url = "/"


class LogsView(generic.ListView, View):
    model = Baby
    template_name = "logs/logs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["diapers"] = Diaper.objects.filter(baby_id=self.kwargs["pk"])
        context["sleeps"] = Sleep.objects.filter(baby_id=self.kwargs["pk"])
        context["baby"] = Baby.objects.filter(id=self.kwargs["pk"])[0]
        # merge diapers and sleeps into 1 entry:
        context["logs_list"] = sorted(
            chain(context["sleeps"], context["diapers"]),
            key=attrgetter("time"),
            reverse=True
        )
        return context


class DiaperCreateView(generic.CreateView):
    model = Diaper
    template_name = "logs/generic_form.html"
    fields = [
        "time",
        "type",
        "notes",
    ]

    def get_form(self):
        form = super().get_form()
        form.fields["time"].widget = DateTimePickerInput()
        return form

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["baby_list"] = Baby.objects.filter(user=self.object.user.id)
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baby"] = Baby.objects.filter(id=self.kwargs["pk"])[0]
        return context

    def form_valid(self, form):
        form.instance.baby_id = self.kwargs["pk"]
        form.save()
        return HttpResponseRedirect(reverse("logs", args=[form.instance.baby_id]))


class DiaperUpdateView(generic.edit.UpdateView):
    model = Diaper
    template_name = "logs/generic_form.html"
    fields = [
        "time",
        "type",
        "notes",
    ]

    def get_form(self):
        form = super().get_form()
        form.fields["time"].widget = DateTimePickerInput()
        return form

    def get_initial(self):
        initial = super(DiaperUpdateView, self).get_initial()

        # retrieve current object
        diaper_object = self.get_object()

        initial["type"] = diaper_object.type
        initial["time"] = diaper_object.time
        initial["notes"] = diaper_object.notes
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_view"] = True
        context["baby"] = Baby.objects.filter(id=self.object.baby.id)[0]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("logs", args=[form.instance.baby_id]))


class DiaperDeleteView(generic.edit.DeleteView):
    model = Diaper
    template_name = "logs/generic_form.html"

    def get_success_url(self, **kwargs):
        return reverse("logs", args=[self.object.baby_id])


class SleepCreateView(generic.CreateView):
    model = Sleep
    template_name = "logs/generic_form.html"
    fields = [
        "time",
        "end_time",
        "notes",
    ]

    class Meta:
        model = Sleep
        fields = [
            "time",
            "end_time",
            "notes",
            # "duration",
        ]

    def get_form(self):
        form = super().get_form()
        form.fields["time"].widget = DateTimePickerInput()
        form.fields["end_time"].widget = DateTimePickerInput()
        # TODO SET THE BELOW TO WHAT IT NEEDS TO BE I GUESS - SLEEP DURATION THING SO DATE TIME FIELD WITH TIME WIDGET?
        # form.fields["duration"] = forms.DurationField(required=False, disabled=True)
        # form.fields["duration"].widget = TimePickerInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baby"] = Baby.objects.filter(id=self.kwargs["pk"])[0]
        return context

    def form_valid(self, form):

        # custom validation - check end time is after start time
        if form.cleaned_data["time"] > form.cleaned_data["end_time"]:
            form.add_error("end_time", "End time cannot be before start time")
            return self.form_invalid(form)

        # set baby for diaper
        form.instance.baby_id = self.kwargs["pk"]
        form.save()
        return HttpResponseRedirect(reverse("logs", args=[form.instance.baby_id]))


class SleepUpdateView(generic.UpdateView):
    model = Sleep
    template_name = "logs/generic_form.html"
    fields = [
        "time",
        "end_time",
        "notes",
    ]

    class Meta:
        model = Sleep
        fields = [
            "time",
            "end_time",
            "notes",
            # "duration",
        ]

    def get_form(self):
        form = super().get_form()
        form.fields["end_time"] = forms.DateTimeField()

        form.fields["time"].widget = DateTimePickerInput()
        form.fields["end_time"].widget = DateTimePickerInput()
        # TODO SET THE BELOW TO WHAT IT NEEDS TO BE I GUESS - SLEEP DURATION THING SO DATE TIME FIELD WITH TIME WIDGET?
        # form.fields["duration"] = forms.DurationField(required=False, disabled=True)
        # form.fields["duration"].widget = TimePickerInput()
        return form

    def get_initial(self):
        initial = super(SleepUpdateView, self).get_initial()

        # retrieve current object
        sleep_object = self.get_object()

        initial["time"] = sleep_object.time
        initial["end_time"] = sleep_object.end_time
        # initial["duration"] = sleep_object.end_time - sleep_object.time
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baby"] = Baby.objects.filter(id=self.object.baby.id)[0]
        context["edit_view"] = True
        return context

    def form_valid(self, form):

        # custom validation - check end time is after start time
        if form.cleaned_data["time"] > form.cleaned_data["end_time"]:
            form.add_error("end_time", "End time cannot be before start time")
            return self.form_invalid(form)

        form.save()
        return HttpResponseRedirect(reverse("logs", args=[form.instance.baby_id]))
