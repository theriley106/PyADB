import os
import threading
Devices = []

def RestartADB(Devices):
	Command = 'sudo adb kill-server'
	os.system(str(Command))
	for devices in Devices:
	   ConnectDevice(devices) 
def ConnectDevice(udid):
	Command = 'sudo adb connect ' + udid
	os.system(str(Command))
def KeycodeUp(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 19"
	os.system(str(Command))
def KeycodeDown(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 20"
	os.system(str(Command))
def KeycodeHome(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 3"
	os.system(str(Command))
def KeycodeRight(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 22"
	os.system(str(Command))
def TouchScreen(udid, x, y):
	Command = 'sudo adb -s ' + udid + " shell input tap " + str(x) + " " + str(y)
	os.system(str(Command))
def KeycodeLeft(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 21"
	os.system(str(Command))
def KeycodeEnter(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 66"
	os.system(str(Command))
def TakeScreenshot(udid):
	screenshot = str(udid) + '.png'
	Command = "sudo adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + screenshot
	os.system(str(Command))
def StartApplication(udid, app):
	Command = 'sudo adb -s ' + udid + " shell monkey -p " + str(app) + " -c android.intent.category.LAUNCHER 1"
	os.system(str(Command))
def PressButton(udid, image):
	screenshot = str(udid) + '.png'
	Command = "sudo adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + screenshot
	os.system(str(Command))
	time.sleep(3)
	Current = Screen.WhichScreen(screenshot)
	if Current is not None:
		Command = detect.FindPlayButton(image, screenshot)
		Command = 'sudo adb -s ' + udid + " shell input tap " + str(Command)
		os.system(str(Command))
	elif Current is None:
		print('error')
