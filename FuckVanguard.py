import ctypes
import os
import keyboard
import time
import win32api,win32gui
import mss
import PIL.ImageGrab
import PIL.Image
import winsound
import pyautogui
import threading
from interception import  *
from consts import *

S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size) # take a screenshot of the screen and return the size of the screenshot

bBhop = False
bTriggerbot = False
bSniperMode = False
bAutoMode = False
bAimLock = False
bStopThread = False
bRunning = False
bPressing = False

class Found(Exception):
	pass

class isSpectating(Exception):
	pass

class CColor:
	Red = '\033[91m'
	Green = '\u001b[32m'
	Yellow = '\u001b[33m'
	Blue = '\u001b[34m'
	Cyan = '\u001b[36m'
	White = '\033[0m'

def bhop():
	keyboard.press_and_release("space")
	keyboard.unhook_all()
	time.sleep(0.1)

def approx(r, g ,b):
	return 250 - 60 < r < 250 + 60 and 100 - 60 < g < 100 + 60 and 250 - 60 < b < 250 + 60

def isSpectating():
	try:
		spectating = pyautogui.locateOnScreen("isSpectate.png",confidence=0.8)
		if spectating is not None:
			print("spectating")
			raise isSpectating
		else:
			return False
	except isSpectating:
		return True


def triggerbot():
	img = grab()
	try:
		for x in range(0,20):
			for y in range(0,20):
				r,g,b = img.getpixel((x,y))
				if approx(r,g,b):
					raise Found
	except Found:
		ctypes.windll.user32.mouse_event(2,0,0,0,0)
		ctypes.windll.user32.mouse_event(4,0,0,0,0)
		if bSniperMode == True:
			time.sleep(0.3)
		elif bAutoMode == True:
			time.sleep(0.1)
		time.sleep(0.1)

def aimassist():
	global bAimLock
	c = interception()
	c.set_filter(interception.is_mouse,interception_mouse_state.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN.value)
	while True:
		hWnd = win32gui.FindWindow(None,"VALORANT  ")
		if(hWnd == win32gui.GetForegroundWindow()):
			device = c.wait()
			stroke = c.receive(device)
			img = aimlock_grab()
			try:
				for x in range(0,40):
					for y in range(0,40):
						r,g,b = img.getpixel((x,y))
						if approx(r,g,b):
							raise Found
			except Found:
				if type(stroke) is mouse_stroke:
					if(bAimLock == True):
						stroke.y = y
			c.send(device,stroke)
		else:
			device = c.wait()
			stroke = c.receive(device)
			c.send(device,stroke)
		#c._destroy_context()

def aimlock_grab():
	with mss.mss() as sct:
		box = (1270, 710, 1310, 750) # box of 20x20 pixel around the crosshair
		img = sct.grab(box)
		return PIL.Image.frombytes('RGB',img.size,img.bgra,'raw','BGRX')

def grab():
	with mss.mss() as sct:
		box = (1270, 710, 1290, 730) # box of 20x20 pixel around the crosshair
		img = sct.grab(box)
		return PIL.Image.frombytes('RGB',img.size,img.bgra,'raw','BGRX')

def printgui():
	os.system("cls")
	Color = CColor()
	print(f"{Color.Yellow}[*]Triggerbot: {Color.Green}{bTriggerbot}{Color.Yellow} [*]{Color.White}")
	print(f"{Color.Red} - Auto Mode: {Color.Green}{bAutoMode}{Color.Red}{Color.White}")
	print(f"{Color.Red} - Sniper Mode: {Color.Green}{bSniperMode}{Color.Red}{Color.White}\r\n")
	print(f"{Color.Yellow}[*]Bhop: {Color.Green}{bBhop}{Color.Yellow} [*]{Color.White}")
	print(f"{Color.Yellow}[*]Aim Assist: {Color.Green}{bAimLock}{Color.Yellow} [*]{Color.White}")

printgui()

while True:
	hWnd = win32gui.FindWindow(None,"VALORANT  ")
	if(hWnd == win32gui.GetForegroundWindow()):
		#bhop
		if(bBhop == True):
			if(keyboard.is_pressed("space")):
				bhop()

		if(bTriggerbot == True):
			triggerbot()
		if(bAimLock == True):
			if(bRunning == False):
				bRunning = True
				tAimLock = threading.Thread(target=aimassist)
				tAimLock.start()

	if(keyboard.is_pressed("ctrl + 4")):
		bAimLock = not bAimLock
		if(bAimLock == True):
			winsound.Beep(440, 75)
			winsound.Beep(700, 100)
		else:
			winsound.Beep(440, 75)
			winsound.Beep(200, 100)
		printgui()

	if(keyboard.is_pressed("ctrl + alt")):
		bTriggerbot = not bTriggerbot
		if(bTriggerbot == True):
			winsound.Beep(440, 75)
			winsound.Beep(700, 100)
		else:
			winsound.Beep(440, 75)
			winsound.Beep(200, 100)
		printgui()

	if(keyboard.is_pressed("ctrl + shift")):
		bBhop = not bBhop
		if(bBhop == True):
			winsound.Beep(440, 75)
			winsound.Beep(700, 100)
		else:
			winsound.Beep(440, 75)
			winsound.Beep(200, 100)
		printgui()

	if(keyboard.is_pressed("ctrl + 1")):
		bAutoMode = not bAutoMode
		if(bAutoMode == True):
			winsound.Beep(440, 75)
			winsound.Beep(700, 100)
		else:
			winsound.Beep(440, 75)
			winsound.Beep(200, 100)
		printgui()

	if(keyboard.is_pressed("ctrl + 2")):
		bSniperMode = not bSniperMode
		if(bSniperMode == True):
			winsound.Beep(440, 75)
			winsound.Beep(700, 100)
		else:
			winsound.Beep(440, 75)
			winsound.Beep(200, 100)
		printgui()

	if(keyboard.is_pressed("delete")):
		print("Have a great day !")
		os._exit(1)
