import os
import interactions

class automation(object):
	def __init__(self, udid, app, ss=False):
		print('Initiated New Thread With: {}\nAutomation: {}'.format(udid, app))
		self.udid = udid
		self.app = app