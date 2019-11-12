# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.enums import Features, InternalFeatures, PropertyStatus, Syndications
from common.models import Address, User
from accounts.models import Account
from deals.models import Deal
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams


class Building(models.Model):
  """Model definition for Building."""

  account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='buildings', null=True)
  address = models.ForeignKey(Address, related_name='buildings', on_delete=models.SET_NULL, null=True)
  deals = models.ForeignKey(Deal, on_delete=models.SET_NULL, related_name='buildings', null=True)
  teams = models.ManyToManyField(Teams, related_name='buildings')

  active_on = models.DateTimeField(blank=True, null=True)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified_on = models.DateTimeField(auto_now=True)

  zumper_id = models.BigIntegerField(db_index=True, unique=True, null=True)
  zumper_agent_id = models.BigIntegerField(null=True)
  zumper_brokerage_id = models.BigIntegerField(null=True)
  zumper_pb_id = models.BigIntegerField(db_index=True, null=True)

  agent_email = models.CharField(_('Agent Email'), null=True, blank=True, max_length=256)
  brokerage_name = models.CharField(_('Brokerage Name'), null=True, blank=True, max_length=256)
  brokerage_key = models.CharField(_('Brokerage Key'), null=True, blank=True, max_length=256)
  building_name = models.CharField(_('Building Name'), max_length=128)
  building_status = models.IntegerField(choices=PropertyStatus.choices(), default=PropertyStatus.UNKNOWN)
  capped = models.BooleanField(default=False)
  contact_email = models.EmailField(max_length=256, null=True, blank=True)
  contact_phone = PhoneNumberField(null=True, blank=True)
  description = models.TextField(blank=True, null=True)
  email_override = models.CharField(_('Email Override'), null=True, blank=True, max_length=256)
  feed_name = models.CharField(max_length=128, blank=True, null=True)
  features = models.BigIntegerField(choices=Features.choices(), blank=True)
  internal_features = models.BigIntegerField(choices=InternalFeatures.choices(), blank=True)
  notes = models.TextField(blank=True, null=True)
  syndications = models.BigIntegerField(choices=Syndications.choices(), blank=True)
