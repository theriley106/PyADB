import os
import random
from xml.dom import minidom
import sys
import time
import Pickling
import re
import operator
import threading
reload(sys)
sys.setdefaultencoding("utf-8")
global Elevated
Elevated = True

def returnList(udid, text=None, resource_id=None, class_name=None, index_num=None, package=None, content_desc=None, checkable=None, checked=None, clickable=None, enabled=None, focusable=None, focused=None, scrollable=None, long_clickable=None, password=None, selected=None, bounds=None):
	filename = GrabUiAutomator(udid)
	xmldoc = minidom.parse(filename)
	itemlist = xmldoc.getElementsByTagName('node')
	ListOfBounds = {}
	PreviousCorrect = 0
	for i in range(len(itemlist)):
		Correct = 0
		if text != None:
			if str(text) == itemlist[i].attributes['text'].value:
				Correct += 1
		if class_name != None:
			if str(class_name) == itemlist[i].attributes['class'].value:
				Correct += 1
		if index_num != None:
			if str(index_num) == itemlist[i].attributes['index'].value:
				Correct += 1
		if resource_id != None:
			if str(resource_id) == itemlist[i].attributes['resource-id'].value:
				Correct += 1
		if package != None:
			if str(package) == itemlist[i].attributes['package'].value:
				Correct += 1
		if content_desc != None:
			if str(content_desc) == itemlist[i].attributes['content-desc'].value:
				Correct += 1
		if checkable != None:
			if str(checkable) == itemlist[i].attributes['checkable'].value:
				Correct += 1
		if checked != None:
			if str(checked) == itemlist[i].attributes['checked'].value:
				Correct += 1
		if clickable != None:
			if str(clickable) == itemlist[i].attributes['clickable'].value:
				Correct += 1
		if enabled != None:
			if str(enabled) == itemlist[i].attributes['enabled'].value:
				Correct += 1
		if focusable != None:
			if str(focusable) == itemlist[i].attributes['focusable'].value:
				Correct += 1
		if focused != None:
			if str(focused) == itemlist[i].attributes['focused'].value:
				Correct += 1
		if scrollable != None:
			if str(scrollable) == itemlist[i].attributes['scrollable'].value:
				Correct += 1
		if long_clickable != None:
			if str(long_clickable) == itemlist[i].attributes['long-clickable'].value:
				Correct += 1
		if password != None:
			if str(password) == itemlist[i].attributes['password'].value:
				Correct += 1
		if selected != None:
			if str(selected) == itemlist[i].attributes['selected'].value:
				Correct += 1
		if Correct > 0 and Correct > PreviousCorrect:
			Bounds = itemlist[i].attributes['bounds'].value
		PreviousCorrect = Correct
	Bounds = GetBounds(Bounds)
	InputRandomBound(udid, Bounds)
	return Bounds



def MultiCommand(command):
	commands = []
	if 'None' in str(command):
		for Device in Devices:
			commands.append(command.replace('None', Device))
	threads = [threading.Thread(target=runCommand, args=(command,)) for command in commands]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()

def runCommand(command):
	if Elevated == True:
		os.system('sudo {}'.format(command))
	else:
		os.system('{}'.format(command))


def MuteSound(udid):
	#Pixi glitz
	StartApplication(udid, 'com.android.music')
	for i in range(10):
		runCommand('sudo adb -s {} shell input keyevent 25'.format(udid))
	print('muted volume')
	
def RemoveLock(udid):
	#Pixi glitz
	runCommand('sudo adb -s {} shell am start -a android.app.action.SET_NEW_PASSWORD'.format(udid))
	time.sleep(1)
	e = UiAutomatorToList(udid)
	for i in range(len(e)):
		if str(e[i][2]) == "None":
			InputRandomBound(udid, e[i][-4:])
			print('removed lock screen')

def ClickStayAwake(udid):
	#Pixi glitz
	runCommand('sudo adb -s {} shell am start -n com.android.settings/.DevelopmentSettings'.format(udid))
	time.sleep(3)
	e = UiAutomatorToList(udid)
	for i in range(len(e)):
		if str(e[i][0]) == "android:id/checkbox" and str(e[i][1]) == "android.widget.CheckBox" and str(e[i-2][2]) == "Screen will never sleep while charging" and str(e[i][7]) == "false":
			InputRandomBound(udid, e[i][-4:])
			print('clicked stay awake')
