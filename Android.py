import os
import random
from xml.dom import minidom
import sys
import time
import Pickling
reload(sys)
sys.setdefaultencoding("utf-8")


def MuteSound(udid):
	#Pixi glitz
	StartApplication(udid, 'com.android.music')
	for i in range(10):
		os.system('adb -s {} shell input keyevent 25'.format(udid))
	print('muted volume')
	
def RemoveLock(udid):
	#Pixi glitz
	os.system('adb -s {} shell am start -a android.app.action.SET_NEW_PASSWORD'.format(udid))
	time.sleep(1)
	e = UiAutomatorToList(udid)
	for i in range(len(e)):
		if str(e[i][2]) == "None":
			InputRandomBound(udid, e[i][-4:])
			print('removed lock screen')

def ClickStayAwake(udid):
	#Pixi glitz
	os.system('adb -s {} shell am start -n com.android.settings/.DevelopmentSettings'.format(udid))
	time.sleep(3)
	e = UiAutomatorToList(udid)
	for i in range(len(e)):
		if str(e[i][0]) == "android:id/checkbox" and str(e[i][1]) == "android.widget.CheckBox" and str(e[i-2][2]) == "Screen will never sleep while charging" and str(e[i][7]) == "false":
			InputRandomBound(udid, e[i][-4:])
			print('clicked stay awake')
def ConnectToWifi(udid, wifi, password, proxy=False):
	#Pixi glitz
	os.system('adb -s {} shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings'.format(udid))
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
	
	print('connected to {}'.format(wifi))

def ClearCache(udid, app):
	os.system('adb -s {} shell pm clear {}'.format(udid, app))
	
def CheckConnected(udid):
	connected = []
	os.system('adb devices > t.txt')
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
	os.system('adb -s {} reboot'.format(udid))
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
	os.system('adb -s {} shell am start -n com.android.settings/.DevelopmentSettings'.format(udid))
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
	
def CheckWifiConnection(udid):
	Connected = False
	os.system('adb -s {} shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings'.format(udid))
	lis = UiAutomatorToList(udid)
	for i in range(len(lis)):
		if "Connected" in str(lis[i]):
			print('{} is connected to: {}'.format(udid, lis[i-1][2]))
			Connected = True
	return Connected

def RemoveUSBBlock(udid):
	os.system('adb -s {} shell am start -n com.android.settings/.DevelopmentSettings'.format(udid))
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
def LoginGooglePlay(udid, username, password):
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

def UiAutomatorToDict(udid):
	information = []
	SavedFile = 'XML/' + str(random.randint(99999,100000000)) + '.xml'
	Command = "adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {} > t.txt".format(udid, udid, SavedFile)
	os.system(Command)
	xmldoc = minidom.parse(SavedFile)
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
	Command = "adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {} > t.txt".format(udid, udid, SavedFile)
	os.system(Command)
	return SavedFile
def LoadingScreen(udid):
	found = False
	loading = 'com.android.vending:id/downloading_bytes'
	for results in UiAutomatorToList(udid):
		for result in results:
			if result == 'com.android.vending:id/downloading_bytes':
				found = True
	return found

def UiAutomatorToList(udid):
	try:
		information = []
		SavedFile = 'XML/' + str(random.randint(99999,100000000)) + '.xml'
		Command = "adb -s {} pull $(adb -s {} shell uiautomator dump | grep -oP '[^ ]+.xml') {} > t.txt".format(udid, udid, SavedFile)
		os.system(Command)
		xmldoc = minidom.parse(SavedFile)
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
	except BaseException as exp:
		print(exp)
	try:
		os.remove(SavedFile)
		return information
	except:
		pass
def XMLtoList(uiautomatorfile):
	#returns a list of lists
	information = []
	xmldoc = minidom.parse(uiautomatorfile)
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

def InputRandomBound(udid, Bounds):
	A = str(random.randint(Bounds[1], Bounds[3]))
	B = str(random.randint(Bounds[0], Bounds[2]))
	print('adb -s {} shell input tap {} {}'.format(udid, B, A))
	os.system('adb -s {} shell input tap {} {}'.format(udid, B, A))
def ReturnRandomBound(udid, Bounds):
	A = str(random.randint(Bounds[1], Bounds[3]))
	B = str(random.randint(Bounds[0], Bounds[2]))
	return [B, A]
def KillADB():
	os.system('adb kill-server')
