import os
import time
import threading
from xml.dom import minidom
import random

ELEVATED = False

def Keycode(number, udid):
	runCommand("sudo adb -s {} shell input keyevent {}".format(udid, number))

def InstallAPK(udid, apk):
	runCommand('sudo adb -s {} install {}'.format(udid, apk))

def CurrentApp(udid):
	app = UiAutomatorToList(udid)[0][3]
	return app

def currentApps(device):
	return getResponse('adb -s {} shell dumpsys activity'.format(device))


def Scroll(udid, sx, sy, ex, ey, Delay=None):
	if Delay == None:
		runCommand('sudo adb -s {} shell input swipe {} {} {} {}'.format(udid, sx, sy, ex, ey))
	else:
		runCommand('sudo adb -s {} shell input swipe {} {} {} {} {}'.format(udid, sx, sy, ex, ey, Delay))

def grabScreenResolution(udid):
	a = getResponse('sudo adb -s {} shell dumpsys window | grep "mUnrestrictedScreen"'.format(udid))
	a = a.partition(") ")[2]
	a, b = a.split("x")
	return [int(a), int(b)]

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

def TakeScreenshot(udid, fileName=None):
	if fileName == None:
		screenshot = str(udid) + '.png'
	else:
		screenshot = fileName
	Command = "sudo adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + str(screenshot)
	runCommand(str(Command))
	return screenshot

def RebootDevice(udid):
	timeout = time.time() + 60*3
	runCommandcu('sudo adb -s {} reboot'.format(udid))
	while CheckConnected(udid) == False:
		time.sleep(5)
		if time.time() > timeout:
			print('Problem Rebooting')
			break

def SetBrightness(udid, brightness):
	runCommand('sudo adb -s {} shell settings put system screen_brightness {}'.format(udid, brightness))

def GrabUiAutomator(udid):
	SavedFile = 'XML/' + str(udid) + '.xml'
	Command = "sudo adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {} > /dev/null".format(udid, udid, SavedFile)
	runCommand(Command)
	return SavedFile

def getResponse(command):
	os.system('{} > tmp'.format(command))
	return open('tmp', 'r').read()

def closeKeyboard(udid):
	if 'mInputShown=true' in str(getResponse('adb -s {} shell dumpsys input_method | grep mInputShown'.format(udid))):
		runCommand('adb -s {} shell input keyevent 111'.format(udid))
		time.sleep(1)

def get_num(x):
	return int(''.join(ele for ele in x if ele.isdigit()))

def closeKeyboard(udid):
	if 'mInputShown=true' in str(getResponse('adb -s {} shell dumpsys input_method | grep mInputShown'.format(udid))):
		runCommand('adb -s {} shell input keyevent 111'.format(udid))
		time.sleep(1)

def grabText(udid, contains):
	closeKeyboard(udid)
	filename = GrabUiAutomator(udid)
	for items in open(filename, 'r').read().split('<node '):
		if str(contains) in str(items):
			return str(items).partition('text="')[2].partition('" resource')[0]

def click(udid, ss=False, addx=0, addy=0, resultNum=None, text=None, resource_id=None, class_name=None, index_num=None, package=None, content_desc=None, checkable=None, checked=None, clickable=None, enabled=None, focusable=None, focused=None, scrollable=None, long_clickable=None, password=None, selected=None, bounds=None):
	closeKeyboard(udid)
	if ss != False:
		TakeScreenshot(udid)
	filename = GrabUiAutomator(udid)
	xmldoc = minidom.parse(filename)
	itemlist = xmldoc.getElementsByTagName('node')
	ListOfBounds = {}
	rotAmt = 0
	PreviousCorrect = 0
	f = []
	for e in locals().keys():
		if locals()[e] != None:
			f.append(locals()[e])
	print("Finding {}".format(f[0]))
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
		if Correct > 0 and resultNum != None:
			rotAmt = rotAmt + 1
			if rotAmt == resultNum:
				Bounds = GetBounds(Bounds)
				InputRandomBound(udid, Bounds, addx=addx, addy=addy)
				return Bounds
		PreviousCorrect = Correct
	try:
		print Bounds
	except:
		print("Error on {}".format(f[0]))
		print("Retrying...")
		time.sleep(10)
		filename = GrabUiAutomator(udid)
		xmldoc = minidom.parse(filename)
		itemlist = xmldoc.getElementsByTagName('node')
		ListOfBounds = {}
		rotAmt = 0
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
			if Correct > 0 and resultNum != None:
				rotAmt = rotAmt + 1
				if rotAmt == resultNum:
					Bounds = GetBounds(Bounds)
					InputRandomBound(udid, Bounds, addy)
					return Bounds
			PreviousCorrect = Correct
	Bounds = GetBounds(Bounds)
	InputRandomBound(udid, Bounds, addy)
	return Bounds

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

def InputRandomBound(udid, Bounds, addy=0, addx=0):
	print ("Addx: {} Addy: {}".format(addx, addy))
	A = str(random.randint(Bounds[1], Bounds[3]) - addy)
	B = str(random.randint(Bounds[0], Bounds[2]) + addx)
	print('sudo adb -s {} shell input tap {} {}'.format(udid, B, A))
	runCommand('sudo adb -s {} shell input tap {} {}'.format(udid, B, A))

def runCommand(command, forcesudo=False):
	if 'sudo' in command.lower():
		command = command.replace('sudo ', '')
	if ELEVATED == True or forcesudo == True:
		os.system('sudo {}'.format(command))
	else:
		os.system('{}'.format(command))

def InputText(udid, text, delay=False):
	if delay != True:
		text = str(text).replace("\n", " ")
		text = str(text).replace(' ', '%s')
		runCommand('adb -s {} shell input text {}'.format(udid, text))
	else:
		for letters in text:
			runCommand('adb -s {} shell input text {}'.format(udid, letters))
			time.sleep(random.randint(10, 30) * .01)

def turnDownVolume(udid):
	for i in range(10):
		runCommand('sudo adb -s {} shell input keyevent 25'.format(udid))

def ClearCache(udid, app):
	runCommand('sudo adb -s {} shell pm clear {}'.format(udid, app))

def ForceClose(udid, app):
	runCommand('sudo adb -s {} shell am force-stop {}'.format(udid, app))

def StartApplication(udid, app):
	runCommand("sudo adb -s {} shell monkey -p {} -c android.intent.category.LAUNCHER 1".format(udid, app))

def resetApplication(udid, app):
	if app in str(currentApps(udid)):
		ForceClose(udid, app)
	runCommand("sudo adb -s {} shell monkey -p {} -c android.intent.category.LAUNCHER 1".format(udid, app))

def valOnScreen(udid, string):
	if string not in str(interactions.GrabUiAutomator(udid)):
		return False
	else:
		return True
