# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

from buildings.models import Building
from common.enums import Features, InternalFeatures, PropertyStatus, Syndications
from common.models import Address, User
from accounts.models import Account
from deals.models import Deal
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams


class Listing(models.Model):
  """Model definition for Listing."""

  account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='listings', null=True)
  address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='listings', null=True)
  building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='listings', null=True)
  deals = models.ForeignKey(Deal, on_delete=models.SET_NULL, related_name='listings', null=True)
  teams = models.ManyToManyField(Teams, related_name='listings')

  created_on = models.DateTimeField(auto_now_add=True)
  last_modified_on = models.DateTimeField(auto_now=True)
  listed_on = models.DateTimeField(blank=True, null=True)

  zumper_id = models.BigIntegerField(db_index=True, unique=True, null=True)
  zumper_agent_id = models.BigIntegerField(null=True)
  zumper_brokerage_id = models.BigIntegerField(null=True)

  agent_email = models.CharField(_('Agent Email'), null=True, blank=True, max_length=256)
  bathrooms = models.IntegerField(null=True, blank=True)
  bedrooms = models.IntegerField(null=True, blank=True)
  brokerage_name = models.CharField(_('Brokerage Name'), null=True, blank=True, max_length=256)
  brokerage_key = models.CharField(_('Brokerage Key'), null=True, blank=True, max_length=256)
  capped = models.BooleanField(default=False)
  contact_email = models.EmailField(max_length=256, null=True, blank=True)
  contact_phone = PhoneNumberField(null=True, blank=True)
  description = models.TextField(blank=True, null=True)
  email_override = models.CharField(_('Email Override'), null=True, blank=True, max_length=256)
  features = models.BigIntegerField(choices=Features.choices(), blank=True)
  feed_name = models.CharField(max_length=128, blank=True, null=True)
  internal_features = models.BigIntegerField(choices=InternalFeatures.choices(), blank=True)
  listing_status = models.IntegerField(choices=PropertyStatus.choices(), default=PropertyStatus.UNKNOWN)
  listing_title = models.CharField(_('Listing Title'), max_length=128)
  min_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
  max_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
  notes = models.TextField(blank=True, null=True)
  syndications = models.BigIntegerField(choices=Syndications.choices(), blank=True)
