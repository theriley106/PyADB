import detect
img1 = []
img2 = []
img3 = []
img4 = []
img5 = []
img6 = []
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
			Command = detect.FindPlayButton(img3, screenshot)
			if Command is not None:
				Screen = ""
				return Screen
			if Command is None:
				Command = detect.FindPlayButton(img4, screenshot)
				if Command is not None:
					Screen = ""
					return Screen
				if Command is None:
					Command = detect.FindPlayButton(img5, screenshot)
					if Command is not None:
						Screen = ""
						return Screen
					if Command is None:
                        Command = detect.FindPlayButton(img6, screenshot)
                        if Command is not None:
                                Screen = ""
                                return Screen
                        if Command is None:
                                Screen = None
                                return Screen
