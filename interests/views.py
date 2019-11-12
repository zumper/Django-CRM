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
                                  TemplateView, View)

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
from leads.forms import (LeadAttachmentForm, LeadCommentForm, LeadForm,
                         LeadListForm)
from leads.models import Lead
from leads.tasks import (create_lead_from_file, send_email_to_assigned_user,
                         send_lead_assigned_emails, update_leads_cache)
from planner.forms import ReminderForm
from planner.models import Event, Reminder
from teams.models import Teams
from django.core.cache import cache


class InterestDetailView(SalesAccessRequiredMixin, LoginRequiredMixin, DetailView):
  model = Interest
  context_object_name = 'interest_record'
  template_name = 'view_interests.html'

  def get_queryset(self):
    queryset = super(InterestDetailView, self).get_queryset()
    queryset = queryset.prefetch_related('building', 'contact', 'lead', 'listing', 'opportunity', 'matching_team')
    return queryset
