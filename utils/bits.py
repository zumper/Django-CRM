# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# a collection of bit logic functions


# for use with reduce: a |= (1<<b)
_orshift = lambda a, b: a | (1 << b)


# NOTE(woody): after some basic speed testing, i determined this was about as speedy as i could get
def decode_bitset(num):
  """yields bit positions that are 1's in the binary repr of input integer.
  This is a yielding function, so if you want a list/set repr, use it appropriately
  This function is unable to decode negative numbers, you must mask to some positive range because
  there is no known precision limit (i16, i32, i64 etc.) to interpret -1 as.

  :param num:  a non-negative integer
  :yields: index positions in ascending order
  """
  if num < 0:
    raise ValueError('unable to decode negative numbers')
  i = 0
  while num != 0:
    if num & 1 == 1:
      yield i
    num >>= 1
    i += 1


def encode_bitset(indices):
  """encodes the indices into a bitset integer.

  :param iterable indices: an iterable of indices. need not be unique or sorted
  :return: integer bitset
  """
  return reduce(_orshift, indices, 0)


def ntz64(i, validate=False):
  """number of trailing zeros for a 64 bit integer
  this is an instruction for most processors, but python doesn't expose it

  :param i: interpreted as 64 bit, best if 'unsigned'
  :param validate:
  :return: the number of trailing zeros, 64 if i==0
  """
  if validate and (i >> 64) > 0:
    raise ValueError('input must be 64 bit or less')
  if (i & 0xffffffffffffffff) == 0:
    return 64
  n = 63
  y = (i & 0xffffffff)
  if y != 0:
    n, i = (n - 32, y)
  else:
    i = (i >> 32) & 0xffffffff
  y = (i << 16) & 0xffffffff
  if y != 0:
    n, i = (n - 16, y)
  y = (i << 8) & 0xffffffff
  if y != 0:
    n, i = (n - 8, y)
  y = (i << 4) & 0xffffffff
  if y != 0:
    n, i = (n - 4, y)
  y = (i << 2) & 0xffffffff
  if y != 0:
    n, i = (n - 2, y)
  return n - ((((i << 1) & 0xffffffff) >> 31) & 0xffffffff)


def ntz32(i, validate=False):
  """number of trailing zeros for a 64 bit integer
  this is an instruction for most processors, but python doesn't expose it

  :param i: interpreted as 32 bit, best if 'unsigned'
  :param validate:
  :return: the number of trailing zeros, 32 if i==0
  """
  if validate and (i >> 32) > 0:
    raise ValueError('input must be 32 bit or less')
  if (i & 0xffffffff) == 0:
    return 32
  n = 31
  y = (i << 16) & 0xffffffff
  if y != 0:
    n, i = (n - 16, y)
  y = (i << 8) & 0xffffffff
  if y != 0:
    n, i = (n - 8, y)
  y = (i << 4) & 0xffffffff
  if y != 0:
    n, i = (n - 4, y)
  y = (i << 2) & 0xffffffff
  if y != 0:
    n, i = (n - 2, y)
  return n - ((((i << 1) & 0xffffffff) >> 31) & 0xffffffff)
