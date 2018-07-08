#!/usr/bin/python
# -*- coding: utf-8 -*- 	
#The coding line above it is necessary in order to
#deal with Japanese characters. Python will default 
#to ASCII as standard encoding if no other encoding 
#hints are given.


"""
	This code is used to manipulate the had movement of Nao. Connect to Nao
	by using its IP address. Press button located on Nao's chest to learn its
	IP. When this program runs Nao will say "Ready".
		
	Indiana University 2018	
"""




# This is a tiny example that shows how to show live images from Nao using PyQt.
# You must have python-qt4 installed on your system.
#

#import sys

from PyQt4.QtGui import QWidget, QImage, QApplication, QPainter
#from naoqi import ALProxy

# To get the constants relative to the video.
import vision_definitions
# comment code properly
import time
import almath
import argparse
import sys
import math
import msvcrt
import motion
import naoqi
import qi
import sys
import random
##import tty
##import termios
##import keyboard
from naoqi import ALProxy
#from naoqi import ALModule
#from Tkinter import Frame
from Tkinter import *

###############################################################################
def print_title():
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n\tWelcome to Nao Controller!\n\t(Enter Commands)"
	print "\n\tIndiana University Bloomington\n\tSummer Research 2018\n\tUSA"
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n"
#### Global Varibales #########################################################
global PARALLEL_TASKS #none False # Talk and walk simultaneously
global POSTURE_PROXY_GLOBAL
global ROBOT_IP_GLOBAL
global PORT_GLOBAL
global MOTION_PROXY_GLOBAL
global GLOBAL_TIME_MOVE_DELAY
global GLOBAL_CHANGE_FRACTION
global WORD_LIST_JAP
global WORD_LIST_ENG
#global PORT_GLOBAL
PORT2 = 9559 # port number
###############################################################################
###############################################################################	

#	VIDEO CLASS	##########
# kQQQQVGA 	8 	Image of 40*30px
# kQQQVGA 	7 	Image of 80*60px
# kQQVGA 	0 	Image of 160*120px
# kQVGA 	1 	Image of 320*240px
####
class ImageWidget(QWidget):
	"""
	Tiny widget to display camera images from Naoqi.
	"""
	def __init__(self, IP, PORT, CameraID, parent=None):
		"""
		Initialization.
		"""
		QWidget.__init__(self, parent)
		self._image = QImage()
		self.setWindowTitle('Nao')

		self._imgWidth = 320
		self._imgHeight = 240
		self._cameraID = CameraID
		self.resize(self._imgWidth, self._imgHeight)

		# Proxy to ALVideoDevice.
		self._videoProxy = None

		# Our video module name.
		self._imgClient = ""

		# This will contain this alImage we get from Nao.
		self._alImage = None

		self._registerImageClient(IP, PORT)

		# Trigget 'timerEvent' every 100 ms.
		self.startTimer(0.51)#(100)


	def _registerImageClient(self, IP, PORT):
		"""
		Register our video module to the robot.
		"""
		self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
		# this set the video quality, higher quality consumes more bandwidth
		#resolution = vision_definitions.k4VGA#1280*960
		#resolution = vision_definitions.kVGA
		resolution = vision_definitions.kQVGA  # 320 * 240
		resolution = vision_definitions.kQQVGA
		#resolution = vision_definitions.kQQQVGA  # 
		#resolution = vision_definitions.kQQQQVGA #low
		colorSpace = vision_definitions.kRGBColorSpace
		self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 30)

		# Select camera.
		self._videoProxy.setParam(vision_definitions.kCameraSelectID,
								  self._cameraID)


	def _unregisterImageClient(self):
		"""
		Unregister our naoqi video module.
		"""
		if self._imgClient != "":
			self._videoProxy.unsubscribe(self._imgClient)


	def paintEvent(self, event):
		"""
		Draw the QImage on screen.
		"""
		painter = QPainter(self)
		painter.drawImage(painter.viewport(), self._image)


	def _updateImage(self):
		"""
		Retrieve a new image from Nao.
		"""
		self._alImage = self._videoProxy.getImageRemote(self._imgClient)
		self._image = QImage(self._alImage[6],			 # Pixel array.
							 self._alImage[0],			 # Width.
							 self._alImage[1],			 # Height.
							 QImage.Format_RGB888)


	def timerEvent(self, event):
		"""
		Called periodically. Retrieve a nao image, and update the widget.
		"""
		self._updateImage()
		self.update()


	def __del__(self):
		"""
		When the widget is deleted, we unregister our naoqi video module.
		"""
		self._unregisterImageClient()
