from picamera import PiCamera
from time import sleep
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from gpiozero import MotionSensor, LED
import time
import os
import cv2
import numpy as np

toaddr = 'abuprojectreciever@gmail.com'
me = 'senderraspi@gmail.com'
Subject='security alert'
led = LED(16)

sensor = MotionSensor(4)
camera=PiCamera(resolution=(540, 400), framerate=60)
camera.start_preview()
my_file = open(".config/.settings", "r")
passwd = my_file.read()
while True:
    if sensor.motion_detected:
        print("Motion was detected...")
        led.on()
        # Wait for the automatic gain control to settle
        sleep(10)
        camera.capture('images/movement.png', resize=(720, 480))
        sleep(2)
        cv_image = cv2.imread("./images/movement.png", 0)
        cv_grey = cv2.cvtColor(cv_image, cv2.COLOR_BAYER_BG2GRAY)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            cv_grey,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        print("fount {0} faces".format(len(faces)))
        sleep(2)
        if(len(faces) > 0):
            BLACK = (155, 155, 155)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 1.1
            font_color = BLACK
            font_thickness = 2
            text = "{0} face(s) detected.".format(len(faces))
            text2 = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
            y0, dy = 50, 30 
            image_text = cv2.putText(cv_image, text, (30, 400), font, font_size, font_color, font_thickness, cv2.LINE_AA)
            cv2.putText(cv_image, text2, (30, 430), font, font_size, font_color, font_thickness, cv2.LINE_AA)
            cv2.imwrite("./sky.jpeg", image_text)

            #Sending the mail

            subject='Security alert!!'
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = me
            msg['To'] = toaddr
            image_file = open('images/movement.png','rb')
            img = MIMEImage(image_file.read())
            image_file.close()
            msg.attach(img)
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(user=me,password=passwd)
            server.send_message(msg)
            print("Alert message sent!")
            server.quit()
            if os.path.exists("images/movement.png"):
                os.remove("images/movement.png")
                sleep(2)
        #else:
         #   if os.path.exists("images/movement.png"):
          #      os.remove("images/movement.png")
    else:
        print("no motion detected yet")
        sleep(1)
        led.off()
