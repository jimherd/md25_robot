#!usr/bin/python
#
# Test program for MD25/Raspberry Pi robot
#
from cmps10 import CMPS10
from lcd03  import LCD03
from md25   import MD25
from srf08  import SRF08

import time
import random
#================================================================
# md25_robot_test1 : initial test program for the robot
#
# Initialise hardware
#
srf08 = SRF08(0x70, debug=True)
srf08.set_range(6000)
srf08.set_gain(12)

md25 = MD25(0x58, debug=True)
md25.set_mode(0)
md25.reset_encoders()
md25.timeout_off()

lcd03 = LCD03(0x63, debug=True)
lcd03.clear()
lcd03.backlight_off()

# cmps10 = CMPS10(0x60, debug=True)

lcd03.write_str('Robot test'.format())

md25.set_speed(0,33)
md25.set_speed(1,33)

while True:
  dist = srf08.get_echo(srf08.RANGE_CM)
  lcd03.set_cursor(4,1)
  lcd03.write_str('Dist = {0}cm'.format(dist))
  if (dist < 10):
    md25.stop()
    break
