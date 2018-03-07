import os
import time
import random
import PIL
from PIL import Image
import re
import face_recognition

def sendSystemCommand(command):
	os.system('{} > tmp'.format(command))
	return open('tmp', 'r').read()

def returnDevices():
	Devices = sendSystemCommand('adb devices')
	return re.findall('\n(\w+)', str(Devices))

def currentApps(device):
	return sendSystemCommand('adb -s {} shell dumpsys activity'.format(device))

def ForceClose(udid, app):
	runCommand('adb -s {} shell am force-stop {}'.format(udid, app))

def startApp(device, app):
	sendSystemCommand('adb -s {} shell monkey -p {} -c android.intent.category.LAUNCHER 1'.format(device, app))

def screenshot(device):
	sendSystemCommand("adb -s {} shell screencap -p | sed 's/\r$//'".format(device))

def dumpUiAutomator(device):
	os.system("adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') tmp".format(device, device))
	return open('tmp', 'r').read()

def findBounds(device):
	Ui = dumpUiAutomator(device)
	Ui = Ui.partition('resource-id="" class="android.widget.FrameLayout" package="com.tinder" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="')[2]
	Ui = Ui.partition('"')[0]
	Ui = re.findall('(\d+)', str(Ui))
	return Ui

def crop(coords, filename):
	coords = tuple([float(i) for i in coords])
	im = Image.open('tmp')
	im = im.crop(coords)
	im.save(filename)
	return filename

def randomBounds(coords, like):
	coords = tuple([float(i) for i in coords])
	StartYBound = str(random.randint(coords[1], coords[3]))
	StartXBound = str(float(random.randint(coords[0], coords[2])) / 5)
	EndXBound = str(coords[2] - int((float(random.randint(coords[0], coords[2])) / 5)))
	EndYBound = str(random.randint(coords[1], coords[3]))
	if like == True:
		return (StartXBound, StartYBound, EndXBound, EndYBound)
	else:
		return (EndXBound, StartYBound, StartXBound, EndYBound)

if __name__ == "__main__":
	for device in returnDevices():
		startApp(device, 'com.tinder')
		time.sleep(5)
		while 'com.tinder' in currentApps(device):
			coords = findBounds(device)
			screenshot(device)
			image = face_recognition.load_image_file(crop(coords, 'save.png'))
			if len(face_recognition.face_locations(image)) > 1:
				bounds = randomBounds(coords, False)
			else:
				bounds = randomBounds(coords, True)
			os.system('adb -s {} shell input swipe {}'.format(device, ' '.join(bounds)))
			#time.sleep(random.randint(1,7))

