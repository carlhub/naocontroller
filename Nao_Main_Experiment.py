#!/usr/bin/python
# -*- coding: utf-8 -*- 	
#The coding line above it is necessary in order to
#deal with Japanese characters. Python will default 
#to ASCII as standard encoding if no other encoding 
#hints are given.


"""
	This file starts the Experiment. There will be two conditions. The first
	condition can be DIRECTED OR CONTINGENT. The second condition will be the
	other gaze.
	
	This file contains functions for the NAO robot using the NAOqi Framework.
	Functions: speak Japanese words, performs directed gaze, contingent gaze,
	automatically changes slides displayed on iPad. Japanese words are written
	using Kanji and Katakana. The NAOqi Framework is utilized.
			
	2018 Indiana University
	
"""


# Libraries imported
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
from Tkinter import *
from naoqi import ALProxy
from socket import *


#### Global Varibales #########################################################
global PARALLEL_TASKS #none False # Talk and walk simultaneously
global POSTURE_PROXY_GLOBAL
global ROBOT_IP_GLOBAL
global PORT_GLOBAL
global MOTION_PROXY_GLOBAL
global GLOBAL_TIME_MOVE_DELAY
global GLOBAL_CHANGE_FRACTION
global WORD_LIST_JAP
global WORD_LIST_JAP_1
global WORD_LIST_JAP_2
global WORD_LIST_ENG
global GLOBAL_SOCKET_CLIENT
PORT2 = 9559 # port number
global GLOBAL_IP
global GLOBAL_PORT

###############################################################################

def print_title():
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n\tWelcome to Nao Controller!\n\t(Enter Commands)"
	print "\n\tIndiana University Bloomington\n\tSummer Research 2018\n\tUSA"
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n"
###############################################################################
# This funciton changes slides displyed on the iPad
def changeSlideOnTabletDirection(command):
	command = str(command)#String

	#send the command through a socket
	# Not sure exactly how it works but its doing fine.
	if(GLOBAL_SOCKET_CLIENT is None):
		raw_input("Wait:::")
	GLOBAL_SOCKET_CLIENT.send(command)
	modifiedSentence = GLOBAL_SOCKET_CLIENT.recv(1024) # get from Server

###############################################################################
# This code below is used to detect keys form keybaord	
def key(event):
	#frame.focus_set()
	"shows key or tk code for the key"
	
	if event.keysym == 'Escape':
		root.destroy()
	if event.char == event.keysym:
		# normal number and letter characters
		print( 'Normal Key %r' % event.char )

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
# Function is used for keys
def callback(event):
	print "::callback::"
	frame.focus_set()
	print "clicked at", event.x, event.y
###############################################################################
	# HeadPitch = Up/Down
	# HeadYaw   = Left/right
	
def moveHeadOrigin(MP):
	MP.post.angleInterpolation("HeadPitch", 0.0, 1.0, True) #'post' funciton allows paralled funtionality
###############################################################################
def moveHeadOrigin2(MP):
	#MP.post.angleInterpolation(names, angleLists, timeLists, isAbsolute) #'post' funciton allows paralled funtionality
	MP.post.angleInterpolation("HeadPitch", 0.0, 1.0, True) #'post' funciton allows paralled funtionality
	MP.post.angleInterpolation("HeadYaw", 0.0, 1.0, True)
