#!/usr/bin/python

from srf08 import SRF08
import time

#=====================================================
# SRF08_test : exercise SRF08 class
#

srf08 =  SRF08(0x70, debug=True)

print "SRF08 test started"

srf08.write_reg(2, 0x8C)
srf08.write_reg(1, 12)
for x in range(0, 9):
  srf08.write_reg(0, 0x51)
  time.sleep(1)
  dist = srf08.read_echo(1)
  lval = srf08.read_reg(1)
  print 'Distance = {0} :: light vale = {1}'.format(dist, lval)

