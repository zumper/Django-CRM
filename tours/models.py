# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

from django.db import models

from buildings.models import Building
from common.enums import AppointmentStatus
from events.models import Event
from listings.models import Listing
from opportunity.models import Opportunity


class Tours(models.Model):
  """Model definition for Team."""
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_tours', null=True)
  opportunities = models.ManyToManyField(Opportunity, related_name='tours')

  building = models.ForeignKey(Building, blank=True, null=True, on_delete=models.SET_NULL, related_name='tours')
  listing = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.SET_NULL, related_name='tours')

  created_on = models.DateTimeField(auto_now_add=True)
  last_modified_on = models.DateTimeField(auto_now=True)

  description = models.TextField(blank=True, null=True)
  end = models.DateTimeField()
  start = models.DateTimeField()
  status = models.IntegerField(choices=AppointmentStatus.choices(), default=AppointmentStatus.SCHEDULED)
