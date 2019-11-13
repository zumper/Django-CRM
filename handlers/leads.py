# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# leads handler

import datetime

from leads.models import Lead
from common.models import User

_CYCLE_DAYS = 60
_RENTER = 'Renter'


def get_lead_for_interest(interest, first_name, last_name):
  query = None
  if interest.email:
    query = Lead.objects.filter(email=interest.email)
  elif interest.phone:
    query = Lead.objects.filter(phone=interest.phone)

  # at this point we don't have enough info to create the lead properly
  if not query:
    return

  lead = query.filter(is_active=True).prefetch_related('interests').first()
  if lead and lead.interests:
    most_recent_intent_dt = lead.interests[0].created_on
    date_diff = datetime.datetime.now().date() - most_recent_intent_dt
    if date_diff < _CYCLE_DAYS:
      return lead

  assigned = User.objects.first()

  new_lead = Lead.objects.create(
      title=_RENTER,
      first_name=first_name,
      last_name=last_name,
      phone=interest.phone,
      status=None,
      # TODO(tetsuji): we can't just assign to the first user...
  )
  new_lead.assigned_to.add(assigned)
  new_lead.save()

  return new_lead
