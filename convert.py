#
# Unit conversions
#

import math

def radtodeg(rad):
  return rad * 180 / math.pi

def degtorad(deg):
  return math.pi * deg / 180

def metrestofeet(metres):
  return metres / 0.3048

def speedtoknots(metrespersec):
  return metrespersec / 0.5144444

def speedtofeetpermin(metrespersec):
  return metrespersec * 60 / 0.3048

def lbstokgs(lbs):
  return lbs * 0.453592 

def radpersecondtorpm(radpersec):
  return radpersec * 60 / (2 * math.pi)

def rpmtoradpersecond(rpm):
  return rpm * 2 * math.pi / 60