def RestartADB(Devices):
	KillADB()
	for devices in Devices:
	   ConnectDevice(devices) 
def ConnectDevice(ip):
	os.system('adb connect {}'.format(ip))
def Rotate(udid):
	os.system('adb -s {} shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0'.format(udid))
def ForceClose(udid, app):
	os.system('adb -s {} shell am force-stop {}'.format(udid, app))
def SetBrightness(udid):
	os.system('adb -s {} shell settings put system screen_brightness 0'.format(udid))
def KeycodePower(udid):
	Command = 'adb -s ' + udid + " shell input keyevent 26"
	os.system(str(Command))

def TakeScreenshot(udid):
	screenshot = str(udid) + '.png'
	Command = "adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + str(screenshot)
	os.system(str(Command))
	return screenshot
def StartApplication(udid, app):
	Command = 'adb -s ' + udid + " shell monkey -p " + str(app) + " -c android.intent.category.LAUNCHER 1"
	os.system(str(Command))
def ConnectedDevices(sudo=None):
	connected = []
	if sudo == None:
		Command = 'adb kill-server'
		os.system(str(Command))
		os.system('adb devices')
		os.system('adb devices > t.txt')
		with open('t.txt') as f:
			lines = f.read().splitlines()
		lines.remove(lines[-1])
		lines.remove(lines[0])
		for i in lines:
			a = str(i).partition('\tdevic')[0]
			connected.append(a)
		os.remove('t.txt')
	else:
		Command = 'sudo adb kill-server'
		os.system(str(Command))
		os.system('sudo adb devices')
		os.system('sudo adb devices > t.txt')
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
		os.system('adb -s {} shell input swipe {} {} {} {}'.format(udid, sx, sy, ex, ey))
	else:
		os.system('adb -s {} shell input swipe {} {} {} {} {}'.format(udid, sx, sy, ex, ey, Delay))
def DetermineFinished(udid):
	#This determines if you're at the end of a list
	EndOfList = False
	List1 = UiAutomatorToList(udid)
	os.system('adb -s {} shell input swipe 150 320 0 0 2000'.format(udid))
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
	os.system('adb -s {} install {}'.format(udid, apk))
def InputText(udid, text):
	os.system('adb -s {} shell input text {}'.format(udid, text))

def ClickButton(udid, button):
	File = GrabUiAutomator(udid)
	CurrentScreen = XMLtoList(File)
	for parts in CurrentScreen:
		for part in parts:
			if str(part) == str(button):
				bounds = parts[-4:]
				InputRandomBound(udid, bounds)

def KeycodeUnknown(udid):
	os.system("adb -s {} shell input keyevent 0".format(udid))
def KeycodeMenu(udid):
	os.system("adb -s {} shell input keyevent 1".format(udid))
def KeycodeSoft_Right(udid):
	os.system("adb -s {} shell input keyevent 2".format(udid))
def KeycodeHome(udid):
	os.system("adb -s {} shell input keyevent 3".format(udid))
def KeycodeBack(udid):
	os.system("adb -s {} shell input keyevent 4".format(udid))
def KeycodeCall(udid):
	os.system("adb -s {} shell input keyevent 5".format(udid))
def KeycodeEndcall(udid):
	os.system("adb -s {} shell input keyevent 6".format(udid))
def Keycode0(udid):
	os.system("adb -s {} shell input keyevent 7".format(udid))
def Keycode1(udid):
	os.system("adb -s {} shell input keyevent 8".format(udid))
def Keycode2(udid):
	os.system("adb -s {} shell input keyevent 9".format(udid))
def Keycode3(udid):
	os.system("adb -s {} shell input keyevent 10".format(udid))
def Keycode4(udid):
	os.system("adb -s {} shell input keyevent 11".format(udid))
def Keycode5(udid):
	os.system("adb -s {} shell input keyevent 12".format(udid))
def Keycode6(udid):
	os.system("adb -s {} shell input keyevent 13".format(udid))
def Keycode7(udid):
	os.system("adb -s {} shell input keyevent 14".format(udid))
def Keycode8(udid):
	os.system("adb -s {} shell input keyevent 15".format(udid))
def Keycode9(udid):
	os.system("adb -s {} shell input keyevent 16".format(udid))
def KeycodeStar(udid):
	os.system("adb -s {} shell input keyevent 17".format(udid))
