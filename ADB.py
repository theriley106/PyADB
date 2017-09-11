import os
import random
from xml.dom import minidom
import sys
import time
import threading
reload(sys)
sys.setdefaultencoding("utf-8")
global Elevated
Elevated = True
#set if you'd like to use to sudo


def runCommand(command):
	if Elevated == True:
		os.system('sudo {}'.format(command))
	else:
		os.system('{}'.format(command))

def RemoveLock(udid):
	#Pixi glitz
	runCommand('adb -s {} shell am start -a android.app.action.SET_NEW_PASSWORD'.format(udid))
	time.sleep(1)
	e = UiAutomatorToList(udid)
	for i in range(len(e)):
		if str(e[i][2]) == "None":
			InputRandomBound(udid, e[i][-4:])
			print('removed lock screen')
def GrabUiAutomator(udid):
	SavedFile = 'XML/' + str(udid) + '.xml'
	Command = "adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {} > t.txt".format(udid, udid, SavedFile)
	runCommand(Command)
	return SavedFile

def XMLtoList(xml):
	#returns a list of lists
	information = []
	xmldoc = minidom.parse(xml)
	itemlist = xmldoc.getElementsByTagName('node')
	for item in itemlist:
		ResourceID = item.attributes['resource-id'].value
		Class = item.attributes['class'].value
		Text = item.attributes['text'].value
		Package = item.attributes['package'].value
		Description = item.attributes['content-desc'].value
		Clickable = item.attributes['clickable'].value
		Checkable = item.attributes['checkable'].value
		Checked = item.attributes['checked'].value
		Enabled = item.attributes['enabled'].value
		Focused = item.attributes['focused'].value
		Focusable = item.attributes['focusable'].value
		Scrollable = item.attributes['scrollable'].value
		LongClick = item.attributes['long-clickable'].value
		Password = item.attributes['password'].value
		Selected = item.attributes['selected'].value
		TopX = GetBounds(item.attributes['bounds'].value)[0]
		TopY = GetBounds(item.attributes['bounds'].value)[1]
		BottomX = GetBounds(item.attributes['bounds'].value)[2]
		BottomY = GetBounds(item.attributes['bounds'].value)[3]
		information.append([ResourceID, Class, Text, Package, Description, Clickable, Checkable, Checked, Enabled, Focused, Focusable, Scrollable, LongClick, Password, Selected, TopX, TopY, BottomX, BottomY])
	return information

def XMLtoDict(xml):
	#Returns everything in a list of dictionaries
	xmldoc = minidom.parse(xml)
	itemlist = xmldoc.getElementsByTagName('node')
	for item in itemlist:
		try:
			xml = {
				'Index': item.attributes['index'].value, 
				'ResourceID': item.attributes['resource-id'].value, 
				'Class': item.attributes['class'].value, 
				'Text': item.attributes['text'].value, 
				'Package': item.attributes['package'].value, 
				'Description': item.attributes['content-desc'].value, 
				'Clickable': item.attributes['clickable'].value, 
				'Checkable': item.attributes['checkable'].value, 
				'Checked': item.attributes['checked'].value, 
				'Enabled': item.attributes['enabled'].value, 
				'Focused': item.attributes['focused'].value, 
				'Focusable': item.attributes['focusable'].value, 
				'Scrollable': item.attributes['scrollable'].value, 
				'LongClick': item.attributes['long-clickable'].value, 
				'Password': item.attributes['password'].value, 
				'Selected': item.attributes['selected'].value, 
				'TopX': GetBounds(item.attributes['bounds'].value)[0], 
				'TopY': GetBounds(item.attributes['bounds'].value)[1], 
				'BottomX': GetBounds(item.attributes['bounds'].value)[2], 
				'BottomY': GetBounds(item.attributes['bounds'].value)[3]
			}
			xml['Bounds'] = [xml["TopX"], xml["TopY"], xml["BottomX"], xml["BottomY"]]
			xml["Coordinate"] = [random.randint(xml['TopX'], xml['BottomX']), random.randint(xml['TopY'], xml['BottomY'])]
			information.append(xml)
		except:
			print(item)
	os.remove(SavedFile)
	return information




def ClickButton(button, udid=None):
	if udid != None:
		information = UiAutomatorToDict(udid)
		for info in information:
			for parts in CurrentScreen:
		for part in parts:
			if str(part) == str(button):
				bounds = parts[-4:]
				InputRandomBound(udid, bounds)
