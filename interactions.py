import os
import time
import threading
from xml.dom import minidom
import random

ELEVATED = False

def GrabUiAutomator(udid):
	SavedFile = 'XML/' + str(udid) + '.xml'
	Command = "sudo adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {} > /dev/null".format(udid, udid, SavedFile)
	runCommand(Command)
	return SavedFile

def get_num(x):
	return int(''.join(ele for ele in x if ele.isdigit()))

def click(udid, resultNum=None, text=None, resource_id=None, class_name=None, index_num=None, package=None, content_desc=None, checkable=None, checked=None, clickable=None, enabled=None, focusable=None, focused=None, scrollable=None, long_clickable=None, password=None, selected=None, bounds=None):
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
				InputRandomBound(udid, Bounds)
				return Bounds
		PreviousCorrect = Correct
	Bounds = GetBounds(Bounds)
	InputRandomBound(udid, Bounds)
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

def InputRandomBound(udid, Bounds):
	A = str(random.randint(Bounds[1], Bounds[3]))
	B = str(random.randint(Bounds[0], Bounds[2]))
	print('sudo adb -s {} shell input tap {} {}'.format(udid, B, A))
	runCommand('sudo adb -s {} shell input tap {} {}'.format(udid, B, A))

def runCommand(command, forcesudo=False):
	if 'sudo' in command.lower():
		command = command.replace('sudo ', '')
	if ELEVATED == True or forcesudo == True:
		os.system('sudo {}'.format(command))
	else:
		os.system('{}'.format(command))

def InputText(udid, text, delay=True):
	if delay != True:
		runCommand('adb -s {} shell input text {}'.format(udid, text))
	else:
		for letters in text:
			runCommand('adb -s {} shell input text {}'.format(udid, letters))
			time.sleep(random.randint(10, 30) * .01)
		