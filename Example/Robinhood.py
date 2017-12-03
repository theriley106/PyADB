import interactions
import os
import time
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
	time.sleep(.5)
	input_state = GPIO.input(24)
	if input_state == False:
		break

phoneID = interactions.ConnectedDevices()[0]
interactions.ForceClose(phoneID, 'com.robinhood.android')
time.sleep(1)
interactions.StartApplication(phoneID, 'com.robinhood.android')
time.sleep(2)
interactions.Scroll(phoneID, 10, 1000, 10, 400)
interactions.GrabUiAutomator(phoneID)
interactions.click(phoneID, text="TSLA")
time.sleep(3)
interactions.GrabUiAutomator(phoneID)
interactions.click(phoneID, text="BUY")
time.sleep(2)
interactions.InputText(phoneID, '10000')
interactions.GrabUiAutomator(phoneID)
interactions.click(phoneID, resource_id="com.robinhood.android:id/review_order_btn")
