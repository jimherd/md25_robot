#!/usr/bin/python

from lcd03 import LCD03
import time

#=====================================================
# LCD03_test : exercise LCD03 class
#

lcd03 = LCD03(0x63, debug=True)

print "LCD03 test started"

lcd03.clear()
lcd03.backlight_on()
value = 42
lcd03.write_str( 'r = {0}'.format(value) )
time.sleep(5)
lcd03.set_cursor(4,1)
lcd03.write_str('row 3')
time.sleep(5)
lcd03.backlight_off()