def ConnectToWifi(wifi, password, proxy=False, udid=None):
	def Command(udid):
		#Pixi glitz
		runCommand('sudo adb -s {} shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings'.format(udid))
		time.sleep(3)
		e = UiAutomatorToList(udid)
		for i in range(len(e)):
			if str(e[i][2]) == str(wifi):
				InputRandomBound(udid, e[i][-4:])
				print('clicked wifi network {}'.format(wifi))
		time.sleep(1)
		InputText(udid, password)
		if proxy != False:
			split = proxy.partition(':')
			host = split[0]
			port = split[2]
			KeycodeBack(udid)
			ClickButton(udid, 'Show advanced options')
			for i in range(6):
				KeycodeDpad_Down(udid)
			ClickButton(udid, "None")
			time.sleep(1)
			ClickButton(udid, "Manual")
			for i in range(6):
				KeycodeDpad_Down(udid)
			ClickButton(udid, "proxy.example.com")
			InputText(udid, host)
			KeycodeBack(udid)
			for i in range(6):
				KeycodeDpad_Down(udid)
			ClickButton(udid, "8080")
			InputText(udid, port)
		time.sleep(1)
		e = UiAutomatorToList(udid)
		for i in range(len(e)):
			if str(e[i][0]) == "android:id/button1":
				InputRandomBound(udid, e[i][-4:])
		
		print('{} connected to {}'.format(udid, wifi))
	if udid != None:
		Command(udid)
	else:
		threads = [threading.Thread(target=Command, args=(udid,)) for udid in Devices]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()

def ClearCache(udid, app):
	runCommand('sudo adb -s {} shell pm clear {}'.format(udid, app))
	
def CheckConnected(udid):
	connected = []
	runCommand('adb devices > t.txt')
	with open('t.txt') as f:
		lines = f.read().splitlines()
	lines.remove(lines[-1])
	lines.remove(lines[0])
	for i in lines:
		a = str(i).partition('\tdevic')[0]
		connected.append(a)
	os.remove('t.txt')
	if str(udid) in str(connected):
		return True
	else:
		return False
def RebootDevice(udid):
	timeout = time.time() + 60*3
	runCommand('sudo adb -s {} reboot'.format(udid))
	while CheckConnected(udid) == False:
		time.sleep(5)
		if time.time() > timeout:
			print('Problem Rebooting')
			break
def RemoveDisplayTimeout(udid):
	StartApplication(udid, 'com.android.settings')
	ClickButton(udid, "Display")
	ClickButton(udid, "Sleep")
	for i in range(15):
		KeycodeDpad_Down(udid)
	ClickButton(udid, "Never")

def ShowTouches(udid):
	runCommand('sudo adb -s {} shell am start -n com.android.settings/.DevelopmentSettings'.format(udid))
	time.sleep(3)
	for i in range(17):
		KeycodeDpad_Down(udid)
	e = UiAutomatorToList(udid)
	for i in range(len(e)):
		if str(e[i][0]) == "android:id/checkbox" and str(e[i][1]) == "android.widget.CheckBox" and str(e[i-2][2]) == "Show visual feedback for touches" and str(e[i][7]) == "false":
			InputRandomBound(udid, e[i][-4:])
			print('clicked show touches')
	for i in range(len(e)):
		if str(e[i][0]) == "android:id/checkbox" and str(e[i][1]) == "android.widget.CheckBox" and str(e[i-2][2]) == "Screen overlay showing current touch data" and str(e[i][7]) == "false":
			InputRandomBound(udid, e[i][-4:])
			print('clicked pointer location')
	
