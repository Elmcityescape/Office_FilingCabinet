import RPi.GPIO as GPIO
from time import sleep

#debug!
print('Start')

GPIO.setmode(GPIO.BCM)

MATRIX = [ [1, 2, 3],
           [4, 5, 6],
           [7, 8, 9],
           ['*',0,'#'] ]

ROW = [21, 20, 16, 12]
COL = [26, 19, 13]

RD=17
ACCT=18

for j in range(3):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)


GPIO.setup(RD, GPIO.OUT) # r&d output
GPIO.setup(ACCT, GPIO.OUT) # accounting output
GPIO.output(RD, 0)
GPIO.output(ACCT, 0)

### MAIN ###



GPIO.wait_for_edge(ROW[1], GPIO.RISING)
print("Pressed")
GPIO.wait_for_edge(ROW[1], GPIO.FALLING)
print("Released")
GPIO.cleanup()

