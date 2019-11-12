# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

from utils import enum


# TODO(tetsuji): none of these enums are fleshed out
class AppointmentStatus(enum.Enum):
  SCHEDULED = 0
  COMPLETED = 1
  CANCELLED = 2
  RESCHEDULED = 3
  DELAYED = 4


class Features(enum.EnumBitmask):
  APPLICATION_FEE = 1
  ASSISTED_LIVING = 2
  SPECIALS = 3
  INCOME_RESTRICTED = 4
  SECTION_8 = 5
  SENIOR_LIVING = 6
  SHORT_TERM = 7
  STUDENT_HOUSING = 8
  VIP = 9
  SWEET_DEAL = 10
  SELECT = 11
  SELECT_MONETIZED = 12
  PAID_PROMOTION = 13
  META_NO_INDEX = 14
  REX = 15
  EXCLUSIVE = 16
  MM_EXCLUDE = 17
  MM_PREVENT = 18
  DIRECT_DEAL = 19
  HAS_UNITS = 20
  BOOK_NOW = 21
  THIRD_PARTY_PAID = 22
  LARGE_LIST_CARD = 23
  REQ_PHONE_NUMBER = 24
  REQ_MOVE_IN_DATE = 25
  REQ_CUSTOM_MSG = 26
  FACEBOOK_EXCLUDE = 27
  LEASELOCK = 28
  FEATURED = 29
  TOUR = 30


class InterestType(enum.Enum):
  UNKNOWN = 0
  USER_MESSAGE = 1
  PHONE = 2


class InternalFeatures(enum.EnumBitmask):
  SHOWING_SPECIALIST = 1


class PropertyStatus(enum.Enum):
  UNKNOWN = 0
  ACTIVE = 1
  DRAFT = 2
  ARCHIVED = 3
  LEASED = 4
  DELETED = 5
  WITHDRAWN = 6
  FETCHING_MEDIA = 7
  MODERATION = 8
  PENDING = 9
  DUPLICATE = 10
  BANNED = 11
  SPAM = 12
  HONEYPOT = 13
  FOR_SALE = 14
  PRIVATE = 15


class Syndications(enum.EnumBitmask):
  TRULIA = 1
