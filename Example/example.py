import Main
import Screen
import detect
Devices = ["192.168.2.128:5555", "192.168.2.129:5555"]

Main.RestartADB(Devices)

def StartGooglePlay(udid):
	Main.RestartADB(udid)
	Main.StartApplication(udid, 'com.android.vending')
	Main.KeycodeDown(udid)
	Main.KeycodeDown(udid)
	Main.KeycodeRight(udid)
	Main.KeycodeEnter(udid)
	time.sleep(3)
	Main.PressButton(udid, 'install.png')
	time.sleep(120)
	Main.PressButton(udid, 'openbutton.png')
	time.sleep(30)
	Main.keycodeHome(udid)

threads = [threading.Thread(target=StartGooglePlay, args=(udid,)) for udid in Devices]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()

	
