from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from bootstrap_datepicker_plus.widgets import (
                                                DateTimePickerInput,
                                                DatePickerInput
    )
from operator import attrgetter
from itertools import chain
from .models import Baby, Diaper, Sleep

# Create your views here.
    

class UserAccessMixin(LoginRequiredMixin, UserPassesTestMixin,
                      SingleObjectMixin):
    """
        Prevents users from accessing babies and baby logs that are not
        registered to them.
    """
    def test_func(self):
        # check logged in User is the User who created the current Baby:
        if self.model.__name__ != "Baby":
            return self.request.user == self.get_object().baby.user
        return self.request.user == self.get_object().user

    def handle_no_permission(self):
        return redirect("/")


class BabyListView(LoginRequiredMixin, generic.ListView):
    model = Baby
    template_name = "logs/index.html"

    # only list babies registered to current user
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class BabyDetailView(UserAccessMixin, generic.detail.DetailView,):
    model = Baby

    # get all babies under current user ID for nav logs dropdown
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baby_list"] = Baby.objects.filter(user=self.object.user.id)
        return context


class BabyCreateView(LoginRequiredMixin, generic.edit.CreateView):
    # set user field to current user

    model = Baby
    template_name = "logs/generic_form.html"

    fields = [
        "baby_name",
        "birthday",
        "due_date",
        "notes",
    ]

    # set 3rd party form widgets for date/time selection
    def get_form(self):
        form = super().get_form()
        form.fields["birthday"].widget = DatePickerInput()
        form.fields["due_date"].widget = DatePickerInput()
        return form

    # add_baby boolean controls form button selection
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_baby"] = True
        return context

    def form_valid(self, form):
        # set baby user
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(reverse("home"))


class BabyUpdateView(UserAccessMixin, generic.edit.UpdateView):
    model = Baby
    template_name = "logs/generic_form.html"

    fields = [
        "baby_name",
        "birthday",
        "due_date",
    ]

    # 3rd party widgets for date/time selection
    def get_form(self):
        form = super().get_form()
        form.fields["birthday"].widget = DatePickerInput()
        form.fields["due_date"].widget = DatePickerInput()
        return form

    def get_initial(self):
        initial = super(BabyUpdateView, self).get_initial()

        # retrieve current baby
        baby_object = self.get_object()

        initial["baby_name"] = baby_object.baby_name
        initial["birthday"] = baby_object.birthday
        initial["due_date"] = baby_object.due_date
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_view"] = True
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("home"))


class BabyDeleteView(UserAccessMixin, generic.edit.DeleteView):
    model = Baby
    template_name = "baby_detail.html"
    success_url = "/"


class LogsView(UserAccessMixin, generic.ListView, View):
    model = Baby
    template_name = "logs/logs.html"

    # context inludes all diapers / sleeps registered to current baby
    def get_context_data(self, **kwargs):
        context = {}
        context["diapers"] = Diaper.objects.filter(baby_id=self.kwargs["pk"])
        context["sleeps"] = Sleep.objects.filter(baby_id=self.kwargs["pk"])
        context["baby"] = Baby.objects.filter(id=self.kwargs["pk"])[0]
        # merge diapers and sleeps into 1 list, sorted by time since entry:
        context["logs_list"] = sorted(
            chain(context["sleeps"], context["diapers"]),
            key=attrgetter("time"),
            reverse=True
        )
        return context


class DiaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diaper
    template_name = "logs/generic_form.html"
    fields = [
        "time",
        "type",
        "notes",
    ]

    # 3rd party date/time selector widgets
    def get_form(self):
        form = super().get_form()
        form.fields["time"].widget = DateTimePickerInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baby"] = Baby.objects.filter(id=self.kwargs["pk"])[0]
        return context

    def form_valid(self, form):
        # get current baby from url
        form.instance.baby_id = self.kwargs["pk"]
        form.save()
        return HttpResponseRedirect(reverse("logs",
                                            args=[form.instance.baby_id]))


class DiaperUpdateView(UserAccessMixin, generic.edit.UpdateView):
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

    # edit_view controls form buttons selection
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_view"] = True
        context["baby"] = Baby.objects.filter(id=self.object.baby.id)[0]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("logs",
                                            args=[form.instance.baby_id]))


class DiaperDeleteView(UserAccessMixin, generic.edit.DeleteView):
    model = Diaper
    template_name = "logs/generic_form.html"

    def get_success_url(self, **kwargs):
        return reverse("logs", args=[self.object.baby_id])


class SleepCreateView(LoginRequiredMixin, generic.CreateView):
    model = Sleep
    template_name = "logs/generic_form.html"
    fields = [
        "time",
        "end_time",
        "notes",
    ]

    # 3rd party date/time picker widgets
    def get_form(self):
        form = super().get_form()
        form.fields["time"].widget = DateTimePickerInput()
        form.fields["end_time"].widget = DateTimePickerInput()
        form.fields["notes"].widget.attrs.update(cols=20, rows=5)
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
        return HttpResponseRedirect(reverse("logs",
                                            args=[form.instance.baby_id]))


class SleepUpdateView(UserAccessMixin, generic.UpdateView):
    model = Sleep
    template_name = "logs/generic_form.html"
    fields = [
        "time",
        "end_time",
        "notes",
    ]

    def get_form(self):
        form = super().get_form()
        form.fields["end_time"] = forms.DateTimeField()
        form.fields["time"].widget = DateTimePickerInput()
        form.fields["end_time"].widget = DateTimePickerInput()
        form.fields["notes"].widget.attrs.update(cols=20, rows=5)
        return form

    def get_initial(self):
        initial = super(SleepUpdateView, self).get_initial()

        # retrieve current object
        sleep_object = self.get_object()

        initial["time"] = sleep_object.time
        initial["end_time"] = sleep_object.end_time
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
        return HttpResponseRedirect(reverse("logs",
                                            args=[form.instance.baby_id]))


class SleepDeleteView(UserAccessMixin, generic.edit.DeleteView):
    model = Sleep
    template_name = "logs/generic_form.html"

    def get_success_url(self, **kwargs):
        return reverse("logs", args=[self.object.baby_id])
