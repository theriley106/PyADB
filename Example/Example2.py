import os
import threading
from xml.dom import minidom
import random
import time
import csv


ButtonsToClick = ["com.checkpoints.app:id/play_all_button", "com.checkpoints.app:id/tab_videos", "android:id/button1", 'com.android.launcher:id/launcher', "com.checkpoints.app:id/sexy_dialog_message"]
def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))
def KillADB():
	Command = 'sudo adb kill-server'
	os.system(str(Command))
def TakeScreenshot(udid):
	screenshot = str(udid) + '.png'
	Command = "sudo adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + screenshot
	os.system(str(Command))
	return screenshot
def LoadDevicesFromCSV(Location):
	RawCSV = open(Location, 'r')
	RawDeviceList = csv.reader(RawCSV)
	RawDeviceRows = [row for row in RawDeviceList]
	Devices = [l[0] for l in RawDeviceRows]
	random.shuffle(Devices)
	IPs = Devices
	print(str(IPs))
	Devices = []
	for IP in IPs:
		Connected = False
		if 'connected' in os.popen('sudo adb connect ' + str(IP)).read():
			os.system('sudo adb -s ' + str(IP) + ':5555 shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0')
			os.system('sudo adb -s ' + str(IP)  + ':5555 shell settings put system screen_brightness 0')
			Devices.append(str(IP) + ':5555')
			Connected = True
			print(str(IP) + ' Connected')
		if Connected == False:
			print(str(IP) + ' Not Connected')
	print(str(Devices))
	return Devices

def FindButton(button, udid):
	SavedFile = str(udid[:-5]) + '.xml'
	Command = "sudo adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {}".format(str(udid), str(udid), SavedFile)
	os.system(Command)
	xmldoc = minidom.parse(SavedFile)
	itemlist = xmldoc.getElementsByTagName('node')
	for s in itemlist:
		item = s.attributes['resource-id'].value
		if str(item) == button:
			tt = s.attributes['bounds'].value
			first, ignore, second = tt.partition("][")
			first = first.split(',')
			second = second.split(',')
			AA = int(get_num(first[0]))
			AB = int(get_num(first[1]))
			BA = int(get_num(second[0]))
			BB = int(get_num(second[1]))
			a = random.randint(0, abs(BB - AB))
			b = random.randint(0, abs(BA - AA))
			CoordinateA = AA + a
			CoordinateB = AB + b
			Command = "sudo adb -s {} shell input tap {} {}".format(str(udid), str(CoordinateA), str(CoordinateB))
	os.remove(SavedFile)
	return Command

def StartApplication(udid):
	print('start application')
	Size = 0
	while True:
		try:
			ResetCheck = 0
			time.sleep(random.randint(1,60) + 5)
			os.system('sudo adb -s ' + udid + " shell monkey -p com.checkpoints.app -c android.intent.category.LAUNCHER 1")
			time.sleep(random.randint(30,120) + 30)
			while ResetCheck < (100 * len(ButtonsToClick)):
				Size1 = os.path.getsize(TakeScreenshot(udid))
				if abs(Size1 - Size) < 5000:
					time.sleep(180)
					Size2 = os.path.getsize(TakeScreenshot(udid))
					if abs(Size2 - Size) < 5000:
						os.system('sudo adb -s ' + udid + " shell monkey -p com.checkpoints.app -c android.intent.category.LAUNCHER 1")
						time.sleep(30)
				Size = Size1
				for i in range(5):
					for button in ButtonsToClick:
                                            command = FindButton(button, udid)
                                            os.system(command)
                                            if str(button) == "android:id/button1" and 'input tap' in str(command):
                                                time.sleep(random.randint(12, 45))
                                                os.system('sudo adb -s ' + udid + " shell monkey -p com.checkpoints.app -c android.intent.category.LAUNCHER 1")
                                                time.sleep(random.randint(30,80))
                                            if str(button) == 'com.android.launcher:id/launcher' and 'input tap' in str(command):
                                                time.sleep(random.randint(12, 45))
                                                os.system('sudo adb -s ' + udid + " shell monkey -p com.checkpoints.app -c android.intent.category.LAUNCHER 1")
                                                time.sleep(random.randint(30,80))
                                            time.sleep(random.randint(5,15) + 20)
                                            ResetCheck = ResetCheck + 1
                        time.sleep(random.randint(120, 480))
		except BaseException as exp:
			print('error' + str(exp))
			time.sleep(random.randint(1200, 2000))

KillADB()
DeviceList = LoadDevicesFromCSV('main.csv')
threads = [threading.Thread(target=StartApplication, args=(udid,)) for udid in DeviceList]
for thread in threads:
	thread.start()

