#!/usr/bin/python

#========================================================
# SD20 20 channel RC servo driver
#
# Author : Jim Herd
# Date : May 2013
#
# Notes
#	Uses Adafruit_I2C module
#       Supplied as 28-pin PIC chip (16F872)

from Adafruit_I2C import Adafruit_I2C

class SD20 :
  i2c = None
  servo_pos = [0] * 20

# constructor
  def __init__(self, address=0x61, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

  def set_servo(self, servo_no, angle): 
    if ((servo_no < 1 ) | (servo_no > 20)):
      if (self.debug):
        print 'Servo number {0} outwith range 1 to 20'.format(servo_no)
        return -1
    if ((angle < 0) | (angle > 90)):
      if (self.debug):
        print 'Angle {0} outwith range 0 to 90 degrees'.format(angle)
	return -1
    self.servo_pos[servo_no - 1] = angle 
    pulse_width = (angle * 255)/90
    self.i2c.write8(servo_no, pulse_width)
    return 0

  def read_pos(self, servo_nos):
    if ((servo_no < 1) | (servo_nos > 20)):
      return -1
    return self.servo_pos[servo_nos - 1]


