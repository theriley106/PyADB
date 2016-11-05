# ADB For All
Multi-Device Android Automation using Python

# [Install the Android Device Bridge](http://lifehacker.com/the-easiest-way-to-install-androids-adb-and-fastboot-to-1586992378)




# Clone Github Repo

    git clone https://github.com/theriley106/ADB_For_All.git

# Install Requirements
	cd ~/ADB_For_All
    pip install -r requirements.txt
# Add Device ID's to Main.Py

    ADB Devices
Add the output in the following format to Main.py

    Devices = ["AXDDISOOSADFSD"]
or add wireless devices using:

    Devices = ["AXDIIDSAOIJFADSDA:XXXX"]
	#Where XXXX is the Port Number
You can also combine wired devices with wireless devices using:

    Devices = ["AXIDSFDOIJFFASFDSD, "FADFSFDASFAS:XXXX", "DFSADSAFSAFDSADASD"]



# Basic Functions  

Restart ADB and connect all devices:

    def RestartADB(Devices):
		Command = 'sudo adb kill-server'
		os.system(str(Command))
		for devices in Devices:
		   ConnectDevice(devices) 

Take Device Screenshots:

    def TakeScreenshot(udid):
		screenshot = str(udid) + '.png'
		Command = "sudo adb -s " + str(udid) + " shell screencap -p | sed 's/\r$//' > " + screenshot
		os.system(str(Command))
Emulate Button Presses:

    def KeycodeEnter(udid):
		Command = 'sudo adb -s ' + udid + " shell input keyevent 66"
		os.system(str(Command))

[List of Valid Keyevents](http://stackoverflow.com/questions/7789826/adb-shell-input-events)

Emulate Touch Screen Presses:

    def TouchScreen(udid, x, y):
		Command = 'sudo adb -s ' + udid + " shell input tap " + str(x) + " " + str(y)
		os.system(str(Command))
Start Application:

    def StartApplication(udid, app):
		Command = 'sudo adb -s ' + udid + " shell monkey -p " + str(app) + " -c android.intent.category.LAUNCHER 1"
		os.system(str(Command))

# Advanced Functions

Find Buttons Based on Image:

*Main.py*

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

*detect.py*

    def FindPlayButton(Xbutton, Screenshot):
		coordinates = pyautogui.locate(Xbutton, Screenshot, grayscale=True)
		a = None
		if coordinates is not None:
			XCoordinate = ((int(coordinates[0])) + (int(coordinates[2] / 2)))
			YCoordinate = ((int(coordinates[1])) + (int(coordinates[3] / 2)))
			a = str(XCoordinate) + " " + str(YCoordinate)
		return a

Detect Current Screen:

*screen.py*

    def WhichScreen(screenshot):
	    Command = detect.FindPlayButton(img1, screenshot)
				if Command is not None:
					Screen = ""
					return Screen
				if Command is None:
                    Command = detect.FindPlayButton(img2, screenshot)
                    if Command is not None:
                        Screen = ""
                        return Screen
                    if Command is None:
                        Screen = None
                        return Screen