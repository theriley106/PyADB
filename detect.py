from __future__ import division
import os
import numpy
from PIL import Image
import pyautogui

def FindPlayButton(Xbutton, Screenshot):
	coordinates = pyautogui.locate(Xbutton, Screenshot, grayscale=True)
	a = None
	if coordinates is not None:
		XCoordinate = ((int(coordinates[0])) + (int(coordinates[2] / 2)))
		YCoordinate = ((int(coordinates[1])) + (int(coordinates[3] / 2)))
		a = str(XCoordinate) + " " + str(YCoordinate)
	return a
