#!/usr/bin/python

from md25 import MD25
import time

#=====================================================
# MD25_test : exercise MD25 class
#

md25 =  MD25(0x58, debug=True)


print 'MD25 : STOPPING MOTORS'

md25.set_mode(1)
md25.reset_encoders()
md25.timeout_off()

md25.stop()

