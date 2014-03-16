#!/usr/bin/python

from srf08 import SRF08
import time

#=====================================================
# SRF08_test : exercise SRF08 class
#

srf08 =  SRF08(0x70, debug=True)

print 'SRF08 address change program'
srf08.write_reg(0, 0xA0)
srf08.write_reg(0, 0xAA)
srf08.write_reg(0, 0xA5)
srf08.write_reg(0, 0xEA)
print 'Change complete'

