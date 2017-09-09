import Android
import interactions
import os
import time
import RPi.GPIO as GPIO
import time
import os
import pyautogui

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def ForceClose(udid, app):
	os.system('adb -s {} shell am force-stop {}'.format(udid, app))

while True:
    input_state = GPIO.input(24)
    if input_state == False:
		a = Android.ConnectedDevices()[0]
		ForceClose(a, 'com.robinhood.android')
		time.sleep(1)
		Android.StartApplication(a, 'com.robinhood.android')
		time.sleep(2)
		Android.Scroll(a, 10, 1000, 10, 400)
		interactions.GrabUiAutomator(a)
		interactions.click(a, text="TSLA")
		time.sleep(3)
		interactions.GrabUiAutomator(a)
		interactions.click(a, text="BUY")
		time.sleep(2)
		interactions.InputText(a, '10000')
		interactions.GrabUiAutomator(a)
		interactions.click(a, resource_id="com.robinhood.android:id/review_order_btn")
