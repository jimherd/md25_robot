from RPIO import PWM
import time

servo = PWM.Servo()
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

servo.set_servo(24, 1000)
time.sleep(2)

for i in range(0,100):
  servo.set_servo(24, (1000 + (i * 10)));
  time.sleep(0.2)

servo.set_servo(24, 1600)
time.sleep(2)
servo.stop_servo(24)