def CheckWifiConnection(udid=None):
	a = []
	def Command(udid):
		Connected = False
		runCommand('sudo adb -s {} shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings'.format(udid))
		lis = UiAutomatorToList(udid)
		for i in range(len(lis)):
			if "Connected" in str(lis[i]):
				print('{} is connected to: {}'.format(udid, lis[i-1][2]))
				Connected = True
		if Connected == False:
			print('{} not currently connected a wifi network'.format(udid))
			KeycodePower(udid)
			a.append(udid)
		return Connected

	if udid != None:
		result = Command(udid)
		return result
	else:
		threads = [threading.Thread(target=Command, args=(udid,)) for udid in Devices]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
	print('{} devices not connected'.format(len(a)))

def RemoveUSBBlock(udid):
	runCommand('sudo adb -s {} shell am start -n com.android.settings/.DevelopmentSettings'.format(udid))
	time.sleep(3)
	for i in range(14):
		KeycodeDpad_Down(udid)
	e = UiAutomatorToList(udid)
	for i in range(len(e)):
		if str(e[i][0]) == "android:id/checkbox" and str(e[i][1]) == "android.widget.CheckBox" and str(e[i-2][2]) == "Check apps installed via ADB/ADT for harmful behavior." and str(e[i][7]) == "true":
			InputRandomBound(udid, e[i][-4:])
			print('clicked remove adb install block over usb')
def Root(udid):
	#Root doesn't work correctly - possibly too old version
	InstallAPK(udid, 'kingroot.apk')

	ClickButton(udid, "More details")
	ClickButton(udid, "com.android.vending:id/continue_anyway")
	StartApplication(udid, 'com.kingroot.RushRoot')
	ClickButton(udid, "TRY TO ROOT")
def SetupDevice(udid):
	#Pixi glitz
	ClickStayAwake(udid)
	ConnectToWifi(udid, 'Ubiquiti2', 'baxter112')
	RemoveLock(udid)
	MuteSound(udid)
def LoginGooglePlay(username, password, udid=None):
	def Command(udid):
		StartApplication(udid, 'com.android.vending')
		ClickButton(udid, "Existing")
		InputText(udid, username)
		KeycodeBack(udid)
		ClickButton(udid, "com.google.android.gsf.login:id/password_edit")
		InputText(udid, password)
		KeycodeBack(udid)
		time.sleep(1)
		ClickButton(udid, "com.google.android.gsf.login:id/next_button")
		time.sleep(1)
		ClickButton(udid, "android:id/button1")
	if udid != None:
		Command(udid)
	else:
		threads = [threading.Thread(target=Command, args=(udid,)) for udid in Devices]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
		



def LoadP(udid, filename):
	PickleResult = Pickling.PicklingList(filename)
	while len(PickleResult) > 0:
		Screen = UiAutomatorToDict(udid)
		for Dic in PickleResult:
			print(Dic)
			for XML in Screen:
				if XML["Index"] == Dic["Index"] and XML["Description"] == Dic["Description"] and XML["ResourceID"] == Dic["ResourceID"] and XML["Class"] == Dic["Class"] and XML["Text"] == Dic["Text"] and XML["Clickable"] == Dic["Clickable"]:
					TouchScreen(udid, XML["Coordinate"][0], XML["Coordinate"][1])
					print(str(XML["Coordinate"][0]), str(XML["Coordinate"][1]))
					PickleResult.remove(Dic)
					Screen = []

def get_num(x):
	return int(''.join(ele for ele in x if ele.isdigit()))
def GetBounds(tt):
	first, ignore, second = tt.partition('][')
	first = first.split(',')
	second = second.split(',')
	AA = int(get_num(first[0]))
	AB = int(get_num(first[1]))
	BA = int(get_num(second[0]))
	BB = int(get_num(second[1]))
	Coordinates = [AA, AB, BA, BB]
	return Coordinates
def GrabUiAutomator(udid):
	SavedFile = 'XML/' + str(udid) + '.xml'
	Command = "sudo adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {} > t.txt".format(udid, udid, SavedFile)
	runCommand(Command)
	return SavedFile
def LoadingScreen(udid):
	found = False
	loading = 'com.android.vending:id/downloading_bytes'
	for results in UiAutomatorToList(udid):
		for result in results:
			if result == 'com.android.vending:id/downloading_bytes':
				found = True
	return found

