# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import Account
from buildings.models import Building
from common.enums import Features, InterestType, InternalFeatures, PropertyStatus, Syndications
from common.models import Address, User
from common.utils import CURRENCY_CODES
from contacts.models import Contact
from leads.models import Lead
from listings.models import Listing
from opportunity.models import Opportunity
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams


class Interest(models.Model):
  """Model definition for Interest."""

  building = models.ForeignKey(Building, on_delete=models.SET_NULL, related_name='interests', null=True)
  contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, related_name='interests', null=True)
  lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, related_name='interests', null=True)
  listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, related_name='interests', null=True)
  opportunity = models.ForeignKey(Opportunity, on_delete=models.SET_NULL, related_name='interests', null=True)
  matching_team = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='interests', null=True)

  created_on = models.DateTimeField(auto_now_add=True)
  last_modified_on = models.DateTimeField(auto_now=True)

  tracking_id = models.CharField(_('Tracking Id'), unique=True, null=True, max_length=256)
  agent_email = models.CharField(_('Agent Email'), null=True, blank=True, max_length=256)
  brokerage_key = models.CharField(_('Brokerage Key'), null=True, blank=True, max_length=256)
  brokerage_name = models.CharField(_('Brokerage Name'), null=True, blank=True, max_length=256)
  min_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
  max_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)

  # customer attributes
  availability_start = models.DateTimeField(blank=True, null=True)
  availability_end = models.DateTimeField(blank=True, null=True)
  budget = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
  clazz = models.CharField(_('Clazz'), blank=True, null=True, max_length=256)
  email = models.EmailField(max_length=256, null=True, blank=True)
  features = models.BigIntegerField(choices=Features.choices(), blank=True, null=True)
  message = models.TextField(null=True)
  move_in_date = models.DateField(blank=True, null=True)
  origin = models.TextField(blank=True, null=True)
  phone = PhoneNumberField(blank=True, null=True)


  class Meta:
    ordering = ['-created_on']
