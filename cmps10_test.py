#!/usr/bin/python

from cmps10 import CMPS10
import time

#=====================================================
# cmps10_test : exercise CMPS10 class
#

cmps10 =  CMPS10(0x60, debug=True)

print "CMPS10 test started"

for x in range(0, 9):
  bearing = cmps10.read_bearing()
  degrees = bearing // 10
  print 'Bearing = {0} :: Angle = {1} '.format(bearing, degrees)
  time.sleep(2)

