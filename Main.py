import os
import threading
import time
import random
Devices = []
Cisco1PTV = ["192.168.2.131", "192.168.2.132", "192.168.2.133", "192.168.2.134", "192.168.2.135"]
RouterPTV = ["192.168.2.91", "192.168.2.92", "192.168.2.93", "192.168.2.94", "192.168.2.95"]
RouterPPQ = ["192.168.2.96", "192.168.2.97", "192.168.2.98", "192.168.2.99", "192.168.2.90"]
Cisco1PPQ = ["192.168.2.128", "192.168.2.129", "192.168.2.130", "192.168.2.136", "192.168.2.137"]
PTV = RouterPTV + Cisco1PTV
PPQ = RouterPPQ + Cisco1PPQ
Cisco1 = Cisco1PPQ + Cisco1PTV
Router = RouterPPQ + RouterPTV
Devices = Cisco1 + Router
WirelessDevices = []
for udid in Devices:
        wireless = str(udid) + ':5555'
        WirelessDevices.append(wireless)
        
        
def RestartADB(Devices):
	Command = 'sudo adb kill-server'
	os.system(str(Command))
	for devices in Devices:
	   ConnectDevice(devices) 
def ConnectDevice(udid):
	Command = 'sudo adb connect ' + udid
	os.system(str(Command))
def Rotate(udid):
        Command = 'sudo adb -s ' + udid + ' shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0'
        os.system(str(Command))
def KeycodePower(udid):
	Command = 'sudo adb -s ' + udid + ":5555 shell input keyevent 26"
	os.system(str(Command))
def KeycodeUp(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 19"
	os.system(str(Command))
def SwipeUp(udid):
        Command = 'sudo adb -s ' + udid + " shell input swipe 0 500 0 0"
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
	print(screenshot)
	Command = "sudo adb -s " + str(udid) + ":5555 shell screencap -p | sed 's/\r$//' > screen1.png"# + str(screenshot)
        print(str(Command))
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
RestartADB(Devices)
for udid in Router:
        Command = 'sudo adb -s ' + udid + ":5555 shell input text treypass1190"
        os.system(str(Command))
        print('done')
for udid in Router:
        Command = 'sudo adb -s ' + udid + ":5555 shell input keyevent 66"
        os.system(str(Command))
        print('done')
        time.sleep(random.randint(1,8))

