import os
import interactions
from PIL import Image
import imageFeatures
import PIL
import random
import time
import psutil

def TakeScreenshot():
	basewidth = 750/10
	picurl = interactions.TakeScreenshot(udid)
	img = Image.open(picurl)
	area = (45, 337, 1375, 2150)
	cropped_img = img.crop(area)
	wpercent = (basewidth/float(cropped_img.size[0]))
	hsize = int((float(cropped_img.size[1])*float(wpercent)))
	cropped_img = cropped_img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
	cropped_img.show()
	time.sleep(2)
	for proc in psutil.process_iter():
		if proc.name() == "display":
			proc.kill()
	return picurl


def Like():
	interactions.Scroll(udid, 23, 1300, 1350, 1100)

def NotLike():
	interactions.Scroll(udid, 1350, 1100, 23, 1300)

for i in range(100):
	a = TakeScreenshot()
	print(a)
	a = imageFeatures.GrabAttractiveness(a)
	if  a > 60:
		Like()
	else:
		NotLike()