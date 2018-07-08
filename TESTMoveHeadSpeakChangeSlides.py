#!/usr/bin/python
# -*- coding: utf-8 -*- 	
#The coding line above it is necessary in order to
#deal with Japanese characters. Python will default 
#to ASCII as standard encoding if no other encoding 
#hints are given.


"""
	This file contains functions for the NAO robot using the NAOqi Framework.
	Functions: speak Japanese words, performs directed gaze, contingent gaze,
	automatically changes slides displayed on iPad. Japanese words are written
	using Kanji and Katakana. The NAOqi Framework is utilized.
	
	
	2018 Indiana University
	
"""




	# while True:
		# time.sleep(2.00)
		# #Change the Slide
		# changeSlideOnTabletDirection('right')
		# #changeSlideOnTabletSimple('right')
		# #GLOBAL_SOCKET_CLIENT.send('right')
		# time.sleep(0.50)
		# #clientSocket.send(command) # input ok so send it
		# #modifiedSentence = GLOBAL_SOCKET_CLIENT.recv(1024) # get from Server
		# #print 'From Server:', modifiedSentence
		# #GLOBAL_SOCKET_CLIENT.close()		
		# ##
		# ##
		# moveheadGoDown(MOTION_PROXY_GLOBAL) #Move Head
		# #GLOBAL_SOCKET_CLIENT.send('right')
		# time.sleep(0.50)		
		# #naoTalksLangauage(tts,1,str(WORD_LIST_ENG[int(counter)])) #English Reading of Words
		# naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words	
		# time.sleep(1.00)
		# naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words x2
		# randTime = random.uniform(0.5,1.5)
		# time.sleep(1.0)
		# #moveheadGoUp(MOTION_PROXY_GLOBAL)
		# moveHeadOrigin(MOTION_PROXY_GLOBAL)
		# counter=int(counter) +1
		# print "::counter::",counter
		# if(counter > 24):# 12 objects x2
			# break	
	# naoTalksLangauage(tts,1,"Ok, Now we are finished!")




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
global WORD_LIST_ENG
global GLOBAL_SOCKET_CLIENT
#global PORT_GLOBAL
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
def changeSlideOnTabletInit():
	# L
	# R
	print "\n\n\t:: *CLIENT SOCKET SETUP TO THE SERVER ::"
	while True:
		keyboard = raw_input("Enter IP: ")
		if(keyboard is not None):
			print"::Ok"
			break

	GLOBAL_IP = keyboard #ROBOT_IP_GLOBAL

	while True:
		keyboard = raw_input("Enter PORT: ")
		if(keyboard is not None):
			print"::Ok"
			break

	GLOBAL_PORT = int(keyboard)

	serverPort = GLOBAL_PORT
	serverIP   = GLOBAL_IP
	print"::CLIENT::Running::(EXIT: exitserver/exitclient)::"
	print"::host::", serverIP
	print"::port::", serverPort

	clientSocket = socket(AF_INET, SOCK_STREAM)
#	clientSocket.connect((serverIP,serverPort))	
	GLOBAL_SOCKET_CLIENT = clientSocket
	GLOBAL_SOCKET_CLIENT.connect((serverIP,serverPort))
	print"::Connect ok"

	# Must start to comment here----
	# while True:
		# #prepare the command
		# sentence = raw_input('Client Input (EXIT: exitserver/exitclient): ')
		# print"::Input_was::",sentence
		# if(sentence == "exitclient"): # is new input is 'exit' then quit
			# print"::Exit_Detected::"
			# break
		# #X
		
		# #send the command through a socket
		# clientSocket.send(sentence) # input ok so send it
		# modifiedSentence = clientSocket.recv(1024) # get from Server
		# print 'From Server:', modifiedSentence
		# #X

	# #close the socket
	# clientSocket.close()
	# GLOBAL_SOCKET_CLIENT.close()
###############################################################################
def changeSlideOnTabletDirection(command):
	command = str(command)#String

	#send the command through a socket
	if(GLOBAL_SOCKET_CLIENT is None):
		raw_input("Wait:::")
	GLOBAL_SOCKET_CLIENT.send(command)
	#clientSocket.send(command) # input ok so send it
	modifiedSentence = GLOBAL_SOCKET_CLIENT.recv(1024) # get from Server
	print 'From Server:', modifiedSentence
	#X	
###############################################################################
def changeSlideOnTabletSimple(command):	
	print "\n\n\t:: *CLIENT SOCKET SETUP TO THE SERVER ::"
	while True:
		keyboard = raw_input("Enter IP: ")
		if(keyboard is not None):
			print"::Ok"
			break

	GLOBAL_IP = keyboard #ROBOT_IP_GLOBAL

	while True:
		keyboard = raw_input("Enter PORT: ")
		if(keyboard is not None):
			print"::Ok"
			break

	GLOBAL_PORT = int(keyboard)

	serverPort = GLOBAL_PORT
	serverIP   = GLOBAL_IP
	print"::CLIENT::Running::(EXIT: exitserver/exitclient)::"
	print"::host::", serverIP
	print"::port::", serverPort

	clientSocket = socket(AF_INET, SOCK_STREAM)
