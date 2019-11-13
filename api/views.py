# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from six import string_types

import json

from handlers import leads
from interests.models import Interest
from listings.models import Listing
from buildings.models import Building


class BaseApiView(APIView):

  _REQUIRED = {}

  def _get_body(self, request):
    unicode_body = request.body.decode('utf-8')
    return json.loads(unicode_body)

  def _validate_body(self, body):
    missing = list()
    for required in self._REQUIRED:
      if isinstance(required, (tuple, list, set, frozenset)):
        if all(body.get(sub_require) is None for sub_require in required):
          missing.append(required)
      elif body.get(required) is None:
        missing.append(required)
    if missing:
      raise ApiException('missing required fields', status_code=status.HTTP_400_BAD_REQUEST, missing=missing)

class InterestApiView(BaseApiView):

  _REQUIRED = frozenset(('first_name', 'last_name', 'tracking_id', 'min_price', 'clazz', ('email', 'phone',),))

  def post(self, request, *args, **kwargs):
    data = self._get_body(request)
    try:
      self._validate_body(data)
    except ApiException as e:
      return Response({'missing params': e.missing}, status=e.status_code)

    if self._exists(data['tracking_id']):
      return Response({'duplicate interest': data['tracking_id']}, status=status.HTTP_208_ALREADY_REPORTED)

    new_interest = Interest.objects.create(
        building_id=data.get('building_id'),
        listing_id=data.get('listing_id'),
        tracking_id=data['tracking_id'],
        agent_email=data.get('agent_email'),
        brokerage_key=data.get('brokerage_key'),
        brokerage_name=data.get('brokerage_name'),
        min_price=data.get('min_price'),
        max_price=data.get('max_price'),
        availability_start=data.get('availability_start'),
        availability_end=data.get('availability_end'),
        budget=data.get('budget'),
        clazz=data.get('clazz'),
        email=data.get('email'),
        move_in_date=data.get('move_in_date'),
        origin=data.get('origin'),
        phone=data.get('phone'),
    )

    attached_lead = leads.get_lead_for_interest(new_interest, data['first_name'], data['last_name'])

    if attached_lead:
      new_interest.lead_id = attached_lead.id

    new_interest.save()

    return Response({'data': new_interest.id}, status=status.HTTP_201_CREATED)

  @staticmethod
  def _exists(tracking_id):
    existing = Interest.objects.filter(tracking_id=tracking_id).first()
    return existing is not None

class ListableApiView(BaseApiView):

  def get(self, request, *args, **kwargs):
    data = self._get_body(request)
    res_body = {
        'listing_id': None,
        'buildiing_id': None,
    }

    if data['listing_id'] is not None:
      listing = Listing.objects.filter(
          zumper_id=data['listing_id']
      ).first()
      if listing:
        res_body['listing_id'] = listing.listing_id
    elif data['building_id'] is not None:
      building = Building.objects.filter(
          zumper_id=data['building_id']
      )
      if building:
        res_body['building_id'] = building.building_id
    return Response(res_body)

  def post(self, request, *args, **kwargs):
    data = self._get_body(request)
    return Response({'tmp_res': 200})


class ApiException(Exception):

  def __init__(self, message, status_code, missing=None):
    self.status_code=status_code
    self.missing = missing
    super(ApiException, self).__init__(message)
