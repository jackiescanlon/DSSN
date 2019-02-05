import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # formerly GPIO.BCM -> doesnt work

PIRpin = 13 #GPIO 18

GPIO.setup(PIRpin, GPIO.IN)

def TEXTALARM(PIRpin):

    print("PIR sensor triggered!")
    time.sleep(2)

print("Motion Sensor Alarm (CTRL+C to exit)")
time.sleep(2)
print("Ready")

try:
    GPIO.add_event_detect(PIRpin, GPIO.RISING, callback=TEXTALARM)
    while(1):
        time.sleep(1)
        if GPIO.input(PIRpin):
            print("PIR pin high")
        else:
            print("PIR pin low")
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
    




