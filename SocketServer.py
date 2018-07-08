

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
def leftKey():
	print"::Key::Action:: "
	time.sleep(GLOBAL_KEY_PRESS_DELAY)
	keyboardSim.press( Key.left )#Enter or Return
	keyboardSim.release( Key.left )
	print"::Key_pressed::"		
###############################################################################
def rightKey():
	print"::Key::Action:: "
	time.sleep(GLOBAL_KEY_PRESS_DELAY)
	keyboardSim.press( Key.right )#Enter or Return
	keyboardSim.release( Key.right )
	print"::Key_pressed::"		
###############################################################################
serverPort = 4322
serverIP = "149.160.188.47"
GLOBAL_KEY_PRESS_DELAY = 0.0






print "::SERVER::Running::(EXIT: exitserver)::(Commands: commandenter)"

# # used to detect parameters passed in CLI
# flag_No_IP_Header_Given = True
# argument_list = ['','','','']
# print"::CLI arguments Size::",len(sys.argv)
# if len(sys.argv) <= 1:
	# print "::Content::",(sys.argv[0])
# else:
	# print"::len(sys.argv) > 1::"
	# flag_No_IP_Header_Given = False
	# for i in range (len(sys.argv)):
		# print "::Content:",(sys.argv[i])
	# for i in range (len(argument_list)):
		# argument_list[i]=(sys.argv[i])	



# # PYTHON.EXE FILENAME IP PORT DELAY	

# while flag_No_IP_Header_Given:
	# keyboard = raw_input("Enter IP: ")
	# #GLOBAL_IP = keyboard
	# if(keyboard is not None):
		# print"::Ok"
		# GLOBAL_IP = str(keyboard)
		# break
		
# while flag_No_IP_Header_Given:
	# keyboard = raw_input("Enter PORT: ")
	# #GLOBAL_IP = keyboard
	# if(keyboard is not None):
		# print"::Ok"
		# GLOBAL_PORT = int(keyboard)
		# break

# while flag_No_IP_Header_Given:
	# keyboard = raw_input("Set key press delay (default 1): ")
	# #GLOBAL_IP = keyboard
	# if(keyboard is not None):
		# print"::Ok"
		# GLOBAL_KEY_PRESS_DELAY = float(keyboard)
		# break	

# GLOBAL_IP				= argument_list[1]
# GLOBAL_PORT				= int(argument_list[2])
# GLOBAL_KEY_PRESS_DELAY	= float(argument_list[3])

GLOBAL_IP				= "192.168.245.5"#argument_list[1]
GLOBAL_PORT				= 6110#int(argument_list[2])
GLOBAL_KEY_PRESS_DELAY	= 0.0#float(argument_list[3])

print "::GLOBAL_KEY_PRESS_DELAY",GLOBAL_KEY_PRESS_DELAY
print "::Port::", GLOBAL_PORT
print "::IP::",GLOBAL_IP

#create an INET, STREAMing socket
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serverSocket.bind((GLOBAL_IP, GLOBAL_PORT)) #this is the server address
#become a server socket
serverSocket.listen(3)

keyboardSim = Controller()

connectionSocket, addr = serverSocket.accept()
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
