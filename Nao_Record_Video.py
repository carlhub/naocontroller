#!/usr/bin/python
# -*- coding: utf-8 -*- 	
#The coding line above it is necessary in order to
#deal with Japanese characters. Python will default 
#to ASCII as standard encoding if no other encoding 
#hints are given.


"""
	This file contains functions for the NAO robot using the NAOqi Framework.
	Functions: move head, arms, legs, and other joints. Can be used with remote
	control through infrared. Desigedn for network connections. Captures live 
	camer feed and displays video in various formats. Run this script using
	Python and user must specify IP address of NAO. Text menu will display
	avialable options.

	
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
##import tty
##import termios
##import keyboard
from naoqi import ALProxy
from naoqi import ALModule


#### Global Varibales ###
global PARALLEL_TASKS #none False # Talk and walk simultaneously
global POSTURE_PROXY_GLOBAL
global ROBOT_IP_GLOBAL
global PORT_GLOBAL
global GLOBAL_FPS
global GLOBAL_VID_RESOLUTION

#global PORT_GLOBAL
PORT2 = 9559 # port number
#################################################
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

###############################################################################
def printCommands(robotIP):	#Print menu 
	print "\n"
	print "\n\t********************************"
	print "\n\t[::CONNECTED_TO_ADDRESS==]", robotIP	
	print "\t[::FPS==>                  ]", GLOBAL_FPS
	print "\t[::QUALITY==>              ]", GLOBAL_VID_RESOLUTION
	print ""
	print "\tCOMMAND LIST:\n"

	print "\t[1: Video Record]"
	print "\n\t[9 : E X I T**]"	
	print "\n\t********************************"
	print "\n"
###############################################################################
	
###############################################################################


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
		self.startTimer(000.0001)#(100)


	def _registerImageClient(self, IP, PORT):
		"""
		Register our video module to the robot.
		"""
		self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
		# this set the video quality, higher quality consumes more bandwidth
		resolution = vision_definitions.k4VGA #1280*960
		resolution = vision_definitions.kVGA # [Ethernet: ok @20fps]
		resolution = vision_definitions.kQVGA  # 320 * 240 Default [WiFi: Bad, is delay] [Ethernet Good @30]
		resolution = vision_definitions.kQQVGA #TEST!!			[WiFi: Ok, small delay good@15fps good@30fps] [Ethernet: Ok @30fps]
		#resolution = vision_definitions.kQQQVGA  # 			[WiFi: Good*, no delay @30fps, Fastest,Poor_resol] 
		#resolution = vision_definitions.kQQQQVGA #low
		colorSpace = vision_definitions.kRGBColorSpace
		#self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, FPS)
		#self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 25)
		self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, int(GLOBAL_FPS))

		#::TEST
		GLOBAL_VID_RESOLUTION = int(resolution)
		print("::resolution___Printout__::vision_definitions.k4VGA::"),vision_definitions.k4VGA
		print("::resolution___Printout__::vision_definitions.kQQVGA::"),vision_definitions.kQQVGA
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
######################################################################
		
class myModule(naoqi.ALModule):
	def pythondatachanged(self, strVarName, value, strMessage):
		"""callback when data change"""
		print "Data changed on", strVarName, ": ", value, " ", strMessage
###############################################################################
	
def StiffnessOn(proxy):
	# We use the "Body" name to signify the collection of all joints
	pNames = "Body"
	pStiffnessLists = 1.0
	pTimeLists = 1.0
	proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
def StiffnessOff(proxy):
	# We use the "Body" name to signify the collection of all joints
	pNames = "Body"
	pStiffnessLists = 0.0
	pTimeLists = 1.0
	proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

###############################################################################

###############################################################################			
def getAnglesInfo(names,useSensors):
	# Puase to be able to read info
	time.sleep(1.00)
	
	MP = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT2)
	#test
	print "::getAnglesInfo__"
	anglesPrint = MP.getAngles(names,useSensors)
	print "::MP___________:",MP
	#print "::Name_________:",names
	#print "::angleLists___:",angleLists
	print "::angles_______:",anglesPrint
	

###############################################################################
def moveheadGoRight():
	print "::moveheadChange:"
	MP = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadYaw", -0.15, 0.05)#Right	
###############################################################################
def moveheadGoLeft():
	print "::moveheadChange:"
	MP = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadYaw", 0.15, 0.05)#Right	
###############################################################################
def moveheadGoUp():
	print "::moveheadChange:"
	MP = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadPitch", -0.15, 0.05)#Right	
###############################################################################
def moveheadGoDown():
	print "::moveheadChange:"
	MP = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadPitch", 0.15, 0.05)#Right		
	MP.wbEnableEffectorControl("Head", False)
###############################################################################

def movehead(direction,MP,yawTime=1.0,pitchTime=1.2,isAbsolute=True):
	#NAMES
	names	   = ["HeadYaw", "HeadPitch"]	
	
	#test
	print "::BEFORE_COMMAND_INIT_POSIT__"
	anglesPrint = MP.getAngles(names,False)
	print "::MP___________:",MP
	print "::Name_________:",names
	print "::anglesPrint__:",anglesPrint	
	


	if(direction == "left"):
		angleLists = [30.0*almath.TO_RAD,25.0*almath.TO_RAD]
	elif(direction == "center"):
		angleLists = [0.0*almath.TO_RAD,25.0*almath.TO_RAD]
	elif(direction == "right"):
		angleLists = [-30.0*almath.TO_RAD,25.0*almath.TO_RAD]
	elif(direction == "origin"):
		angleLists = [0*almath.TO_RAD,0*almath.TO_RAD]
	elif (direction == "up" or direction == 3):
		angleLists = [0*almath.TO_RAD,0*almath.TO_RAD]
	elif (direction == "down" or direction == 3):
		angleLists = [0*almath.TO_RAD,30.0*almath.TO_RAD]
	else:
		angleLists = [0.0,0.0]

	timeLists  = [yawTime, pitchTime]
	
	#test
	print "::ANGELS_FED_COMMAND::", angleLists
	
	#MP.post.angleInterpolation(names, angleLists, timeLists, isAbsolute) #'post' funciton allows paralled funtionality
	MP.post.angleInterpolation(names, angleLists, timeLists, isAbsolute) #'post' funciton allows paralled funtionality
	


###############################################################################
def videoEnabler(robotIP):
	#print ("Enable Video? (1:YES  2:NO)")
	#videoChoice = raw_input("Enable Video? (1:YES  2:NO)")
	#if(str(videoChoice) == "1"):
	#VIDEO
	#print "::VIDEO_ON"
	IP = robotIP ##"nao.local"  # Replace here with your NaoQi's IP address.
	#IP = "169.254.87.118"
	PORT = 9559
	CameraID = 0

	app = QApplication(sys.argv)
	myWidget = ImageWidget(IP, PORT, CameraID)
	myWidget.show()
	#sys.exit(app.exec_())
	##
##	else:
	print "::VIDEO_ON"      

def rotate(rx,ry,rz,t,mp,armSide):
    effector   = "RArm"
    effector   = armSide
    space      = motion.FRAME_ROBOT
    axisMask   = almath.AXIS_MASK_VEL    # just control position
    isAbsolute = True

    # Since we are in relative, the current position is zero
    currentPos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # Define the changes relative to the current position
    dx         =  0.00      # translation axis X (meters)
    dy         =  0.00      # translation axis Y (meters)
    dz         =  0.00      # translation axis Z (meters)
    dwx        =  rx      # rotation axis X (radians)
    dwy        =  ry      # rotation axis Y (radians)
    dwz        =  rz     # rotation axis Z (radians)
    targetPos  = [dx, dy, dz, dwx, dwy, dwz]

    # Go to the target and back again
    path       = [targetPos]
    times      = [t] # seconds

    mp.positionInterpolation(effector, 1, path,
                                      56, times, isAbsolute)


######################################################################
def randomMoveHead(robotIP, armSide):
	''' Example of a whole body head orientation control
	Warning: Needs a PoseInit before executing
			 Whole body balancer must be inactivated at the end of the script
	'''
	# Init proxies.
	# ALMotion, ALRobotPosturte Proxie is initialized in main()
	try:
		motionProxy = ALProxy("ALMotion", robotIP, 9559)
	except Exception, e:
		print "Could not create proxy to ALMotion"
		print "Error was: ", e

	try:
		postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
	except Exception, e:
		print "Could not create proxy to ALRobotPosture"
		print "Error was: ", e

	# Set NAO in Stiffness On
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	effectorName = "Head"

	# Active Head tracking
	isEnabled    = True
	motionProxy.wbEnableEffectorControl(effectorName, isEnabled)

	# Example showing how to set orientation target for Head tracking
	# The 3 coordinates are absolute head orientation in NAO_SPACE
	# Rotation in RAD in x, y and z axis

	# X Axis Head Orientation feasible movement = [-20.0, +20.0] degree
	# Y Axis Head Orientation feasible movement = [-75.0, +70.0] degree
	# Z Axis Head Orientation feasible movement = [-30.0, +30.0] degree

	targetCoordinateList = [
	[+20.0,  00.0,  00.0], # target 0
	[-20.0,  00.0,  00.0], # target 1
	[ 00.0, +70.0,  00.0], # target 2
	[ 00.0, +70.0, +30.0], # target 3
	[ 00.0, +70.0, -30.0], # target 4
	[ 00.0, -75.0,  00.0], # target 5
	[ 00.0, -75.0, +30.0], # target 6
	[ 00.0, -75.0, -30.0], # target 7
	[ 00.0,  00.0,  00.0], # target 8
	]

	# wbSetEffectorControl is a non blocking function
	# time.sleep allow head go to his target
	# The recommended minimum period between two successives set commands is
	# 0.2 s.
	for targetCoordinate in targetCoordinateList:
		targetCoordinate = [target*math.pi/180.0 for target in targetCoordinate]
		motionProxy.wbSetEffectorControl(effectorName, targetCoordinate)
		time.sleep(3.0)

	# Deactivate Head tracking
	isEnabled    = False
	motionProxy.wbEnableEffectorControl(effectorName, isEnabled)		
######################################################################
def moveArm(robotIP,armSide):
##	RArm
	''' Example showing a path of two positions
	Warning: Needs a PoseInit before executing
	'''

	# Init proxies.
	try:
			motionProxy = ALProxy("ALMotion", robotIP, 9559)
	except Exception, e:
			print "Could not create proxy to ALMotion"
			print "Error was: ", e

	try:
			postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
	except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e

	# Set NAO in Stiffness On
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	drx = 1.0
	drz = 1.0
	rotate(drx,-2.0,0.0,2.0,motionProxy,armSide)
	rotate(3.0,-2.0,-1.0,1.0,motionProxy,armSide)
	# rotate(1,-2.0,-1.0,1.0,motionProxy)
	# rotate(-drx,0.0,0.0,motionProxy)

	postureProxy.goToPosture("StandInit", 0.5)	
	
######################################################################
def moveBody(robotIP):
	print "movebody"
	#from naoqi import ALProxy
##	try:
##		motion = ALProxy("ALMotion", robotIP, 9559)
##		motion.moveInit()
##		motion.moveTo(0.5, 0, 0)
##	except Exception, e:
##		print e
#
	motion = ALProxy("ALMotion", robotIP, 9559)
	# Set NAO in Stiffness On
	StiffnessOn(motion)	
	motion.moveInit()
	#motion.post.moveTo(0.5, 0, 0)
	#motion.post.moveTo(0.0,0.25,0)
	motion.post.moveTo(0.80,0.0,0.)
	#motion.post.moveTo(0,side-step-left,ROTATE-LEFT)
#
######################################################################	
	# MOVE BODY 
	#motion.post.moveTo(FORWARD,side-step-left,ROTATE-LEFT)___in_+__POSITIVE_SYMBOL
def moveBodyRotateLeft(robotIP): 
	motion = ALProxy("ALMotion", robotIP, 9559)
	# Set NAO in Stiffness On
	StiffnessOn(motion)	
	motion.moveInit()
	motion.post.moveTo(0.0,0.0,0.8)# ROTATE LEFT
######################################################################
	# MOVE BODY 
	#motion.post.moveTo(FORWARD,side-step-left,ROTATE-LEFT)___in_+__POSITIVE_SYMBOL
def moveBodyRotateRight(robotIP): 
	motion = ALProxy("ALMotion", robotIP, 9559)
	# Set NAO in Stiffness On
	StiffnessOn(motion)	
	motion.moveInit()
	motion.post.moveTo(0.0,0.0,-0.8)# ROTATE LEFT
######################################################################
	#motion.post.moveTo(FORWARD,side-step-left,ROTATE-LEFT)___in_+__POSITIVE_SYMBOL
def moveBodyStepFRW(robotIP): 
	motion = ALProxy("ALMotion", robotIP, 9559)
	# Set NAO in Stiffness On
	StiffnessOn(motion)	
	motion.moveInit()
	motion.post.moveTo(0.25,0.0,-0.0)# STEP 
######################################################################
	#motion.post.moveTo(FORWARD,side-step-left,ROTATE-LEFT)___in_+__POSITIVE_SYMBOL
def moveBodyStepBKW(robotIP): 
	motion = ALProxy("ALMotion", robotIP, 9559)
	# Set NAO in Stiffness On
	StiffnessOn(motion)	
	motion.moveInit()
	motion.post.moveTo(-0.25,0.0,-0.0)# STEP 
######################################################################
def moveBodyAndTalk(robotIP):
	try:
		motion = ALProxy("ALMotion", robotIP, 9559)
		#tts    = ALProxy("ALTextToSpeech", robotIP, 9559)
		# Set NAO in Stiffness On
		StiffnessOn(motion)		
		motion.moveInit()
		motion.post.moveTo(0.5, 0, 0)
		speakFunction("Hi, my name is Nao. Now Foward Motor Movement is Enabled")
	except Exception, e:
		print e
######################################################################
def userInputSpeak(robotIP):
	print "::speak"
	motion = ALProxy("ALMotion", robotIP, 9559)
	#tts    = ALProxy("ALTextToSpeech", robotIP, 9559)
	# Set NAO in Stiffness On
	StiffnessOn(motion)
	#input = raw_input("Enter sentence (9:EXIT):  ")
	input = raw_input("Enter sentence:  ") # (9:EXIT):  ")
	speakFunction(input)
	StiffnessOff(motion)
	#if (input is not None):
		#print"::not_note_::entered==",input
	# while True:
		# #print"Enter 9:EXIT"
		# input = raw_input("Enter sentence (9:EXIT):  ")
		# if(input is not None):
			# print "::input_NOT_none::"
			# print input
			# #tts.say(input)
			# speakFunction(input)
		# if(input == "9"):
			# print("::break::input_IS_9_::input=9")
			# break
	# StiffnessOff(motion)
######################################################################
def speakFunction(text_dialog):#,PARALLEL_TASKS):
	#,PARALLEL_TASKS is defined GLOBAl
	tts = ALProxy("ALTextToSpeech",robotIP,PORT2)
	#tts.say("I am Ready")	
	#print "hi"
	if(PARALLEL_TASKS):
		print "::PARALLEL_TASKS=ON"
		tts.post.say(text_dialog)
	else:
		print "::PARALLEL_TASKS=OFF"
		tts.say(text_dialog)
###############################################################################
def getNaoNetworkInfo():
	print "N/A"
	#alconnman = ALProxy("ALConnectionManager", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#print "network state: " + alconnman.state()
	#print "::NETWORK_INFO::" + alconnman.NetworkInfo()
	#print alconnman.toALValue()
	#netInfo = ALProxy("NetworkInfo", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	#print netInfo.toALValue()
###############################################################################
def getNaoVideo():
	try:
		camProxy = ALProxy("ALVideoDevice",ROBOT_IP_GLOBAL,PORT_GLOBAL)
	except Exception,e:
		print "Error when creating vision proxy:"
		print e
	
	print str(e)
	#exit(1)
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
	
	#Change Voice
	tts.setVoice('naoenu')	#English
							#Japanese 'maki_n16'
	
	# Enable TalkToSpeech, Set Language, Say text

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
	
	tts.setLanguage('English') # reset to English
###############################################################################

#
# This file is use to record Vidoe
# This code is currently not working
#

#0 = kQQVGA, 1 = kQVGA, 2 = kVGA 640x480
def videoRecord():
	try:
		videoRecorderProxy = ALProxy("ALVideoRecorder", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "Error when creating ALVideoRecorder proxy:"
		print str(e)
	#exit(1)
	
	#START
	videoRecorderProxy.setFrameRate(30.0)#(10.0)
	videoRecorderProxy.setResolution(2) # Set resolution to VGA (640 x 480)
	# We'll save a  video record in /home/nao/recordings/cameras/
	videoRecorderProxy.post.startRecording("/home/nao/recordings/cameras", 'naovideo')
	#videoRecorderProxy.startRecording("/mnt/naousb/naorec", "test")
	print "Video record started."

	#REC_TIME= 60.0*60.0*(5.0/60.0) # 5 Min
	REC_TIME= 60.0*60.0*(1.0/60.0) # 1 Min
	time.sleep(REC_TIME)#(5)

	videoInfo = videoRecorderProxy.stopRecording()
	print "Video was saved on the robot: ", videoInfo[1]
	print "Total number of frames: ", videoInfo[0]
###############################################################################
def main(robotIP,faceSize,PORT=9559):
	
	# print (bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.OKGREEN) #bcolors.ENDC
	# print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
	
	try:		
		# START
		initRemoteInputFlag = True
		session = qi.Session()
		session.connect("tcp://"+ robotIP + ":" + str(PORT))
		ba_service = session.service("ALBasicAwareness")
		motion_service = session.service("ALMotion")
		motion_service.wakeUp()
		ba_service.startAwareness()
##				print "Take some time to play with the robot"
##				time.sleep(50)
		#print "Stopping BasicAwareness"
		ba_service.stopAwareness()
		motion_service.rest()

##		# ALMotion Start Setup  #
##		motionProxy = ALProxy("ALMotion", robotIP, PORT)
##		motionProxy.setStiffnesses("Head", 1.0)
##		motionProxy.wbEnableEffectorControl("Head", True)
	except Exception, e:
		print "::ERROR::ALBasicAwareness,ALMotion", e


	# ALMotion Start Setup	#
	try:				
		motionProxy = ALProxy("ALMotion", robotIP, PORT)
##		motionProxy.setStiffnesses("Head", 1.0)
##		motionProxy.wbEnableEffectorControl("Head", True)		
	except Exception, e:
		print "::ALMotion__ error", e
	# ALTracker
##		try:
##				trackerProxy = ALProxy("ALTracker", robotIP, PORT)
##		except Exception, e:
##				print "Could not create proxy to ALTracker"
##				print "Error was: ", e

	# # ALInfrared
	# try:
		# #print("start infrared")
		# lirc = ALProxy("ALInfrared", robotIP, PORT)
		# lirc.initReception(10)				  
		# lirc.exit() #RESET
		# lirc = ALProxy("ALInfrared", robotIP, PORT)
		# lirc.initReception(10)				  
# ##		
# ##				lircProxy = naoqi.ALProxy("ALInfrared", robotIP, PORT)				  
# ##				lircProxy.sendRemoteKey("My_TV_name", "KEY_POWER")
# ##				pythonModule = myModule("pythonModule")
# ##				memProxy = naoqi.ALProxy("ALMemory")#, robotIP, PORT)
# ##				memoryProxy.subscribeToEvent("InfraRedRemoteKeyReceived", "pythonModule", "pythondatachanged")
# ##				lirc.sendRemoteKey("My_TV_name", "KEY_POWER")				 
		# print("::infrared OK")
	# except Exception, e:
		# print "Error was: ", e
	# ALMemory							
	try:
		memoryProxy = ALProxy("ALMemory", robotIP, PORT)
		memoryProxy.subscribeToEvent("InfraRedRemoteKeyReceived", "pythonModule", "pythondatachanged")
		memoryProxy.unsubscribeToEvent("InfraRedRemoteKeyReceived", "pythonModule")##, "pythondatachanged")	  
		#print "::memoryProxy:: no error"
	except Exception, e:
		print "Error when creating memory proxy:"
		print str(e)		

	# ALRobotPosture Code for standing, sitting, or other positions
	try:
		postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
	except Exception, e:
		print "Could not create proxy to ALRobotPosture"
		print "Error was: ", e		
	#
	#
	try:
		postureProxy = ALProxy("ALRobotPosture", robotIP, PORT_GLOBAL)
	except Exception, e:
		print "::ERR_"
		print e
		
	# init VARIABLES
	POSTURE_PROXY_GLOBAL = postureProxy


				# dont touch! I have little understanding of what this actual does, but it is necessary
##		memoryProxy.subscribeToEvent("InfraRedRemoteKeyReceived", "pythonModule", "pythondatachanged")
##		StiffnessOn(motionProxy)
				# First, wake up.
				# motionProxy.wakeUp()
##		motionProxy.setStiffnesses("Head", 1.0)

				# Add target to track.
	targetName = "Face"
##		  faceWidth = faceSize
##		trackerProxy.registerTarget(targetName, faceWidth)

				# Then, start tracker.
##		trackerProxy.track(targetName)
##		trackerProxy.stopTracker() # TEST TEMP Disalbe tracker

	#print "ALTracker successfully started, now show your face to robot!"
	#print "Use Ctrl+c to stop this script."


	# initiate variables for while statements
	target = [0.0, 0.0, 0.0]
	curpos = 'KEY_POWER'
	newpos = 'KEY_1'
	firstCenter = True

	bootUp = True
	#		START  Move	 #
##	print("::START::voice")
##	target = "origin"
##	movehead(target,motionProxy)
	#		Start Speak
	#tts = ALProxy("ALTextToSpeech",robotIP,PORT)
	#speakFunction("I am Ready")	
	try:
		# run the entire dialogue first
		while True:
			# First check if POWER button is in memory



##
			printCommands(robotIP)
			keyboard = raw_input("Enter Command (Numbers #):  ")
			print "*Entered= ", keyboard
			remoteInput = [0,0,0,0,0] # TEMP VAR
			#print "::KEYBOARD==", keyboard
##
			

			if (keyboard  == "0"):
				print("::0")
				# target = "left"
				# newpos="KEY_1"
			# elif (keyboard == "2"):
				# target = "center"
				# newpos="KEY_2"				
			# elif (keyboard == "3"):
				# target = "right"
				# newpos="KEY_3"				
			# elif (keyboard == "4"):
				# target = "origin"
				# newpos="KEY_PLAY"				
			# elif (keyboard == "5"):
				# target = "center"
				# newpos="KEY_STOP"
			# elif (keyboard == "6"):
				# speakFunction("Hello")
			# elif (keyboard == "7"):
				# speakFunction("Good Job")
			# elif (keyboard == "8"):
				# speakFunction("Thank You")
			# elif (keyboard=="10"):
				# postureProxy.goToPosture("Sit", 1.0)			
				# print "Sit"
			# elif (keyboard=="11"):
				# print "Stand up"				
				# postureProxy.goToPosture("Stand", 1.0)
			# elif (keyboard  == "12"):
				# postureProxy.goToPosture("StandInit", 1.0)
			# elif (keyboard == "13"):
				# postureProxy.goToPosture("SitRelax", 1.0)
			# elif (keyboard == "14"):
				# postureProxy.goToPosture("StandZero", 1.0)		
			# elif (keyboard == "15"):
				# postureProxy.goToPosture("LyingBelly", 1.0)		
			# elif (keyboard == "16"):
				# postureProxy.goToPosture("Crouch", 1.0)
			# elif (keyboard == "17"):
				# videoEnabler(robotIP)
			# elif (keyboard == "18"):
				# randomMoveHead(robotIP)
			# elif (keyboard == "19"):
				# moveArm(robotIP,"RArm")
			# elif (keyboard == "20"):
				# moveArm(robotIP,"LArm")
			# elif (keyboard == "21"):
				# #target = "origin"
				# speakFunction("That object is called a ball.")
				# speakFunction("The color of the ball is yellow.")
			# elif (keyboard == "22"):
				# #target = "origin"
				# speakFunction("That object is called a ball.")
				# speakFunction("The color of the ball is red.")
			# elif (keyboard == "23"):
				# #target = "origin"
				# speakFunction("That object is called a triangle.")
				# speakFunction("The color of the object is blue.")
			# elif (keyboard == "24"):
				# #target = "origin"
				# speakFunction("That object is called a box.")
				# speakFunction("The color of the box is orange.")
			# elif (keyboard == "25"):
				# moveBody(robotIP)
			# elif (keyboard == "26"):
				# moveBodyAndTalk(robotIP)
			# elif (keyboard == "27"): # user types in words or sentences
				# userInputSpeak(robotIP)
			# elif (keyboard == "28"):
				# moveBodyRotateLeft(robotIP)
			# elif (keyboard == "29"):
				# moveBodyRotateRight(robotIP)
			# elif (keyboard == "30"):
				# moveBodyStepFRW(robotIP)
			# elif (keyboard == "31"):
				# moveBodyStepBKW(robotIP)		
			# elif (keyboard == "32"):
				# #moveheadLeft()
				# print "::key_32"
				# target = "left"
				# newpos="KEY_1"
			# elif (keyboard == "33"):
				# print "::moveheadChange:"
				# newpos="33"
				# #moveheadChange()
			# elif (keyboard == "41"):#r,l,u,d
				# #newpos="41"
				# moveheadGoLeft()
			# elif (keyboard == "42"):#r,l,u,d
				# #newpos="42"
				# moveheadGoRight()
			# elif (keyboard == "43"):#r,l,u,d
				# #newpos="43"
				# moveheadGoUp()
			# elif (keyboard == "44"):#r,l,u,d
				# #newpos="44"
				# moveheadGoDown()
			# elif (keyboard == "50"):
				# print"stop"
				# postureProxy.stopMove()
			# elif (keyboard == "51"):
				# print "rest"
				# motionProxy.rest()
			# elif (keyboard == "52"):
				# print "::SUMMARY::"
				# print motionProxy.getSummary()
			# elif (keyboard == "60"):
				# getNaoNetworkInfo()
			# elif (keyboard == '70'):
				# naoTalks()
			elif (keyboard == '1'):
				videoRecord()
			elif (remoteInput[2] == 'KEY_POWER' or keyboard=="9"):
				break
				
			
			

			
			
			

				
				

				
		
			if(keyboard=="9911" or keyboard=="9927"):#Only if Standing!
				print "::Standing"
			elif(curpos == newpos):
				print("::HEY!:: same position!!")
				#motionProxy.rest()
				#time.sleep(0)
			else:
				motionProxy.setStiffnesses("Head", 1.0)
				motionProxy.wbEnableEffectorControl("Head", True)
				movehead(target,motionProxy)
				motionProxy.wbEnableEffectorControl("Head", False)
				curpos = newpos


		#print remoteInput
		#print ("::end of while")

	except KeyboardInterrupt:
		print
		print "Interrupted by user"
		print "Stopping..."

	# Stop tracker.
	if remoteInput[2] == 'KEY_POWER':
		print("Power hit")		
	motionProxy.rest()
	#tts = ALProxy("ALTextToSpeech",robotIP,PORT)
	#speakFunction("good bye ")
	#tts.say("Good Bye")	

print "ALTracker stopped."
#######################################################################################

if __name__ == "__main__":

	print "\n"
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n\tWelcome to Nao Controller!\n\t()"
	print "\n\tIndiana University Bloomington\n\tSummer Research 2018\n\tUSA"
	print "\n\tVideo Recorder"
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n"

	robotIP = "192.168.0.100"
	# if it doesn't work try using the direct IP
					# robotIP = number
	#sys.exit()	
	#init
	ROBOT_IP_GLOBAL = robotIP
	PORT = 9559
	PORT_GLOBAL = PORT
	GLOBAL_FPS = 30
	#print ("Enable Video? (1:YES  2:NO)")
	#videoChoice = raw_input("Enable Video? (1:YES  2:NO)")
	videoChoice = 2 #default off
	if(str(videoChoice) == "1"):
		userInputFPS = raw_input("Enter desired FPS (Default 30fps):  ")
		if(int(userInputFPS) > 10):
			print "::fps=::",userInputFPS
			GLOBAL_FPS=userInputFPS
		else:
			GLOBAL_FPS = 30
			print "::fps::", GLOBAL_FPS
		#VIDEO
		print "::VIDEO_ON"
		IP = robotIP ##"nao.local"  # Replace here with your NaoQi's IP address.
		#IP = "169.254.87.118"
		#PORT = 9559
		CameraID = 0
		#CameraID = 1

		app = QApplication(sys.argv)
		myWidget = ImageWidget(IP, PORT, CameraID)
		myWidget.show()
		#sys.exit(app.exec_())
		##
	else:
	       print "::No_VIDEO"       
		   
	# PARALLEL_TASKS
	#userChoice = raw_input("Enable Parallel Tasks (i.e. talk and walk same time)? (1:YES  2:NO)")
	userChoice = 1 #default yes
	if(str(userChoice) == "1"):
		#
		print "::_ON"
		PARALLEL_TASKS = True
	else:
		print "::_OFF"	
		PARALLEL_TASKS = False
	# PARALLEL_TASKS
	
	# init global
	postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
	POSTURE_PROXY_GLOBAL = postureProxy #"init"
	GLOBAL_VID_RESOLUTION = 0
	
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="nao.local",
		help="Robot ip address.")
	parser.add_argument("--port", type=int, default=9559,
		help="Robot port number.")
	parser.add_argument("--facesize", type=float, default=0.173,
		help="Face width.")

	args = parser.parse_args()


	# used to determine if the robot Ip is able to connect
	if len(sys.argv) <= 1:
		print "Usage python motion_wbEffectorControlHead.py robotIP (optional default: 127.0.0.1)"
	else:
		robotIP = sys.argv[1]

	main(robotIP,args.facesize)