#	clientSocket.connect((serverIP,serverPort))	
	GLOBAL_SOCKET_CLIENT = clientSocket
	GLOBAL_SOCKET_CLIENT.connect((serverIP,serverPort))
	print"::Connect ok"
	
	command='right'
	command = str(command)#String
	#GLOBAL_SOCKET_CLIENT = cleintSocket
	#clientSocket = GLOBAL_SOCKET_CLIENT
	#send the command through a socket
	if(GLOBAL_SOCKET_CLIENT is None):
		raw_input("Wait:::")
	GLOBAL_SOCKET_CLIENT.send(command)
	#clientSocket.send(command) # input ok so send it
	modifiedSentence = GLOBAL_SOCKET_CLIENT.recv(1024) # get from Server
	print 'From Server:', modifiedSentence
	GLOBAL_SOCKET_CLIENT.close()
###############################################################################
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
def moveHeadOrigin(MP):
	
	#MP.post.angleInterpolation(names, angleLists, timeLists, isAbsolute) #'post' funciton allows paralled funtionality
	MP.post.angleInterpolation("HeadPitch", 0.0, 1.0, True) #'post' funciton allows paralled funtionality
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
	MP.changeAngles("HeadPitch", -0.35, GLOBAL_TIME_MOVE_DELAY)#Right	
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
	MP.changeAngles("HeadPitch", 0.45, GLOBAL_TIME_MOVE_DELAY)#Right		was 0.35
	MP.wbEnableEffectorControl("Head", False)
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
#def main(robotIP,faceSize,PORT=9559):
###############################################################################
def interact_Contingent():
	print "::"

	# Setup VAR			
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
	MOTION_PROXY_GLOBAL = motionProxy
	counter = 0
	# End Setup

	naoTalksLangauage(tts,1,"Ready, Lets begin!. Contingent")	
	# Disable For TEST
	while True:
		#time.sleep(2.00)
		#Change the Slide
		changeSlideOnTabletDirection('right')
		#changeSlideOnTabletSimple('right')
		#GLOBAL_SOCKET_CLIENT.send('right')
		time.sleep(0.50)
		#clientSocket.send(command) # input ok so send it
		#modifiedSentence = GLOBAL_SOCKET_CLIENT.recv(1024) # get from Server
		#print 'From Server:', modifiedSentence
		#GLOBAL_SOCKET_CLIENT.close()		
		##
		##
		#moveheadGoDown(MOTION_PROXY_GLOBAL) #Move Head
		#GLOBAL_SOCKET_CLIENT.send('right')
		#time.sleep(0.50)		
		#naoTalksLangauage(tts,1,str(WORD_LIST_ENG[int(counter)])) #English Reading of Words
		naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words	
		time.sleep(1.00)
		naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words x2
		time.sleep(1.0)
		#moveheadGoUp(MOTION_PROXY_GLOBAL)
		#moveHeadOrigin(MOTION_PROXY_GLOBAL)
		time.sleep(3.5)
		counter=int(counter) +1
		print "::counter::",counter
		if(counter > 24):# 12 objects x2
			break	
	naoTalksLangauage(tts,1,"Great Job!. Now we are finished!")
	print "::STOP_TIMING::"	
	print "::End Method"
	motionProxy.setStiffnesses("Head", 0.0)
	motionProxy.wbEnableEffectorControl("Head", False)			
##############################################################################
def interact_NonContingent():

	# Setup VAR			
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
	MOTION_PROXY_GLOBAL = motionProxy
	counter = 0
	# End Setup

	naoTalksLangauage(tts,1,"Ready, Lets begin!")
	
	while True:
		time.sleep(2.00)
		changeSlideOnTabletDirection('right')
		time.sleep(0.50)
		moveheadGoDown(MOTION_PROXY_GLOBAL) #Move Head
		time.sleep(0.50)		
		naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words	
		time.sleep(1.00)
		naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words x2
		time.sleep(1.0)
		moveHeadOrigin(MOTION_PROXY_GLOBAL)
		counter=int(counter) +1
		print "::counter::",counter
		if(counter > 24):# 12 objects x2
			break
	naoTalksLangauage(tts,1,"Great Job!. Now we are finished!")
	print "::STOP_TIMING::"	
	print "::End Method"
	motionProxy.setStiffnesses("Head", 0.0)
	motionProxy.wbEnableEffectorControl("Head", False)	
