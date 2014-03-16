#!/usr/bin/python

#========================================================
# SRF08 ultrasonic ranger driver
#
# Author : Jim Herd
# Date : August 2013
#
# Notes
#	Uses Adafruit_I2C module

from Adafruit_I2C import Adafruit_I2C
import time

class SRF08 :
  i2c = None

# constructor
  def __init__(self, address=0x70, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug
    (self.RANGE_INCH, self.RANGE_CM, self.RANGE_US) = (0x50, 0x51, 0x52)
    
#
  def read_reg(self, reg): 
    if ((reg < 0 ) | (reg > 35)):
      if (self.debug):
	print 'Register {0} outwith range 0 to 35'.format(reg)
      return -1 
    return self.i2c.readU8(reg)
#
  def write_reg(self, reg, val):
    if ((reg < 0) | (reg > 2)):
      if (self.debug):
        print 'Register {0} outwith range 0 to 2'.format(reg)
      return -1
    self.i2c.write8(reg, val)
#
  def read_echo(self, echo):
    if ((echo < 1) | (echo > 17)):
      if (self.debug):
        if (self.debug):
          print 'Echo request {0} outwith range 1 to 17'.format(echo)
        return -1
    return self.i2c.readU16(((echo - 1) * 2) + 2)
#
  def get_echo(self, mode):
    if ((mode < self.RANGE_INCH) | (mode > self.RANGE_US)):
      if (self.debug):
        print ' Range should be RANGE_INCH, RANGE_CM or RANGE_US'.format()
      return -1
    self.write_reg(0, mode)
    time.sleep(0.07)
    return self.read_echo(1)
#
  def read_light_sensor(self):
    return self.read_reg(1)
#
  def set_gain(self, gain_code):
    if ((gain_code < 0) | (gain_code > 31)):
      if (self.debug):
        print 'gain code {0} must be in range 0 to 31'.format(gain_code)
      return -1
    self.write_reg(1, gain_code)
#
  def set_range(self, distance):
    if ((distance < 50) | (distance > 6000)):
      if (self.debug):
        print 'Range of {0} must bet between 50mm and 6000mm'.format(distance)
      return -1
    val = abs(distance/43)
    self.write_reg(2, val)

    
