# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# base class for enums

from enum import IntEnum

from utils import bits


class Enum(IntEnum):
  """Base class for enums"""

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

  @classmethod
  def labels_to_values(cls):
    return {key.name: key.value for key in cls}

  @classmethod
  def values_to_labels(cls):
    return {key.value: key.name for key in cls}


class EnumBitmaskMeta(type):
  """Metaclass to provide a bits attribute to an EnumBitmask class, with bit-shifted enum values.
  """

  def __new__(mcs, name, bases, attrs):
    # The EnumBitmask object will call this when it's created. That class shouldn't have a
    # attrs, so skip the check. This preserves the error where the __metaclass__ is
    # used in error though.
    if name != 'EnumBitmask':
      shifted = dict((k, 1 << v,) for k, v in attrs.labels_to_values().items())
      shifted['_ALL'] = ~0
      attrs['bits'] = type('EnumBits', (), shifted)
      attrs['_ALL'] = set(attrs.labels_to_values().values())

    return super(EnumBitmaskMeta, mcs).__new__(mcs, name, bases, attrs)


class EnumBitmask(Enum):
  """Base class for enums used with bitmasks."""
  __metaclass__ = EnumBitmaskMeta

  @classmethod
  def decode_bitmask(cls, encoded_value):
    """Decodes a bitmask to a list of underlying integer enum values."""
    if encoded_value is None:
      return None
    return [x for x in cls.values_to_labels().keys() if encoded_value >> x & 1]

  @classmethod
  def encode_bitmask(cls, enum_values):
    if enum_values is None:
      return None
    return bits.encode_bitset(enum_values)

  @classmethod
  def encode_labels_to_bitmask(cls, labels):
    if labels is None:
      return None
    return bits.encode_bitset(cls.labels_to_values()[x] for x in labels)

  @classmethod
  def decode_bitmask_to_labels(cls, encoded_value):
    """Decodes a bitmask to a list of underlying enum string names."""
    if encoded_value is None:
      return None
    return [v for k, v in cls.values_to_labels().items() if encoded_value >> k & 1]

  @classmethod
  def decode_bitmask_to_set(cls, encoded_value):
    """Decodes a bitmask to a set of underlying integer enum values."""
    if encoded_value is None:
      return None
    return set(cls.decode_bitmask(encoded_value))

  @classmethod
  def decode_set_to_labels(cls, set_values):
    if set_values is not None:
      return [v for k, v in cls.values_to_labels().items() if k in set_values]

  @classmethod
  def is_enum_in_bitmask(cls, enum_value, encoded_bitmask_value):
    """Returns whether the given enum is included the bitmask encoded value

    :param int|None encoded_bitmask_value:
    :param int enum_value:
    :rtype: bool
    """
    return enum_value in (cls.decode_bitmask_to_set(encoded_bitmask_value) or set())
