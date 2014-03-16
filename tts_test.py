#
# test the Text-To-Speech system
#
import os, time

def say(something):
  os.system('espeak -ven+f2 "{0}"'.format(something))

say("hello jim")
time.sleep(2)
say("this after 2 seconds")

