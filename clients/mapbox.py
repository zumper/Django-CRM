# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# mapbox client

_BASE_URL = 'https://api.mapbox.com/%s/%s/mapbox'
_KEY = 'pk.eyJ1IjoidGV0c3VqaS16dW1wZXIiLCJhIjoiY2p0cmtjbno5MHI2MTQ1bXVibGZlNnNmaCJ9.Kz56IrmqwCeayVnzHmdwmA'

_DEFAULT_ICON = 'theatre'

class Client(object):
  """client for MapBox"""

  def __init__(self, service, version='v1'):
    self._BASE_URL = _BASE_URL % (service, version)
    self._HEADERS = {
        'Content-Type': 'applications/x-www-form-urlencoded'
    }
    self._KEY = _KEY


def feature_body(f_type, properties, geo, icon=None, geo_type=None):
  if icon:
    properties['icon'] = icon
  return {
      'type': f_type,
      'properties': properties,
      'geometry': {
          'type': geo_type or 'Point',
          'coordinates': list(geo)
      }
  }
