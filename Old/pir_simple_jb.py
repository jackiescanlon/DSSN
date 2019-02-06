#Basic code to control the PIR Sensor
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) #if RPi.GPIO detects changes to the pin is throws a flag
GPIO.setmode(GPIO.BOARD)

#Read output pin of PIR sensor
GPIO.setup (3,GPIO.IN) #Basic structure GPIO.setup (channel, GPIO.IN/OUT, initial=GPIO.HIGH/LOW)

try:
  print('I am sleeping. Give me a moment')
  time.sleep(0) #Allows sensor to stabilize (takes about a minute)
  while True:
      detection = GPIO.input(3) #read the value of a GPIO pi
      if detection==1:                 #When output from motion sensor is LOW
        print ("Intruder alert")
        print ("Who's man's is in my house")
        time.sleep(2) #Adjust this as necessary to get rid of multipl detections
      time.sleep(.01)
except:
  GPIO.cleanup()
