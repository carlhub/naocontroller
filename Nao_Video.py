#!/usr/bin/python
# -*- coding: utf-8 -*- 	
#The coding line above it is necessary in order to
#deal with Japanese characters. Python will default 
#to ASCII as standard encoding if no other encoding 
#hints are given.


"""
	This file contains functions for the NAO robot using the NAOqi Framework.
	Video File.
	
	Indiana University 2018
"""



from PyQt4.QtGui import QWidget, QImage, QApplication, QPainter
#from naoqi import ALProxy

# To get the constants relative to the video.
import vision_definitions
# comment code properly
import time
import Tkinter as tk# Python 2 import Tkinter as tk
import almath
import argparse
import sys
import math
import msvcrt
import motion
import naoqi
import qi
import sys

from naoqi import ALProxy
from naoqi import ALModule




#global PORT_GLOBAL
PORT2 = 9559 # port number


def print_title():
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n\tWelcome to Nao Controller!\n\t(Enter Commands)"
	print "\n\tIndiana University Bloomington\n\tSummer Research 2018\n\tUSA"
	print "\n\tVideo File"
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n"
#######################################################################################

# Code taken form online example

#	VIDEO CLASS	##########GLOBAL_VID_RESOLUTION
# Parameter ID Name 	ID Value 	Description
# kQQQQVGA 	8 	Image of 40*30px
# kQQQVGA 	7 	Image of 80*60px
# k4VGA 	3 	Image of 1280*960px
# kVGA 		2 	Image of 640*480px
# kQVGA 	1 	Image of 320*240px
# kQQVGA 	0 	Image of 160*120px

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
		self.setWindowTitle('Nao Video')

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
		self.startTimer(000.0001)#(100)


	def _registerImageClient(self, IP, PORT):
		"""
		Register our video module to the robot.
		"""
		self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
		# this set the video quality, higher quality consumes more bandwidth
		#resolution = vision_definitions.k4VGA#1280*960
		#resolution = vision_definitions.kVGA
		resolution = vision_definitions.kQVGA  # 320 * 240 Default [WiFi: Bad, is delay] [*TEST_ Seems ok with newer ['router':'tp-link ac1200',PC':'Eth','NAO':'WiFi'] ]
		#resolution = vision_definitions.kQQVGA #__USE_THIS_SETTING__			[WiFi: Good] [Ethernet: Ok @30fps]
		#resolution = vision_definitions.kQQQVGA  # 			[WiFi: Good*, no delay @30fps, Fastest,Poor_resol] 
		#resolution = vision_definitions.kQQQQVGA #low
		colorSpace = vision_definitions.kRGBColorSpace
		#self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, FPS)
		#self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 25)
		self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, int(GLOBAL_FPS))

		#::TEST
		GLOBAL_VID_RESOLUTION = int(resolution)
		#print("::resolution___Printout__::vision_definitions.k4VGA::"),vision_definitions.k4VGA
		#print("::resolution___Printout__::vision_definitions.kQQVGA::"),vision_definitions.kQQVGA
		print ("::resolution VAR::"), resolution
		
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
		#self._image = QImage(self._alImage[6],200,200,QImage.Format_RGB888)#,100,100,QImage.Format_RGB888)


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

###############################################################################

# This program will start video
# Enter 9 to exit program

def main(robotIP,PORT=9559):
	print "\n\n"
	print "\t##################"
	print "\tVideo Started."
	print "\t##################"
	print "\n"	
	while True:
		input=raw_input("\n\t**Enter 9 to exit:  ")
		if(int(input) ==9):
			break
			
#######################################################################################

if __name__ == "__main__":				
		
	# Print the App title
	print_title()	
	
	robotIP = "192.168.0.100"
	ROBOT_IP_GLOBAL = robotIP
	PORT = 9559
	PORT_GLOBAL = PORT
	GLOBAL_FPS = 30		
	videoChoice = 1 # ("Enable Video? (1:YES  2:NO)")
	
	# This comes from example and helps video work
	if(str(videoChoice) == "1"):
		#GLOBAL_FPS = raw_input("Enter desired FPS (Default 30fps):  ") # Disabled
		if(int(GLOBAL_FPS) > 10):
			print "::fps=::",GLOBAL_FPS
		else:
			GLOBAL_FPS = 30
			print "::fps::", GLOBAL_FPS
		#VIDEO
		print "::VIDEO_ON"
		IP = robotIP ##
		CameraID = 0
		app = QApplication(sys.argv)
		myWidget = ImageWidget(IP, PORT, CameraID)
		myWidget.show()
	else:
	       print "::No_VIDEO"       
		   	
	main(robotIP)

