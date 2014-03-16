#!/usr/bin/python

from md25 import MD25
import time

#=====================================================
# MD25_test : exercise MD25 class
#

md25 =  MD25(0x58, debug=True)

print 'MD03 test started'

md25.set_mode(0)
md25.reset_encoders()
md25.timeout_off()
md25.set_accel_rate(1)

logfile  = open('md25_logfile.log','w')

print 'MD25 motor controller test program'
print 'Software revision :: {0}'.format(md25.read_reg(13))
print 'I2C address = 0x{0:x}'.format(md25.address)
print 'Mode = {0}'.format(md25.read_reg(15))
print 'Battery voltage = {0:.1f}V'.format(md25.read_voltage()/10.0)

for i in range(1, 2):
  md25.reset_encoders()
  print 'speed = {0}'.format(md25.set_speed(0, (i*25)))
  md25.set_speed(1, (i*25))
  time.sleep(5)
  md25.stop()
  print 'encoder 0 = {0}'.format(md25.read_encoder(0))
  print 'encoder 1 = {0}'.format(md25.read_encoder(1))
  time.sleep(2)

for i in range (1, 2):
  md25.reset_encoders()
  print 'speed = {0}'.format(md25.set_speed(0, (i * (-25))))
  md25.set_speed(1, (i * (-25)))
  time.sleep(5)
  md25.stop()
  print 'encoder 0 = {0}'.format(md25.read_encoder(0))
  print 'encoder 1 = {0}'.format(md25.read_encoder(1))
  time.sleep(2)
#
for i in range (1, 2):
  md25.set_speed(1, 10)
#  md25.set_speed(1, (i*25))
  time.sleep(1)
  print 'current on motor 0 = {0}A'.format(md25.read_current(0))
  print 'current on motor 1 = {0}A'.format(md25.read_current(1))
  time.sleep(1)
  md25.stop()
  time.sleep(1)
#
encoder_count = md25.move_distance(100, 50, 0)

print 'Encoder count = {0}'.format(encoder_count)
print 'Actual count = {0}'.format(md25.read_encoder(0))

encoder_count = md25.move_distance(-150, 50, 0)
print 'Encoder count = {0}'.format(encoder_count)
print 'Actual count = {0}'.format(md25.read_encoder(0))

md25.stop()

logfile.close()