###############################################################################
def moveheadGoRight(MP):
	print "::moveheadChange:"
	#MP.changeAngles(names,changes,fractionMaxSpeed)
	MP.changeAngles("HeadYaw", -GLOBAL_CHANGE_FRACTION, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
def moveheadGoLeft(MP):
	MP.changeAngles("HeadYaw", GLOBAL_CHANGE_FRACTION, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
def moveheadGoUp(MP):
	#	changeAngles(JOINT_NAME, CHANGE_ANGLE_AMOUNT, FRACTION_OF_MAX_SPEED_FOR_MOVEMENT) 
	MP.changeAngles("HeadPitch", -0.35, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
	# NAO will face the Experimentor at beginning of Experiment
def moveheadExperiment1(MP):
	MP.changeAngles("HeadYaw", 3*GLOBAL_CHANGE_FRACTION, GLOBAL_TIME_MOVE_DELAY)# Move Left x3
	MP.changeAngles("HeadPitch", 2*-0.35, GLOBAL_TIME_MOVE_DELAY)				# Move Up x2
###############################################################################
def moveheadGoUpRandom(MP):
	print "::moveheadChange:"
	MP.changeAngles("HeadPitch", -0.35, GLOBAL_TIME_MOVE_DELAY)#Right	
###############################################################################
def moveheadGoDown(MP):
	#MP.changeAngles(names,changes,fractionMaxSpee)
	MP.changeAngles("HeadPitch", 0.45, GLOBAL_TIME_MOVE_DELAY)#Right		was 0.35
	MP.wbEnableEffectorControl("Head", False)
###############################################################################
def naoTalks():
	# Subscribe to NAO Speech function
	# Test To Speech is setup with Proxy: ALTextToSpeech
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
def naoTalksFeedText(text,lang=0):
	# Subscribe to NAO Speech function
	# Test To Speech is setup with Proxy: ALTextToSpeech	
	try:
		tts = ALProxy("ALTextToSpeech", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::error speech"
		print e 

	langList = ['English','Japanese']
	
	if(lang is ''):
		lang = 0		# Default Value
	
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
#def main(robotIP,faceSize,PORT=9559):
###############################################################################
def interact_Contingent(word_list):
	print "::"

	# Subscribe to NAO Speech function
	# Test To Speech is setup with Proxy: ALTextToSpeech	
	try:
		tts = ALProxy("ALTextToSpeech", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALTextToSpeech::",e
	
	try:												# Sets up proxy so head movement is enabled
		motionProxy = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALMotion::",e
		
	motionProxy.setStiffnesses("Head", 1.0)				# enables stiffness 
	motionProxy.wbEnableEffectorControl("Head", True)	# enables head movement
	MOTION_PROXY_GLOBAL = motionProxy
	moveHeadOrigin(MOTION_PROXY_GLOBAL)					# moves head to origin or face the participant
	counter = 0											# initialize the counter to 0
	# End Setup
	
														# 1=English
	naoTalksLangauage(tts,1,"Ready, Lets begin")		# Speech before condition starts
	while True:
		changeSlideOnTabletDirection('right')			# Change slide
		time.sleep(0.50)								# Pause
		naoTalksLangauage(tts,2,str(word_list[int(counter)])) #JAP Reading of Words 
		time.sleep(1.00)								# Pause
		time.sleep(1.0)									# Pause
		naoTalksLangauage(tts,2,str(word_list[int(counter)])) #JAP Reading of Words 
		time.sleep(3.5)									# Pause
		counter=int(counter) +1							# Counts total number of slides
		print "::SLIDE:  ",counter
		if(counter > 11):# 12 objects x2
			break	
	changeSlideOnTabletDirection('right')				# Change to last slide
	naoTalksLangauage(tts,1,"Great Job!. Now we are finished!")
	print "::STOP_TIMING::"	
	print "::End Method"
	motionProxy.setStiffnesses("Head", 0.0)				# Disable the head motors
	motionProxy.wbEnableEffectorControl("Head", False)	# Keep robot from getting hot
##############################################################################
def interact_NonContingent(word_list): #DIRECTED condition function definition

	# Subscribe to NAO Speech function
	# Test To Speech is setup with Proxy: ALTextToSpeech
	try:
		tts = ALProxy("ALTextToSpeech", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALTextToSpeech::",e
	
	try:
		motionProxy = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALMotion::",e
		
	motionProxy.setStiffnesses("Head", 1.0) # Stifness must be on in order to move the head
	motionProxy.wbEnableEffectorControl("Head", True) # Enabled to ensure head movement
	MOTION_PROXY_GLOBAL = motionProxy # Test later
	counter = 0
	# End Setup
	
	naoTalksLangauage(tts,1,"Ready, Lets begin!") # Tells robot to speak in English
	
	while True:
		print "::SLIDE:  ",counter
		time.sleep(2.00)						# Pause
		changeSlideOnTabletDirection('right')	# Changes slides
		time.sleep(0.50)						# Pause
		moveheadGoDown(MOTION_PROXY_GLOBAL) 	# Move Head down
		time.sleep(0.50)						# Pause
		naoTalksLangauage(tts,2,str(word_list[int(counter)])) #JAP Reading of Words 
		time.sleep(1.00)						# Pause
		naoTalksLangauage(tts,2,str(word_list[int(counter)])) #JAP Reading of Words 
		time.sleep(1.0)							# Pause
		moveHeadOrigin(MOTION_PROXY_GLOBAL)		# Move head to origin position
		counter=int(counter) +1					# Count the number of slides
		if(counter > 11):# 12 objects x2
			break
	changeSlideOnTabletDirection('right')		# Change slide
	naoTalksLangauage(tts,1,"Great Job!. Now we are finished!") 
	print "::STOP_TIMING::"	
	print "::End Method"
	motionProxy.setStiffnesses("Head", 0.0)
	motionProxy.wbEnableEffectorControl("Head", False)	
##############################################################################

def get_user_choice_interact():
	print""
	print""
	print""
	print""
	print""
	print""
	print""
	print""
	print""
	print "\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
	print""
	print ("\tWould you like to continue into next Condition?")
	print "\t[1] Yes. Start next condition."
	print "\t[2] No. Go back to main menu."
	print ""
	print""
	print""
	keyboard=raw_input("\t** Enter Choice (when ready):  ")
	return int(keyboard)	
##############################################################################

"""
	This function starts the experiment of running both conditions. User will 
	decide which condition goes first.
"""
def interact_BOTH_CONDITIONS(choice):	
	# 1:DIRECTED
	# 2:CONTINGENT
	
	# Setup VAR			
	if(choice==1):				# 1: DIRECTED, CONTINGENT
		condition_1_isOn=True
	else:
		condition_1_isOn=False 	# 2: CONTINGENT, DIRECTED	
	try:	# Setup Head Joint
		motionProxy = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALMotion::",e
		
	motionProxy.setStiffnesses("Head", 1.0)
	motionProxy.wbEnableEffectorControl("Head", True)
	# End Setup
	
	changeSlideOnTabletDirection('restart')	# Tells iPad to restart Slides
	
	# Center head location
	print "CONDITION:1"
	moveHeadOrigin(MOTION_PROXY_GLOBAL)
	if(condition_1_isOn):						# If True, start DIRECTED 
		interact_NonContingent(WORD_LIST_JAP_1) # DIRECTED, use Word List #1
	else:
		interact_Contingent(WORD_LIST_JAP_1)	# CONTINGENT, use Word List #1
	
	naoTalksFeedText("Whew. I don’t know about you, but I need a break. I’ll see you again in a few minutes")
	keyboard=get_user_choice_interact() 		# User hit Enter to continue
	print "::input is: ",keyboard
	if(keyboard==2):
		return
		
	print "CONDITION:2"						# This is condition 2
	naoTalksFeedText("Hi. Good to see you again.")
	naoTalksFeedText("Are you ready to learn the names of my other favorite 12 things. Can I get started.")
	keyboard=raw_input("Hit Enter to continue::")
	naoTalksFeedText("OK, I’ll start. Remember to repeat each word after me.")
	moveHeadOrigin(MOTION_PROXY_GLOBAL)			# center the head
	if(condition_1_isOn): 						# If True, then start CONTINGENT
		interact_Contingent(WORD_LIST_JAP_2)	# Send word list #2 to function
	else:
		interact_NonContingent(WORD_LIST_JAP_2)	# Send word list #2 to function	
	# End
	
	# Speech after finishing the experiment
	naoTalksFeedText("Thanks for letting me share my favorite things with you in my native language! I really enjoyed it, and hope you did too. I hope you come back and see me if you learn more Japanese. Goodbye")
	
	# Disables the head movements
	# This prevents motors from getting too hot
	motionProxy.setStiffnesses("Head", 0.0)
	motionProxy.wbEnableEffectorControl("Head", False)	
##############################################################################

"""
	This function starts the experiment of running a single condition. User will 
	decide which condition.
"""
def interact_SINGLE_CONDITIONS(choice):	# Variable choice is passed from Main function
	# 1:DIRECTED
	# 2:CONTINGENT
	
	# Setup VAR			
	if(choice==1):				# 1: DIRECTED, CONTINGENT
		condition_1_isOn=True

	else:
		condition_1_isOn=False 	# 2: CONTINGENT, DIRECTED
	
	try:
		motionProxy = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALMotion::",e
		
	motionProxy.setStiffnesses("Head", 1.0)
	motionProxy.wbEnableEffectorControl("Head", True)
	# End Setup
	
	changeSlideOnTabletDirection('restart')	
	
	# Center head location
	print "CONDITION:1"
	moveHeadOrigin(MOTION_PROXY_GLOBAL)
	if(condition_1_isOn):
		interact_NonContingent(WORD_LIST_JAP_1)
	else:
		interact_Contingent(WORD_LIST_JAP_1)

	# Disables the head movements
	# This prevents motors from getting too hot
	motionProxy.setStiffnesses("Head", 0.0)
	motionProxy.wbEnableEffectorControl("Head", False)	
##############################################################################

def speak_intro():	#Script that NAO says at beginning of experiment
	print "::"
	"""
	Experimenter introduces child and robot. “Good morning Rei [robot’s name]. How are you?”
	Robot, “Great! I’m excited to see a new friend here today!”
	Experimenter, “Yes, will you please introduce yourself.”
	Robot, “Hello, my name is Rei. What is your name? ….waits… Nice to meet you! I don’t know much English, but I do know Japanese, I would really like to teach you what my favorite things are called in Japanese. OK?.... OK, I’m going to tell you the names of 12 objects now, and 12 objects later. Let’s get started with the first 12.

	"""
	
	moveheadExperiment1(MOTION_PROXY_GLOBAL)  # Moves Head during beginning of Intro. 
	time.sleep(2.0)								# Pause
	naoTalksFeedText("Great! I’m excited to see a new friend here today!") # User defined function that receives
																	# as input and sends to the text to speech	
																	# enine
	keyboard=raw_input("Hit Enter to continue::")	# Waits for operator to hit Enter
	
	moveHeadOrigin2(MOTION_PROXY_GLOBAL) # Move head to origin and faces the participant
	time.sleep(2.0) # Pause
	
	naoTalksFeedText("My name is  ")#
	naoTalksFeedText(" Ray")#
	naoTalksFeedText("What is your name?")
	keyboard=raw_input("Hit Enter to continue::") # User hits Enter when ready
		
	naoTalksFeedText("Nice to meet you! I don’t know much English, but I do know Japanese, I would really like to teach you what my favorite things are called in Japanese. OK?")
	keyboard=raw_input("Hit Enter to continue::") # Waits for user to press Enter
	naoTalksFeedText("OK, I’m going to tell you the names of 12 objects now, and 12 objects later. You'll repeat each word after I say them. Let’s get started with the first 12")

	
##############################################################################
def interact_tester2():	# This funct is used for testing Only
	# Code here is temporary and only to help debug
	
	get_user_choice_interact()
	
	system.exit(0)
	
	try:
		tts = ALProxy("ALTextToSpeech", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALTextToSpeech::",e
		
	try:
		motionProxy = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL)
	except Exception, e:
		print "::ALMotion::",e
		
	motionProxy.setStiffnesses("Head", 1.0)
	motionProxy.wbEnableEffectorControl("Head", True)
	# End Setup
	
	list=['列車','蜂']
	list2=['れっしゃ','はち​​']
	for i in range (len(list)):
		print "::Content:",(list[i])
		naoTalksLangauage(tts,2,list[i]) #JAP Reading of Words 列車		
		time.sleep(1.50)
		naoTalksLangauage(tts,2,list[i]) #JAP Reading of Words 列車		
		time.sleep(3.0)
		
		naoTalksLangauage(tts,2,list2[i]) #JAP Reading of Words 列車
		time.sleep(1.5)
		naoTalksLangauage(tts,2,list2[i]) #JAP Reading of Words 列車
		time.sleep(3.0)
	# End
	while True:
		changeSlideOnTabletDirection('right')
		naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words	
		time.sleep(0.0250)
		naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words x2
		time.sleep(0.0)
		counter=int(counter) +1
		print "::counter::",counter
		if(counter > 24):# 12 objects x2
			break	
	naoTalksLangauage(tts,1,"Great Job!. Now we are finished!")
	
	motionProxy.setStiffnesses("Head", 0.0)
	motionProxy.wbEnableEffectorControl("Head", False)	
##############################################################################	

if __name__ == "__main__":	# Start of Program

	# App title
	print_title()
	
	# Title
	print "\tHead Movements"
	print "\tSends Signals"
	print "\tChange Slides"
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n"	
	
	WORD_LIST_ENG = [
		"Cat",
		"Dog",
		"Elephant ",
		"Bear",
		"Red",
		"Green",
		"Apple",
		"Strawberry",
		"Carrot",
		"Pumpkin",
		"Bread",
		"Eggs",
		"Kite",
		"Jump rope",
		"Watch",
		"Hat",
		"Mountain",
		"Tree",
		"Triangle",
		"Star",
		"Train",
		"Plane",
		"Bike",
		"Bee ",
		"Snail "]

	WORD_LIST_JAP_1 = [
	"猫 ", #(Neko)
	"林檎", # (Ringo)
	"象 ", #(Zō)
	"赤", # (Aka)
	"三角形", # (Sankakkei)
	"ニンジン", # (Ninjin)
	"凧", # (Tako)
	"時計", # (Tokei)
	"列車", # (Ressha)
	"キノコ", # (Kinoko)
	"山", # (Yama)
	"蜂", # (Hachi) ['列車','蜂']
	]

	WORD_LIST_JAP_2 = [
	" 犬",# (Inu)
	" イチゴ",# (Ichigo)
	" くま",# (Kuma)
	" ミドリ ",# (Midori)
	" ホシガタ",# (Hoshigata)
	" カボチャ",# (Kabocha)
	" 縄跳び",# (Nawatobi)
	" 帽子",# (Bōshi)
	" 飛行機",# (Hikōki) 
	" 卵",# (Tamago)
	" 木",# (Ki)
	" カタツムリ ",#(Katatsumuri)
	]	
	
	
	# Init variable values	for NAO. Setup with Router Name: nao5
	robotIP="192.168.0.100"
	ROBOT_IP_GLOBAL = robotIP
	PORT = 9559
	PORT_GLOBAL = PORT		
	GLOBAL_TIME_MOVE_DELAY = 0.20	# how long it takes for head to move
	GLOBAL_CHANGE_FRACTION = 0.20	# how far should head move for every key press
			
	# Network data for Server
	GLOBAL_IP	= "192.168.245.5" # IP # of machine containing the server
	GLOBAL_PORT = 6110			# Port number can be changed
	serverPort =  GLOBAL_PORT #6110
	serverIP   =  GLOBAL_IP #"192.168.245.5"
	print"::CLIENT::Running::(EXIT: exitserver/exitclient)::"
	print"::host::", serverIP
	print"::port::", serverPort
	
	# Create Socket. Copied from online Sample
	clientSocket = socket(AF_INET, SOCK_STREAM)
	GLOBAL_SOCKET_CLIENT = clientSocket
	GLOBAL_SOCKET_CLIENT.connect((serverIP,serverPort))
	print"::Connect ok"	

	# Subscribe to NAO Speech function
	# Test To Speech is setup with Proxy: ALTextToSpeech
	try:
		tts = ALProxy("ALTextToSpeech", ROBOT_IP_GLOBAL, PORT_GLOBAL) 
	except Exception, e:
		print "::ALTextToSpeech::",e
	
	try:
		motionProxy = ALProxy("ALMotion", ROBOT_IP_GLOBAL, PORT_GLOBAL) # Allows NAO to move head
	except Exception, e:
		print "::ALMotion::",e
		
	motionProxy.setStiffnesses("Head", 1.0)								# Must be stiff in order to move
	motionProxy.wbEnableEffectorControl("Head", True)					# Head function enabled
	MOTION_PROXY_GLOBAL = motionProxy
	

	

	# ***************************************************************************
	# ***************************************************************************
	while True:			# Print Menu
		print "\n\n\t*** N A O Experiment (Indiana University 2018) ***"
		print ""
		print "\t**Chose an option"
		print "\t[0] NAO Introduciton"
		print "\t[1] DIRECTED	--> CONTINGENT"
		print "\t[2] CONTINGENT	--> DIRECTED"
		print "\t[5] Test Program"
		print "\t[6] [ONLY]: CONTINGENT"
		print "\t[7] [ONLY]: DIRECTED"
		print "\t[9] Exit**"		

		keyboard = raw_input("\n\tEnter Option (EXIT: 9):  ")
		keyboard=int(keyboard)

		if(keyboard==0):					# Intro
			speak_intro()					
		if(keyboard==1):					# 1st -->DIRECTED 
			interact_BOTH_CONDITIONS(1)
		if(keyboard==2):					# 1st -->CONTINGENT 
			#interact_CONTINGENT_DIRECTED()			
			interact_BOTH_CONDITIONS(2)		# Passes value 2 (Contingent)	
		if(keyboard==5):					# Test Function
			interact_tester2()
		if(keyboard==6):
			interact_SINGLE_CONDITIONS(2) # 2:CONTINGENT
			#interact_Contingent()		
		if(keyboard==7):
			#changeSlideOnTabletDirection('restart')	
			interact_SINGLE_CONDITIONS(1) # 1:DIRECTED			
		if(keyboard==9):
			break			
	# ***************************************************************************
	# ***************************************************************************
	
	# End Socket 
	GLOBAL_SOCKET_CLIENT.close() #Close#connection	
	sys.exit(0)		# Exit Program