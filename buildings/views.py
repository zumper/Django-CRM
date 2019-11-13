# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# views for interest model

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
from common import status
from common.access_decorators_mixins import (MarketingAccessRequiredMixin,
                                             SalesAccessRequiredMixin,
                                             marketing_access_required,
                                             sales_access_required)
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
  model = Interest
  context_object_name = 'building_record'
  template_name = 'buildings.html'

  def get_queryset(self):
    queryset = super(BuildingDetailView, self).get_queryset()
    queryset = queryset.prefetch_related('building', 'contact', 'lead', 'listing', 'opportunity', 'matching_team')
    return queryset


class BuildingsListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
  model = Interest
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
    context = super(BuildingsListView, self).get_context_data(**kwargs)
    context["building_obj_list"] = self.get_queryset()
    context["per_page"] = self.request.POST.get('per_page')
    search = False
    if (
        self.request.POST.get('phone') or
        self.request.POST.get('email') or
        self.request.POST.get('building')
    ):
      search = True
    context["search"] = search
    return context

  def post(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    return self.render_to_response(context)


class CreateBuildingView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
    model = Interest
    form_class = InterestForm
    template_name = "create_interest.html"

    def get_context_data(self, **kwargs):
      context = super(CreateBuildingView, self).get_context_data(**kwargs)
      context["interest_form"] = context["form"]
      return context


class UpdateBuildingView(SalesAccessRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Interest
    form_class = InterestForm
    template_name = "create_interest.html"

    def get_context_data(self, **kwargs):
      context = super(UpdateBuildingView, self).get_context_data(**kwargs)
      context["interest_obj"] = self.object
      context["interest_form"] = context["form"]
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
