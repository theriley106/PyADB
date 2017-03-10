import sys
import threading
import os
sys.argv = sys.argv[1:]
global command
command = ""
global a

a = 0
for i in sys.argv:
	command = command + i + ' '
command = command.lower()
if 'adb' in str(command).lower():
	
	command = command.replace('adb', 'sudo adb -s UDID')



def ConnectedDevices():
	connected = []
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

def RunCommand(udid):
	global a
	global com
	com = command.replace('UDID', "{}".format(udid))
	os.system(com)
	a = a + 1

Devices = ConnectedDevices()
threads = [threading.Thread(target=RunCommand, args=(udid,)) for udid in Devices]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()

print("\n{} \n\nrun on {} devices".format(com, int(a)))