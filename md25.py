#!/usr/bin/python

#========================================================
# MD25 Dual 12V 2.8A H-bridge motor driver
#
# Author : Jim Herd
# Date : May 2013
#
# Notes
#	Uses Adafruit_I2C module

from Adafruit_I2C import Adafruit_I2C
import time

class MD25 :
  i2c = None

# constructor
  def __init__(self, address=0x58, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug
    self.mode = 0
  # constants
    self.CMD_REG = 16
    self.WHEEL_DIAM = 100
    self.MM_PER_ENCODER_COUNT = (3.14159 * self.WHEEL_DIAM)/360
    self.SHORT_MOVE = 4     # no of slices in a short move
# enumerated values
    self.STOP = 0
    self.NOSTOP = 1
# local variables
    self.slice_size = 100    # move unit in encoder counts
    self.min_speed = 10     # 10% seems reasonable
    self.max_speed = 100
    self.speed_inc = self.min_speed
    self.accel_slice_count = 0
# methods
  def set_mode(self, new_mode):
    if ((new_mode < 0) | (new_mode > 3)):
      if (self.debug):
        print 'Mode {0} must be in range 0 to 3'.format(new_mode)
      return -1
    self.mode = new_mode
    self.i2c.write8(15, new_mode)
    return
#
# set speed with reference to mode
#
  def set_speed(self, channel, speed): 
    if ((speed < -100) | (speed > 100)):
      if (self.debug):
        print 'Speed {0} outwith range -100% to 100%'.format(speed)
      return -1 
    if ((channel < 0) | (channel > 1)):
      if (self.debug):
        print 'Channel {0} must be 0 or 1'.format(channel)
      return -1
    if ((self.mode == 0) | (self.mode == 2)):
      if (speed < 0):
        spd = -((abs(speed - 100) * 128)/100)
      else:
        spd = 128 + ((speed * 127)/100)
    else:
      spd = (speed * 127)/100
    self.i2c.write8(channel, spd)
    return spd
#
# use simple trapezoidal speed profile
#
  def move_distance(self, dist_cm, speed, channel):
    # do checks
    if (dist_cm == 0):
      return 0
    if ((dist_cm < -1000) | (dist_cm > 1000)):
      if (self.debug):
        print 'Distance {0}cm should be in range 0cm to 1000cm'.format(dist_cm)
        return 0
    if ((speed < self.min_speed) | (speed > 100)):
      if (self.debug):
        print 'speed {0} should be in range {1}% to 100%'.format(speed, self.min_speed)
      return -1
    self.max_speed = speed
    if ((channel < 0) | (channel > 1)):
      if (self.debug):
        print 'Channel {0} must be 0 or 1'.format(channel)
      return -1
    # calc slice_size to be proportional to speed (needed because of slowness of I2C)
    slice_size = 10 + speed
    # set direction and appropriate values
    if (dist_cm < 0):
      self.min_speed = -self.min_speed
      self.max_speed = -self.max_speed
      spd_inc = -self.speed_inc
    else:
      spd_inc = self.speed_inc
    # calculate profile parameters
    encoder_count =  int(abs(dist_cm) * 10 * self.MM_PER_ENCODER_COUNT)
    nos_slices = int(encoder_count / self.slice_size)
    slices_to_go = nos_slices
    slices_done = 0
    slices_to_accel = int(speed / self.speed_inc)
    if (slices_to_accel > (nos_slices // 2)):
        slices_to_accel = nos_slices // 2
    slices_to_decel = slices_to_accel - 1
    slices_to_coast = nos_slices - (slices_to_accel + slices_to_decel)
    spd = 0
    # execute move
    self.reset_encoders()
    # if SHORT MOVE then simple move with no trapezoidal profile
    if (nos_slices < self.SHORT_MOVE):
      self.do_move(encoder_count, self.min_speed, channel, self.STOP)
      return encoder_count
    # do acceleration segment
    slices_done = 0
    for i in range (1, (slices_to_accel + 1)):
      spd += spd_inc
      slices_done += 1
      self.do_move((slices_done * self.slice_size), spd, channel, self.NOSTOP)
    # do coast segment
    if (slices_to_coast > 0):
      for i in range (1, (slices_to_coast + 1)):
        slices_done += 1 
        self.do_move((slices_done * self.slice_size), spd, channel, self.NOSTOP)
    # do deceleration segment
    for i in range (1, (slices_to_decel)):
      spd -= spd_inc
      slices_done += 1
      self.do_move((slices_done * self.slice_size), spd, channel, self.NOSTOP)
    # do final run in
    spd -= spd_inc
    self.do_move(encoder_count, spd, channel, self.STOP)
    return encoder_count
#
  def do_move(self, encoder_count, speed, channel, action):
    print 'count = {0}, speed = {1}, action = {2}, mode = {3}'.format(encoder_count, speed, action, self.mode)
    self.set_speed(0, speed)
    self.set_speed(1, speed)
    errno = self.wait_encoder_count(encoder_count, channel)
    if ((action == self.STOP) | (errno < 0)):
      self.stop()
#
  def turn_angle(self, angle, speed):
    if ((angle < -359) | (angle > 359)):
      if (self.debug):
        print 'Angle {0} should be in range -359 to +359'.format(angle)
      return -1
#
  def wait_encoder_count(self, count, channel):
    null_count = 0
    while True:
      new_count = abs(self.read_encoder(channel))
      if (new_count >= count):
        return 0
      if (new_count < 2):
        null_count += 1
      if (null_count > 1000):
        return -1
#
  def set_accel(self, accel):
    if ((accel < 0) | (accel > 100)):
      if (self.debug):
        print 'Acceleration {0} outwith range 0 to 100%'.format(accel)
    acc = 255 - ((accel * 255)/100)
    self.i2c.write8(3, acc)
    return 0
#
  def stop(self):
    stop_spd = 0
    if ((self.mode == 0) | (self.mode == 2)):
      stop_spd = 128
    self.i2c.write8(0, stop_spd)
    self.i2c.write8(1, stop_spd)
#
  def read_voltage(self):
    return (self.i2c.readU8(10))
#
  def read_current(self, channel):
    if ((channel < 0) | (channel > 1)):
      if (self.debug):
        print 'Channel {0} outwith range 0 to 1'.format(channel)
      return -1
    return (self.i2c.readU8(11 + channel))
#
  def read_reg(self, reg):
    return  self.i2c.readU8(reg)
#
  def write_reg(self, reg, value):
    self.i2c.write8(reg, value)
#
  def read_encoder(self, num):
    if ((num < 0) | (num > 1)):
      if (self.debug):
        print 'encoder {0} is not in range 0 to 1'.format(num)
      return -1
    base_reg = 2
    if (num == 0):
      base_reg = 6
    b3 = self.i2c.readS8(base_reg)
    b2 = self.i2c.readU8(base_reg+1)
    b1 = self.i2c.readU8(base_reg+2)
    b0 = self.i2c.readU8(base_reg+3)
    encoder = (b3 << 24) + (b2 << 16) + (b1 << 8) + b0
    return encoder
#
  def reset_encoders(self):
    self.write_reg(self.CMD_REG, 0x20)
#
  def speed_reg_on(self):
    self.write_reg(self.CMD_REG, 0x31) 
#
  def speed_reg_off(self):
    self.write_reg(self.CMD_REG, 0x30)
#
  def timeout_on(self):
    self.write_reg(self.CMD_REG, 0x33)
#
  def timeout_off(self):
    self.write_reg(self.CMD_REG, 0x32)
#
  def set_accel_rate(self, accel_rate):
    if ((accel_rate < 1) | (accel_rate > 10)):
      if (self.debug):
        print'Acceleration rate {0} outwith range 1 to 10'.format(accel_rate)
      return -1
    self.write_reg(14, accel_rate)