def InputRandomBound(udid, Bounds):
	A = str(random.randint(Bounds[1], Bounds[3]))
	B = str(random.randint(Bounds[0], Bounds[2]))
	print('sudo adb -s {} shell input tap {} {}'.format(udid, B, A))
	runCommand('sudo adb -s {} shell input tap {} {}'.format(udid, B, A))
def ReturnRandomBound(udid, Bounds):
	A = str(random.randint(Bounds[1], Bounds[3]))
	B = str(random.randint(Bounds[0], Bounds[2]))
	return [B, A]
def KillADB():
	runCommand('adb kill-server')
def RestartADB(Devices):
	KillADB()
	for devices in Devices:
	   ConnectDevice(devices) 
def ConnectDevice(ip):
	runCommand('adb connect {}'.format(ip))
def Rotate(udid):
	runCommand('sudo adb -s {} shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0'.format(udid))
def ForceClose(udid, app):
	runCommand('sudo adb -s {} shell am force-stop {}'.format(udid, app))
def SetBrightness(udid, brightness):
	runCommand('sudo adb -s {} shell settings put system screen_brightness {}'.format(udid, brightness))
def KeycodePower(udid):
	Command = 'sudo adb -s ' + udid + " shell input keyevent 26"
	runCommand(str(Command))

def TakeScreenshot(udid):
	screenshot = str(udid) + '.png'
	Command = "sudo adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + str(screenshot)
	runCommand(str(Command))
	return screenshot
def StartApplication(udid, app):
	Command = 'sudo adb -s ' + udid + " shell monkey -p " + str(app) + " -c android.intent.category.LAUNCHER 1"
	runCommand(str(Command))
def ConnectedDevices(sudo=None):
	connected = []
	Command = 'adb kill-server'
	runCommand(str(Command))
	runCommand('adb devices')
	runCommand('adb devices > t.txt')
	with open('t.txt') as f:
		lines = f.read().splitlines()
	lines.remove(lines[-1])
	lines.remove(lines[0])
	for i in lines:
		a = str(i).partition('\tdevic')[0]
		connected.append(a)
	os.remove('t.txt')
	try:
		return connected
	except:
		return
def CurrentApp(udid):
	app = UiAutomatorToList(udid)[0][3]
	return app
def Scroll(udid, sx, sy, ex, ey, Delay=None):
	if Delay == None:
		runCommand('sudo adb -s {} shell input swipe {} {} {} {}'.format(udid, sx, sy, ex, ey))
	else:
		runCommand('sudo adb -s {} shell input swipe {} {} {} {} {}'.format(udid, sx, sy, ex, ey, Delay))
def DetermineFinished(udid):
	#This determines if you're at the end of a list
	EndOfList = False
	List1 = UiAutomatorToList(udid)
	runCommand('sudo adb -s {} shell input swipe 150 320 0 0 2000'.format(udid))
	List2 = UiAutomatorToList(udid)
	if List1 == List2:
		EndOfList = True
	return EndOfList
def SearchForMultiButtons(udid, listofbuttons):
	#Searches through a list of buttons on the screen and if the button is found it clicks and returns
	File = GrabUiAutomator(udid)
	CurrentScreen = XMLtoList(File)
	for parts in CurrentScreen:
		for buttons in listofbuttons:
			for part in parts:
				if str(part) == str(buttons):
					bounds = parts[-4:]
					InputRandomBound(udid, bounds)
					return str(buttons)
def InstallAPK(udid, apk):
	runCommand('sudo adb -s {} install {}'.format(udid, apk))
def InputText(udid, text):
	runCommand('sudo adb -s {} shell input text {}'.format(udid, text))


def ClickButton(udid, button):
	File = GrabUiAutomator(udid)
	CurrentScreen = XMLtoList(File)
	for parts in CurrentScreen:
		for part in parts:
			if str(part) == str(button):
				bounds = parts[-4:]
				InputRandomBound(udid, bounds)

def Keycode(number, udid=None):
	def Command(number):
		return str("sudo adb -s {} shell input keyevent {}".format(udid, number))
	Command = Command()
	if udid != None:
		runCommand(Command)
	else:
		MultiCommand(Command)

#Devices = ConnectedDevices()
#print('{} Devices Currently Connected'.format(len(Devices)))