######################################################################


def key(event):
	#frame.focus_set()
	"shows key or tk code for the key"
	
	if event.keysym == 'Escape':
		root.destroy()
	if event.char == event.keysym:
		# normal number and letter characters
		print( 'Normal Key %r' % event.char )
		# if(event.char == 1):
			# #print "::VIDEO_ON"
			# IP = robotIP ##"nao.local"  # Replace here with your NaoQi's IP address.
			# #IP = "169.254.87.118"
			# #PORT = 9559
			# CameraID = 0

			# app = QApplication(sys.argv)
			# myWidget = ImageWidget(IP, PORT, CameraID)
			# myWidget.show()
	elif len(event.char) == 1:
		# charcters like []/.,><#$ also Return and ctrl/key
		print( 'Punctuation Key %r (%r)' % (event.keysym, event.char) )
	else:
		# f1 to f12, shift keys, caps lock, Home, End, Delete ...
		print( 'Special Key %r' % event.keysym )
		if(event.keysym == "Up"):
			print ("got ")
			moveheadGoUp(MOTION_PROXY_GLOBAL)
		if(event.keysym == "Down"):
			print ("got ")
			moveheadGoDown(MOTION_PROXY_GLOBAL)
		if(event.keysym == "Left"):
			print ("got ")
			moveheadGoLeft(MOTION_PROXY_GLOBAL)
		if(event.keysym == "Right"):
			print ("got ")		
			moveheadGoRight(MOTION_PROXY_GLOBAL)

###############################################################################
def callback(event):
	print "::callback::"
	frame.focus_set()
	print "clicked at", event.x, event.y
###############################################################################
	# Init proxies.
	try:
			motionProxy = ALProxy("ALMotion", robotIP, 9559)
	except Exception, e:
			print "Could not create proxy to ALMotion"
			print "Error was: ", e

	
###############################################################################
###############################################################################
def moveHeadOrigin(MP):
	#angleLists = [0.0,0.0]
	#timeLists  = [yawTime, pitchTime]
	
	#test
	#print "::ANGELS_FED_COMMAND::", angleLists
	
	#MP.post.angleInterpolation(names, angleLists, timeLists, isAbsolute) #'post' funciton allows paralled funtionality
	MP.post.angleInterpolation("HeadPitch", 0.0, 1.0, True) #'post' funciton allows paralled funtionality
###############################################################################
###############################################################################
def moveheadGoRight(MP):
	print "::moveheadChange:"
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadYaw", -GLOBAL_CHANGE_FRACTION, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
def moveheadGoLeft(MP):
	print "::moveheadChange:"
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadYaw", GLOBAL_CHANGE_FRACTION, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
def moveheadGoUp(MP):
	print "::moveheadChange:"
	#MP = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadPitch", -.35, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
###############################################################################
def moveheadGoUpRandom(MP):
	print "::moveheadChange:"
	#MP = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadPitch", -0.35, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
def moveheadGoDown(MP):
	print "::moveheadChange:"
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadPitch", 0.35, GLOBAL_TIME_MOVE_DELAY)#Right		
	MP.wbEnableEffectorControl("Head", False)
###############################################################################	
###############################################################################

