#!/usr/bin/python

#========================================================
# MD03 24V 20A H-bridge motor driver
#
# Author : Jim Herd
# Date : May 2013
#
# Notes
#	Uses Adafruit_I2C module

from Adafruit_I2C import Adafruit_I2C

class MD03 :
  i2c = None

# constructor
  def __init__(self, address=0x58, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

  def set_speed(self, speed): 
    if ((speed < 0 ) | (speed > 100)):
      if (self.debug):
	print 'Speed {0} outwith range 0 to 100%'.format(speed)
	return -1 
    spd = ((speed * 255)/100)
    self.i2c.write8(2, spd)
    return 0

  def set_accel(self, accel):
    if ((accel < 0) | (accel > 100)):
      if (self.debug):
        print 'Acceleration {0} outwith range 0 to 100%'.format(accel)
    acc = 255 - ((accel * 255)/100)
    self.i2c.write8(3, acc)
    return 0

  def stop(self):
    self.i2c.write8(0, 0)

  def move_forward(self):
    self.i2c.write8(0, 1)

  def move_reverse(self):
    self.i2c.write8(0, 2)

  def read_reg(self, reg):
    return  self.i2c.readU8(reg)