def KeycodePound(udid):
	os.system("adb -s {} shell input keyevent 18".format(udid))
def KeycodeDpad_Up(udid):
	os.system("adb -s {} shell input keyevent 19".format(udid))
def KeycodeDpad_Down(udid):
	os.system("adb -s {} shell input keyevent 20".format(udid))
def KeycodeDpad_Left(udid):
	os.system("adb -s {} shell input keyevent 21".format(udid))
def KeycodeDpad_Right(udid):
	os.system("adb -s {} shell input keyevent 22".format(udid))
def KeycodeDpad_Center(udid):
	os.system("adb -s {} shell input keyevent 23".format(udid))
def KeycodeVolume_Up(udid):
	os.system("adb -s {} shell input keyevent 24".format(udid))
def KeycodeVolume_Down(udid):
	os.system("adb -s {} shell input keyevent 25".format(udid))
def KeycodePower(udid):
	os.system("adb -s {} shell input keyevent 26".format(udid))
def KeycodeCamera(udid):
	os.system("adb -s {} shell input keyevent 27".format(udid))
def KeycodeClear(udid):
	os.system("adb -s {} shell input keyevent 28".format(udid))
def KeycodeA(udid):
	os.system("adb -s {} shell input keyevent 29".format(udid))
def KeycodeB(udid):
	os.system("adb -s {} shell input keyevent 30".format(udid))
def KeycodeC(udid):
	os.system("adb -s {} shell input keyevent 31".format(udid))
def KeycodeD(udid):
	os.system("adb -s {} shell input keyevent 32".format(udid))
def KeycodeE(udid):
	os.system("adb -s {} shell input keyevent 33".format(udid))
def KeycodeF(udid):
	os.system("adb -s {} shell input keyevent 34".format(udid))
def KeycodeG(udid):
	os.system("adb -s {} shell input keyevent 35".format(udid))
def KeycodeH(udid):
	os.system("adb -s {} shell input keyevent 36".format(udid))
def KeycodeI(udid):
	os.system("adb -s {} shell input keyevent 37".format(udid))
def KeycodeJ(udid):
	os.system("adb -s {} shell input keyevent 38".format(udid))
def KeycodeK(udid):
	os.system("adb -s {} shell input keyevent 39".format(udid))
def KeycodeL(udid):
	os.system("adb -s {} shell input keyevent 40".format(udid))
def KeycodeM(udid):
	os.system("adb -s {} shell input keyevent 41".format(udid))
def KeycodeN(udid):
	os.system("adb -s {} shell input keyevent 42".format(udid))
def KeycodeO(udid):
	os.system("adb -s {} shell input keyevent 43".format(udid))
def KeycodeP(udid):
	os.system("adb -s {} shell input keyevent 44".format(udid))
def KeycodeQ(udid):
	os.system("adb -s {} shell input keyevent 45".format(udid))
def KeycodeR(udid):
	os.system("adb -s {} shell input keyevent 46".format(udid))
def KeycodeS(udid):
	os.system("adb -s {} shell input keyevent 47".format(udid))
def KeycodeT(udid):
	os.system("adb -s {} shell input keyevent 48".format(udid))
def KeycodeU(udid):
	os.system("adb -s {} shell input keyevent 49".format(udid))
def KeycodeV(udid):
	os.system("adb -s {} shell input keyevent 50".format(udid))
def KeycodeW(udid):
	os.system("adb -s {} shell input keyevent 51".format(udid))
def KeycodeX(udid):
	os.system("adb -s {} shell input keyevent 52".format(udid))
def KeycodeY(udid):
	os.system("adb -s {} shell input keyevent 53".format(udid))
def KeycodeZ(udid):
	os.system("adb -s {} shell input keyevent 54".format(udid))
def KeycodeComma(udid):
	os.system("adb -s {} shell input keyevent 55".format(udid))
def KeycodePeriod(udid):
	os.system("adb -s {} shell input keyevent 56".format(udid))
def KeycodeAlt_Left(udid):
	os.system("adb -s {} shell input keyevent 57".format(udid))
def KeycodeAlt_Right(udid):
	os.system("adb -s {} shell input keyevent 58".format(udid))
def KeycodeShift_Left(udid):
	os.system("adb -s {} shell input keyevent 59".format(udid))
def KeycodeShift_Right(udid):
	os.system("adb -s {} shell input keyevent 60".format(udid))