def naoTalks():
	textToSpeechProxy = ALProxy("ALTextToSpeech",ROBOT_IP_GLOBAL,PORT_GLOBAL)
	try:
		tts = ALProxy("ALTextToSpeech", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::error speech"
		print e 
	
	lang = tts.getAvailableLanguages()
	voices = str(tts.getAvailableVoices())
	print "Languages:"
	print lang
	#print str(lang)
	print "Voices"
	print voices #
	

	
###############################################################################
def naoTalksLangauage(tts,lang,text):
	langList = ['English','Japanese']
	
	if(lang is ''):
		lang = 0
	
	lang = int(lang) # set to int
	
	if(lang == 0):
		lang= langList[0]
	if(lang == 1):
		lang = langList[lang-1]
	if(lang == 2):
		lang = langList[lang-1]
	tts.setLanguage(lang)
	tts.say(text)
	#time.sleep(3.0)
	
	tts.setLanguage('English') # reset to English
###############################################################################
###############################################################################
# App title
print_title()


keyboard = raw_input("Enter IP: ")
if (keyboard is not None):
	robotIP=str(keyboard)
	#ROBOT_IP_GLOBAL = robotIP
	print "::entered=", robotIP
else:
	print "::entered::NONE"
	
#robotIP	= "192.168.0.100"
PORT = 9559		
PORT_GLOBAL = PORT
ROBOT_IP_GLOBAL = robotIP
GLOBAL_TIME_MOVE_DELAY = 0.20

# VALUE FOR CONTINGENT & NON CONTINGNT EXPERIEMNT 0.35 (UP/DOWN)
#GLOBAL_ROBOT_IP = robotIP
#GLOBAL_PORT = PORT

tts = ALProxy("ALTextToSpeech", ROBOT_IP_GLOBAL, PORT_GLOBAL)
motionProxy = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
motionProxy.setStiffnesses("Head", 1.0)
motionProxy.wbEnableEffectorControl("Head", True)
MOTION_PROXY_GLOBAL = motionProxy
GLOBAL_CHANGE_FRACTION = 0.20

#WORD_LIST_JAP = ['','','','','','','','','','','','']	   
WORD_LIST_ENG = ["Cat","Dog",
	"Elephant ","Bear",
	"Red","Green",
	"Apple","Strawberry",
	"Carrot","Pumpkin",
	"Bread","Eggs",
	"Kite","Jump rope",
	"Watch","Hat",
	"Mountain","Tree",
	"Triangle","Star",
	"Train","Plane","Bike",
	"Bee ","Snail "]

WORD_LIST_JAP = [
	" 猫",
	" 犬",
	" 象",
	" くま",
	" 赤",
	" 黄色",
	" 林檎",
	" イチゴ",
	" ニンジン",
	" カボチャ ",
	" パン ",
	" 卵 ",
	" 凧 ",
	" 縄跳び",
	" 時計",
	" 帽子",
	" 山",
	" 木",
	" 三角形",
	" 星形",
	" 模型",
	" 平面",
	" 自転車",
	" 蜂",
	" カタツムリ"]
root = Tk()



#TEST LOOP FOR TALKING

#time.sleep(2.00)
moveHeadOrigin(MOTION_PROXY_GLOBAL)
#naoTalksLangauage(tts,1,"CONTROL START ")

#array of all word lists



print( "Press a key (Escape key to exit):" )
frame = Frame(root, width=300, height=300)
frame.bind("<Up>", key)
frame.bind("<Down>", key)
frame.bind("<Left>", key)
frame.bind("<Right>", key)
frame.bind('<Button-1>',callback)
frame.pack()
root.mainloop()

# IP = robotIP ##"nao.local"  # Replace here with your NaoQi's IP address.
# CameraID = 0
# print sys.argv
# app = QApplication(sys.argv)
# myWidget = ImageWidget(IP, PORT, CameraID)
# myWidget.show()