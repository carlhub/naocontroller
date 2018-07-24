

"""
	This file creates a socket that listens on serverIP, serverPort and can
	be run a remote machine or a local machine. The server will listen on
	serverPort. When command is received, this file will emulate a key being 
	pressed. 
	
	Indiana University 2018
"""


import socket
import sys
import time
from pynput.keyboard import Key, Controller
#from socket import *

###############################################################################
global GLOBAL_IP
global GLOBAL_PORT
global GLOBAL_KEY_PRESS_DELAY
###############################################################################
def changeDelay():
	keyboard = raw_input("Enter new delay: ")
	try:
		GLOBAL_KEY_PRESS_DELAY = int(keyboard)
	except Exception, e:
		print "::error::", e
		return
	print"::set::"
###############################################################################
def leftKey():									# This function changes to previous slides
	print"::Key::Action:: "						# Prinout of current settings
	time.sleep(GLOBAL_KEY_PRESS_DELAY)			# Puse set to 0 seconds
	keyboardSim.press( Key.left )				# Enter or Return
	keyboardSim.release( Key.left )				# Release the Enter key
	print"::Key_pressed::"						# Print so user knows function
												# has finished
###############################################################################
def rightKey():								# This function advances to next slide
	print"::Key::Action:: "
	time.sleep(GLOBAL_KEY_PRESS_DELAY)		# Pause set to 0 (default)
	keyboardSim.press( Key.right )			# Enter or Return
	keyboardSim.release( Key.right )		# Release the key
	print"::Key_pressed::"		
###############################################################################
# This function will ensure that slides start from the beginning
# Meant for the start of the experiment
def restartSlides():
	print"::Key::Action:: "					# for debugging. User knows it started
	time.sleep(GLOBAL_KEY_PRESS_DELAY)		# Puase for 0 sec.
	keyboardSim.press( Key.esc )			# Press Esc
	keyboardSim.release( Key.esc )			# Release Esc
	keyboardSim.press( Key.f5 )				# Press key F5 (slideshow mode)
	keyboardSim.release( Key.f5 )			# Release key F5
	print"::Key_pressed::"					# Used for debugging. Lets user know 
											# function finished.
###############################################################################

serverPort = 4322
serverIP = "149.160.188.47"
GLOBAL_KEY_PRESS_DELAY = 0.0


print "::SERVER::Running::(EXIT: exitserver)::(Commands: commandenter)"

# # used to detect parameters passed in CLI
flag_No_IP_Header_Given = True
argument_list = ['','','']#None#['','','','']
print"::CLI arguments Size::",len(sys.argv)
if len(sys.argv) <= 1:
	print "::Content::",(sys.argv[0])
else:
	print"::len(sys.argv) > 1::"
	flag_No_IP_Header_Given = False
	for i in range (len(sys.argv)):
		print "::Content:",(sys.argv[i])
	for i in range (len(argument_list)):
		argument_list[i]=(sys.argv[i])	


#GLOBAL_IP				= "192.168.0.101"
GLOBAL_IP				= "192.168.245.5"		# This IP# should be the same as the one on Nao_Main_Experiment
GLOBAL_PORT				= 6110					# This IP# should be the same as the one on Nao_Main_Experiment
GLOBAL_KEY_PRESS_DELAY	= 0.0#float(argument_list[3])
GLOBAL_FLAG				= ''

print "::GLOBAL_KEY_PRESS_DELAY",GLOBAL_KEY_PRESS_DELAY	# Print out of settings
print "::Port::", GLOBAL_PORT							# Print out of settings
print "::IP::",GLOBAL_IP								# Print out of settings

# Code below is taken from an online sample
#create an INET, STREAMing socket
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serverSocket.bind((GLOBAL_IP, GLOBAL_PORT)) #this is the server address
#become a server socket
serverSocket.listen(3)

keyboardSim = Controller()						# From library: Pynput

connectionSocket, addr = serverSocket.accept()	# Part of server socket

GLOBAL_FLAG = "GO"								# Part of experimental code, maybe delete?

#############################################################################################
while True:
	while True:
		#connectionSocket, addr = serverSocket.accept() # this returns a connection/socket		
		sentence = connectionSocket.recv(1024)# reads data from connection
		print"::Received::", sentence
		if(sentence == ''):				# Nothing received from client socket
			print"::empty::NA::"
			break
		if(sentence == 'exitserver'):	# Tells server to quit
			print "::encountered-->exit"
			break
		if(sentence == 'changedelay'):	# disabled 
			print("::NA")#changeDelay()
		if(sentence == 'left'):
			print("::LeftAction")		# Moves to previous slide
			leftKey()
		if(sentence == 'right'):		# This function advances to next slide
			rightKey()	
		if(sentence == 'restart'):		# Meant for the beginning of a condition
			restartSlides()				# calls the function to restart the slides
		if(sentence == 'commandenter'):
			print"::ENTERsimulate::Action:: "
			time.sleep(GLOBAL_KEY_PRESS_DELAY) 	# Pause for 0 seconds.
												# This function advances to next slide
			keyboardSim.press( Key.enter ) 		# Enter or Return
			keyboardSim.release( Key.enter )	# Release Enter
			print"::Key was pressed::"	
		
		# Code below is from online sample but it is wokring good.
		# Capitalize the Sentence
		capitalizedSentence = sentence.upper()
		connectionSocket.send(capitalizedSentence)#response to Client		
	if (GLOBAL_FLAG == 'STOP'):
		print "::flag detected"
		break

##############################################################################################

while True:
	#connectionSocket, addr = serverSocket.accept() # this returns a connection/socket		
	sentence = connectionSocket.recv(1024)# reads data from connection
	print"::Received::", sentence
	if(sentence == ''):
		print"::empty::NA::"
		break
	if(sentence == 'exitserver'):
		print "::encountered-->exit"
		break
	if(sentence == 'changedelay'):
		print("::NA")#changeDelay()
	if(sentence == 'left'):
		print("::LeftAction")
		leftKey()
	if(sentence == 'right'):
		rightKey()	
	if(sentence == 'restart'):
		restartSlides()			
	if(sentence == 'commandenter'):
		print"::ENTERsimulate::Action:: "
		time.sleep(GLOBAL_KEY_PRESS_DELAY)
		keyboardSim.press( Key.enter )#Enter or Return
		keyboardSim.release( Key.enter )
		print"::Key was pressed::"	
	# Capitalize the Sentence
	capitalizedSentence = sentence.upper()
	connectionSocket.send(capitalizedSentence)#response to Client		
		
	
print "::END"
connectionSocket.close()
