#!/usr/bin/python

from md21 import MD21
import time

#=====================================================
# MD21_test : exercise MD21 class
#

md21 =  MD21(0x61, debug=True)

print 'MD21 test started'

md21.set_servo(1, 10, 0)
time.sleep(3)
md21.set_servo(1, 80, 0)
time.sleep(3)
md21.set_servo(0, 45, 0)
print 'Voltage reading = {0}'.format(md21.read_volts())
