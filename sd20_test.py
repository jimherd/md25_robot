#!/usr/bin/python

from sd20 import SD20
import time

#=====================================================
# MD21_test : exercise MD21 class
#

sd20 =  SD20(0x61, debug=True)

print 'SD20 test started'

sd20.set_servo(1, 1)
time.sleep(5)
sd20.set_servo(1, 90)