def KeycodeTab(udid):
	os.system("adb -s {} shell input keyevent 61".format(udid))
def KeycodeSpace(udid):
	os.system("adb -s {} shell input keyevent 62".format(udid))
def KeycodeSym(udid):
	os.system("adb -s {} shell input keyevent 63".format(udid))
def KeycodeExplorer(udid):
	os.system("adb -s {} shell input keyevent 64".format(udid))
def KeycodeEnvelope(udid):
	os.system("adb -s {} shell input keyevent 65".format(udid))
def KeycodeEnter(udid):
	os.system("adb -s {} shell input keyevent 66".format(udid))
def KeycodeDel(udid):
	os.system("adb -s {} shell input keyevent 67".format(udid))
def KeycodeGrave(udid):
	os.system("adb -s {} shell input keyevent 68".format(udid))
def KeycodeMinus(udid):
	os.system("adb -s {} shell input keyevent 69".format(udid))
def KeycodeEquals(udid):
	os.system("adb -s {} shell input keyevent 70".format(udid))
def KeycodeLeft_Bracket(udid):
	os.system("adb -s {} shell input keyevent 71".format(udid))
def KeycodeRight_Bracket(udid):
	os.system("adb -s {} shell input keyevent 72".format(udid))
def KeycodeBackslash(udid):
	os.system("adb -s {} shell input keyevent 73".format(udid))
def KeycodeSemicolon(udid):
	os.system("adb -s {} shell input keyevent 74".format(udid))
def KeycodeApostrophe(udid):
	os.system("adb -s {} shell input keyevent 75".format(udid))
def KeycodeSlash(udid):
	os.system("adb -s {} shell input keyevent 76".format(udid))
def KeycodeAt(udid):
	os.system("adb -s {} shell input keyevent 77".format(udid))
def KeycodeNum(udid):
	os.system("adb -s {} shell input keyevent 78".format(udid))
def KeycodeHeadsethook(udid):
	os.system("adb -s {} shell input keyevent 79".format(udid))
def KeycodeFocus(udid):
	os.system("adb -s {} shell input keyevent 80".format(udid))
def KeycodePlus(udid):
	os.system("adb -s {} shell input keyevent 81".format(udid))
def KeycodeMenu(udid):
	os.system("adb -s {} shell input keyevent 82".format(udid))
def KeycodeNotification(udid):
	os.system("adb -s {} shell input keyevent 83".format(udid))
def KeycodeSearch(udid):
	os.system("adb -s {} shell input keyevent 84".format(udid))
def KeycodeTagLast(udid):
	os.system("adb -s {} shell input keyevent 85".format(udid))
def KeycodeBack(udid):
	os.system('adb -s {} shell input keyevent 4'.format(udid))
def KeycodeHome(udid):
	os.system('adb -s {} shell input keyevent 3'.format(udid))
def TouchScreen(udid, x, y):
	os.system('adb -s {} shell input tap {} {}'.format(udid, x, y))
def KeycodeEnter(udid):
	os.system('adb -s {} shell input keyevent 66'.format(udid))
def KeycodeSearch(udid):
	os.system('adb -s {} shell input keyevent 84'.format(udid))
def KeycodeMenu(udid):
	os.system('adb -s {} shell input keyevent 82'.format(udid))
def KeycodeSpace(udid):
	os.system('adb -s {} shell input keyevent 62'.format(udid))
def KeycodeClear(udid):
	os.system('adb -s {} shell input keyevent 28'.format(udid))
def KeycodePower(udid):
	os.system('adb -s {} shell input keyevent 26'.format(udid))
def KeycodeVolumeUp(udid):
	os.system('adb -s {} shell input keyevent 24'.format(udid))
def KeycodeVolumeDown(udid):
	os.system('adb -s {} shell input keyevent 25'.format(udid))
def KeycodeSoftRight(udid):
	os.system('adb -s {} shell input keyevent 2'.format(udid))
def KeycodeUp(udid):
	os.system('adb -s {} shell input keyevent 19'.format(udid))
def KeycodeDown(udid):
	os.system('adb -s {} shell input keyevent 20'.format(udid))
def KeycodeLeft(udid):
	os.system('adb -s {} shell input keyevent 21'.format(udid))
def KeycodeRight(udid):
	os.system('adb -s {} shell input keyevent 22'.format(udid))
def KeycodeCenter(udid):
	os.system('adb -s {} shell input keyevent 22'.format(udid))


