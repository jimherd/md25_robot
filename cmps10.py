#!/usr/bin/python

#========================================================
# CMPS10: Tilt compensated compass
#
# Author : Jim Herd
# Date : May 2013
#
# Notes
#	Uses Adafruit_I2C module

from Adafruit_I2C import Adafruit_I2C

class CMPS10 :
  i2c = None

# constructor
  def __init__(self, address=0x60, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

  def read_reg(self, reg): 
    if ((reg < 0 ) | (reg > 22)):
      if (self.debug):
	print 'Register {0} outwith range 0 to 22'.format(reg)
	return -1 
    return self.i2c.readU8(reg)

  def write_cmd(self, val):
    self.i2c.write8(22, val)
    return 0

  def read_bearing(self):
    return self.i2c.readU16(2)

