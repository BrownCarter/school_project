from picamera import PiCamera
from time import sleep
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from gpiozero import MotionSensor, LED
import time

toaddr = 'abuprojectreciever@gmail.com'
me = 'senderraspi@gmail.com'
Subject='security alert'
led = LED(16)

sensor = MotionSensor(4)
camera=PiCamera()
camera.resolution= (1024,768)
camera.start_preview()
my_file = open(".config/.settings", "r")
passwd = my_file.read()
while True:
    if sensor.motion_detected:
        print("Motion was detected...")
        led.on()
        # Wait for the automatic gain control to settle
        sleep(2)
        camera.capture('movement.jpg', resize=(720, 480))
        sleep(10)
        subject='Security alert!!'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr
        
        image_file = open('movement.jpg','rb')
        img = MIMEImage(image_file.read())
        image_file.close()
        msg.attach(img)

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user=me,password=passwd)
        server.send_message(msg)
        print("Alert message sent!")
        server.quit()
    else:
        print("no motion detected yet")
        led.off()
