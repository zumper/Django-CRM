# Copyright 2019 Zumper Inc.
# Author: Akshay Chandramouli (akshay@zumper.com)
#

from django.contrib.postgres import fields as pg_fields
from django.db import models

from common.enums import Features
from accounts.models import Account


class Deal(models.Model):
  """Model definition for Deal"""

  account_id = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='deals')

  created_on = models.DateTimeField(auto_now_add=True)
  last_modified_on = models.DateTimeField(auto_now=True)
  start_on = models.DateTimeField(null=True, blank=True)
  end_on = models.DateTimeField(null=True, blank=True)

  zumper_id = models.BigIntegerField(db_index=True, unique=True, null=True)
  zumper_agent_ids = pg_fields.ArrayField(models.BigIntegerField(), null=True, blank=True)
  zumper_building_ids = pg_fields.ArrayField(models.BigIntegerField(), null=True, blank=True)
  zumper_listing_ids = pg_fields.ArrayField(models.BigIntegerField(), null=True, blank=True)
  zumper_brokerage_ids = pg_fields.ArrayField(models.BigIntegerField(), null=True, blank=True)

  features = models.BigIntegerField(choices=Features.choices(), blank=True)
  feed_names = pg_fields.ArrayField(models.TextField(), null=True, blank=True)
  flat_revenue = models.IntegerField(null=True, blank=True)
  flat_revenue_per = models.IntegerField(null=True, blank=True)
  lead_revenue = models.IntegerField(null=True, blank=True)
  lead_revenue_cap = models.IntegerField(null=True, blank=True)
  lead_revenue_cap_per = models.IntegerField(null=True, blank=True)
  name = models.CharField(unique=True, max_length=128)
  opportunity_id = models.CharField(null=True, blank=True, max_length=128)
  rank = models.FloatField(null=True, blank=True)
  type = models.TextField(null=True, blank=True)
