# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _

from buildings.models import Building
from common.enums import Features, InternalFeatures, PropertyStatus, Syndications
from common.models import Address, User
from common.utils import CURRENCY_CODES
from accounts.models import Account
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams


class LeadRoutes(models.Model):
  """Model definition for Lead Route."""

  team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='lead_routes', null=True)

  created_on = models.DateTimeField(auto_now_add=True)
  last_modified_on = models.DateTimeField(auto_now=True)

  agent_email = models.CharField(_('Agent Email'), null=True, blank=True, max_length=256)
  brokerage_key = models.CharField(_('Brokerage Key'), null=True, blank=True, max_length=256)
  description = models.TextField(blank=False, null=False)
  is_active = models.BooleanField(default=False)
  is_exclusive = models.NullBooleanField(null=True)
  name = models.CharField(_('Name'), max_length=128)