##############################################################################
if __name__ == "__main__":

	# App title
	print_title()
	
	print "\tHead Movements"
	print "\tSends Signals"
	print "\tChange Slides"
	print "\n\t********************************\n\t********************************\n\t********************************"
	print "\n"	
	
	
	# # used to detect parameters passed in CLI
	print"::CLI arguments Size::",len(sys.argv)
	if len(sys.argv) <= 1:
		print "::Content::",(sys.argv[0])
	else:
		print"::len(sys.argv) > 1::"
		#print"::0::", sys.argv[0]
		#print"::1::", sys.argv[1]
		for i in range (len(sys.argv)):
			print "::Content:",(sys.argv[i])
		print ("::End of sys.argv::")
	
	
	

	robotIP = "nao.local"
	print "::Start Head Movement, Japanese Pronunciation, Slide Changer::"
	keyboard = raw_input("Enter IP: ")
	if (keyboard is not None):
		robotIP=str(keyboard)
		print "::entered=", robotIP
	else:
		print "::entered::NONE::"
	ROBOT_IP_GLOBAL = robotIP
	PORT = 9559
	PORT_GLOBAL = PORT		
	GLOBAL_TIME_MOVE_DELAY = 0.20
	GLOBAL_CHANGE_FRACTION = 0.20
	
		
	##									##	
	##		Initialize the Sockets		##
	##									##
	#changeSlideOnTabletInit()
	print "\n\n\t:: *CLIENT SOCKET SETUP TO THE SERVER ::"
	while True:
		keyboard = raw_input("Enter IP: ")
		if(keyboard is not None):
			print"::Ok"
			break
	GLOBAL_IP = keyboard #ROBOT_IP_GLOBAL
	while True:
		keyboard = raw_input("Enter PORT: ")
		if(keyboard is not None):
			print"::Ok"
			break
	GLOBAL_PORT = int(keyboard)
	serverPort = GLOBAL_PORT
	serverIP   = GLOBAL_IP
	print"::CLIENT::Running::(EXIT: exitserver/exitclient)::"
	print"::host::", serverIP
	print"::port::", serverPort
	clientSocket = socket(AF_INET, SOCK_STREAM)
#	clientSocket.connect((serverIP,serverPort))	
	GLOBAL_SOCKET_CLIENT = clientSocket
	GLOBAL_SOCKET_CLIENT.connect((serverIP,serverPort))
	print"::Connect ok"	
	##									##	
	##		Initialize the Sockets		##
	##									##
	
		
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
	MOTION_PROXY_GLOBAL = motionProxy
	
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

	WORD_LIST_JAP = [
		" 猫",
		" 犬",
		" 象",
		" くま",
		" 赤",
		" 緑",
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
		" 星", #star
		" 模型",
		" 飛行機", # airplane
		" 自転車",
		" 蜂",
		" カタツムリ"]
	
	root = Tk()

	#TEST LOOP FOR TALKING
	#print "::START_TIMING::"
	#counter = 0.0
	#time.sleep(2.00)
#	moveHeadOrigin(MOTION_PROXY_GLOBAL)
	#naoTalksLangauage(tts,1,"Ready, Lets begin!")
	
	
	
	
	
	# # Disable For TEST
	# while True:
		# #time.sleep(2.00)
		# #Change the Slide
		# changeSlideOnTabletDirection('right')
		# #changeSlideOnTabletSimple('right')
		# #GLOBAL_SOCKET_CLIENT.send('right')
		# time.sleep(0.50)
		# #clientSocket.send(command) # input ok so send it
		# #modifiedSentence = GLOBAL_SOCKET_CLIENT.recv(1024) # get from Server
		# #print 'From Server:', modifiedSentence
		# #GLOBAL_SOCKET_CLIENT.close()		
		# ##
		# ##
		# #moveheadGoDown(MOTION_PROXY_GLOBAL) #Move Head
		# #GLOBAL_SOCKET_CLIENT.send('right')
		# #time.sleep(0.50)		
		# #naoTalksLangauage(tts,1,str(WORD_LIST_ENG[int(counter)])) #English Reading of Words
		# naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words	
		# time.sleep(1.00)
		# naoTalksLangauage(tts,2,str(WORD_LIST_JAP[int(counter)])) #JAP Reading of Words x2
		# time.sleep(1.0)
		# #moveheadGoUp(MOTION_PROXY_GLOBAL)
		# #moveHeadOrigin(MOTION_PROXY_GLOBAL)
		# time.sleep(3.5)
		# counter=int(counter) +1
		# print "::counter::",counter
		# if(counter > 24):# 12 objects x2
			# break	
	# naoTalksLangauage(tts,1,"Ok, Now we are finished!")
	# print "::STOP_TIMING::"	
	
	
	
	
	
	
	
	moveHeadOrigin(MOTION_PROXY_GLOBAL)
	
	# Contingent
	interact_Contingent()
	
	moveHeadOrigin(MOTION_PROXY_GLOBAL)
	
	# Call Non-Contingent
	interact_NonContingent()
	
	# End Socket 
	GLOBAL_SOCKET_CLIENT.close() #Close#connection	
	sys.exit(0)	
	
	
	#Move Head
	print( "Press a key (Escape key to exit):" )
	frame = Frame(root, width=300, height=300)
	frame.bind("<Up>", key)
	frame.bind("<Down>", key)
	frame.bind("<Left>", key)
	frame.bind("<Right>", key)
	frame.bind('<Button-1>',callback)
	frame.pack()
	root.mainloop()

