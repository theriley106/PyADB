import os
import threading
from xml.dom import minidom
import random
import time
import csv


ButtonsToClick = ["com.checkpoints.app:id/play_all_button", "com.checkpoints.app:id/tab_videos"]

def KillADB():
	Command = 'sudo adb kill-server'
	os.system(str(Command))
def TakeScreenshot(udid):
	screenshot = str(udid) + '.png'
	Command = "sudo adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + screenshot
	os.system(str(Command))
def LoadDevicesFromCSV(Location):
	RawCSV = open(Location, 'r')
	RawDeviceList = csv.reader(RawCSV)
	RawDeviceRows = [row for row in RawDeviceList]
	Devices = [l[0] for l in RawDeviceRows]
	random.shuffle(Devices)
	IPs = Devices
	Devices = []
	for IP in IPs:
		Connected = False
		if 'unable' not in os.popen('sudo adb connect ' + str(IP)).read():
			os.system('sudo adb -s ' + str(IP) + ' shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0')
			os.system('sudo adb -s ' + str(IP)  + ' shell settings put system screen_brightness 0')
			Devices.append(str(IP) + ':5555')
			Connected = True
			print(str(IP) + ' Connected')
		if Connected == False:
			print(str(IP) + ' Not Connected')
	return Devices

def FindButton(button, udid):
	SavedFile = str(udid[:-5]) + str(random.randint(99,9999999999)) + '.xml'
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
	while True:
		try:
			ResetCheck = 0
			time.sleep(random.randint(1,60) + 5)
			os.system('sudo adb -s ' + udid + " shell monkey -p com.checkpoints.app -c android.intent.category.LAUNCHER 1")
			time.sleep(random.randint(30,120) + 30)
			while ResetCheck < (100 * len(ButtonsToClick)):
				for button in ButtonsToClick:
					os.system(FindButton(button, udid))
					time.sleep(random.randint(5,15) + 20)
					ResetCheck = ResetCheck + 1
			time.sleep(random.randint(120, 480))
		except:
			print('error')
			time.sleep(random.randint(1200, 2000))

KillADB()
DeviceList = LoadDevicesFromCSV('main.csv')
threads = [threading.Thread(target=StartApplication, args=(udid,)) for udid in DeviceList]
for thread in threads:
	thread.start()

