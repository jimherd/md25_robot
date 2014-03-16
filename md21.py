#!/usr/bin/python

#========================================================
# MD21 21 channel RC servo driver
#
# Author : Jim Herd
# Date : May 2013
#
# Notes
#	Uses Adafruit_I2C module

from Adafruit_I2C import Adafruit_I2C

class MD21 :
  i2c = None
  servo_pos = [0] * 21

# constructor
  def __init__(self, address=0x61, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

  def set_servo(self, servo_no, angle, speed): 
    if ((servo_no < 1 ) | (servo_no > 21)):
      if (self.debug):
        print 'Servo number {0} outwith range 1 to 21'.format(servo_no)
        return -1
    if ((angle < 0) | (angle > 90)):
      if (self.debug):
        print 'Angle {0} outwith range 0 to 90 degrees'.format(angle)
	return -1
    if ((speed < 0 ) | (speed > 255)):
      if (self.debug):
	print 'Speed {0} outwith range 0 to 255'.format(speed)
	return -1
    self.servo_pos[servo_no - 1] = angle 
    pulse_width = 1000 + ((angle *1000)/90)
    buffer = [speed, (pulse_width & 0xFF), ((pulse_width >> 8) & 0xFF)]
    self.i2c.writeList(((servo_no - 1) * 3), buffer)
    return 0

  def read_pos(self, servo_nos):
    if ((servo_no < 1) | (servo_nos > 21)):
      return -1
    return self.servo_pos[servo_nos - 1]

  def read_volts(self):
    return  self.i2c.readU8(65)

