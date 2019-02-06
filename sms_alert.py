import time
import smtplib
import RPi.GPIO as GPIO

TO= 6316556084@vtext.com
GMAIL_USER=jbor34@gmail.com
PASS= 'M@lfegor1'

SUBJECT = 'Alert!'
TEXT = 'Your Raspberry Pi detected an intruder!'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN)

def send_mail(): #the texting portion
    print "Sending text"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(GMAIL_USER,PASS)
    header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
    print header
    msg = header + '\n' + TEXT + '\n\n'
    server.sendmail(GMAIL_USER,TO,msg)
    server.quit()
    time.sleep(1)
    print "Text sent"

while True:
    if GPIO.input(13)==1: #trigger if sensor has detected something
        send_mail()
        time.sleep(120) #Sleep for 2 minutes
    else:
        time.sleep(5) #check every 5 seconds
