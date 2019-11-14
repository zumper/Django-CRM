# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# views for building model

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View, UpdateView)

from accounts.models import Account, Tags
from buildings.forms import BuildingForm
from buildings.models import Building
from common import status
from common.access_decorators_mixins import (MarketingAccessRequiredMixin,
                                             SalesAccessRequiredMixin,
                                             marketing_access_required,
                                             sales_access_required)
from common.forms import BillingAddressForm
from common.models import APISettings, Attachments, Comment, User
from common.tasks import send_email_user_mentions
from common.utils import COUNTRIES, LEAD_SOURCE, LEAD_STATUS
from contacts.models import Contact
from interests.models import Interest
from interests.forms import InterestForm
from leads.forms import (LeadAttachmentForm, LeadCommentForm, LeadForm,
                         LeadListForm)
from leads.models import Lead
from leads.tasks import (create_lead_from_file, send_email_to_assigned_user,
                         send_lead_assigned_emails, update_leads_cache)
from planner.forms import ReminderForm
from planner.models import Event, Reminder
from teams.models import Teams
from django.core.cache import cache


class BuildingDetailView(SalesAccessRequiredMixin, LoginRequiredMixin, DetailView):
  model = Building
  context_object_name = 'building_record'
  template_name = 'buildings.html'

  def get_queryset(self):
    queryset = super(BuildingDetailView, self).get_queryset()
    queryset = queryset.prefetch_related('interests', 'listings',)
    return queryset


class BuildingListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
  model = Building
  context_object_name = "building_obj_list"
  template_name = "buildings.html"

  def get_queryset(self):
    queryset = self.model.objects.all()
    if (self.request.user.role != "ADMIN" and not
    self.request.user.is_superuser):
      queryset = queryset.filter(
        Q(assigned_to__in=[self.request.user]) |
        Q(created_by=self.request.user))

    request_post = self.request.POST
    if request_post:
      if request_post.get('building'):
        queryset = queryset.filter(
          building__city__icontains=request_post.get('building'))
      if request_post.get('phone'):
        queryset = queryset.filter(
          phone__icontains=request_post.get('phone'))
      if request_post.get('email'):
        queryset = queryset.filter(
          email__icontains=request_post.get('email'))
    return queryset.distinct()

  def get_context_data(self, **kwargs):
    context = super(BuildingListView, self).get_context_data(**kwargs)
    context["building_obj_list"] = self.get_queryset()
    context["per_page"] = self.request.POST.get('per_page')
    search = True if (
        self.request.POST.get('phone') or
        self.request.POST.get('email') or
        self.request.POST.get('listing')
    ) else False

    context["search"] = search
    return context

  def post(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    return self.render_to_response(context)


class CreateBuildingView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = "create_building.html"

    def post(self, request, *args, **kwargs):
      self.object = None
      form = self.get_form()
      address_form = BillingAddressForm(request.POST)
      if form.is_valid() and address_form.is_valid():
        address_obj = address_form.save()
        building_obj = form.save(commit=False)
        building_obj.address = address_obj
        building_obj.created_by = self.request.user
        building_obj.save()
        return self.form_valid(form)

      return self.form_invalid(form)

    def get_context_data(self, **kwargs):
      context = super(CreateBuildingView, self).get_context_data(**kwargs)
      context["building_form"] = context["form"]
      if "address_form" in kwargs:
        context["address_form"] = kwargs["address_form"]
      else:
        if self.request.POST:
          context["address_form"] = BillingAddressForm(self.request.POST)
        else:
          context["address_form"] = BillingAddressForm()
      return context


class UpdateBuildingView(SalesAccessRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = "create_building.html"

    def post(self, request, *args, **kwargs):
      self.object = None
      form = self.get_form()
      address_form = BillingAddressForm(request.POST)
      if form.is_valid() and address_form.is_valid():
        address_obj = address_form.save()
        building_obj = form.save(commit=False)
        building_obj.address = address_obj
        building_obj.created_by = self.request.user
        building_obj.save()
        return self.form_valid(form)

      return self.form_invalid(form)

    def get_context_data(self, **kwargs):
      context = super(UpdateBuildingView, self).get_context_data(**kwargs)
      context["building_obj"] = self.object
      context["building_form"] = context["form"]
      return context


class RemoveBuildingView(SalesAccessRequiredMixin, LoginRequiredMixin, View):

  def get(self, request, *args, **kwargs):
    return self.post(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    contact_id = kwargs.get("pk")
    self.object = get_object_or_404(Contact, id=contact_id)
    if (self.request.user.role != "ADMIN" and not
    self.request.user.is_superuser and
        self.request.user != self.object.created_by):
      raise PermissionDenied
    else:
      if self.object.address_id:
        self.object.address.delete()
      self.object.delete()
      if self.request.is_ajax():
        return JsonResponse({'error': False})
      return redirect("buildings:list")
