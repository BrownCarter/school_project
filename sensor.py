from gpiozero import MotionSensor
from time import sleep
pir = MotionSensor(4)
while True:
	pir.wait_for_motion()
	print("Motion dected")
	pir.wait_for_no_motion()
