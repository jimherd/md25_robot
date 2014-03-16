#!/usr/bin/python

#========================================================
# LCD03 : 20 * 4 LCD LCD text display
#
# Author : Jim Herd
# Date : June 2013
#
# Notes
#	Uses Adafruit_I2C module

from Adafruit_I2C import Adafruit_I2C

CMD_REG = 0
ON = 1
OFF = 0

CLR_SCREEN = 12

(ROW_MAX, COLUMN_MAX) = (4,20)

class LCD03 :
  i2c = None

# constructor
  def __init__(self, address=0x63, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug
#
  def clear(self): 
    self.i2c.write8(CMD_REG, CLR_SCREEN) 
    return 0
#
  def set_cursor(self, row, column):
    if ((row < 1) | (row > ROW_MAX)):
      if (self.debug):
        print 'row {0} should be in range 0 to {1}'.format(row, ROW_MAX)
      return -1
    if ((column < 1) | (column > COLUMN_MAX)):
      if (self.debug):
        print 'column {0} should be in range 0 to {1}'.format(column, COLUMN_MAX)
      return -1
    cmdlist = [3, row, column]
    self.i2c.writeList(CMD_REG, cmdlist)

 
  def backlight_on(self):
    self.i2c.write8(CMD_REG, 19)
    return 0

  def backlight_off(self):
    self.i2c.write8(CMD_REG, 20)
    return 0

  def write_chr(self, char):
    self.i2c.write8(CMD_REG, ord(char))
    return 0

  def write_str(self, string):
    for i in range(0, len(string)):
      self.write_chr(string[i])
    return 0
