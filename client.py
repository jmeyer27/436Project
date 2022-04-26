#!/usr/bin/env python3
import uuid
import socket
from datetime import datetime
import sys

# Time operations in python
# timestamp = datetime.fromisoformat(isotimestring)
isotimestring = datetime.now().isoformat()

# Extract local MAC address [DO NOT CHANGE]
MAC = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1]).upper()

# SERVER IP AND PORT NUMBER [DO NOT CHANGE VAR NAMES]
SERVER_IP = "10.0.0.100"
SERVER_PORT = 9000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def discover():
  # Sending DISCOVER message
  discover = "DISCOVER " + str(MAC)
  clientSocket.sendto(discover.encode(), (SERVER_IP, SERVER_PORT))

def release():
  release = "RELEASE " + str(MAC) #need to add ip address
  clientSocket.sendto(release.encode(), (SERVER_IP, SERVER_PORT))

def renew():
  renew = "RENEW " + str(MAC) #need to add ip address
  clientSocket.sendto(renew.encode(), (SERVER_IP, SERVER_PORT))




# LISTENING FOR RESPONSE
def listen():
  print("The client is waiting for a message.")#the program is running and waiting for a message
  message, _ = clientSocket.recvfrom(4096)
  print("Client received <- " +message.decode())

  return str(message.decode())


#if client receives OFFER, checks if messages MAC is the same as the MAC it sent
  #if yes, checks if timestamp is expired
    #if not expired, send REQUEST w/ MAC and IP and timestamp
#if received ACKNOWLEDGE, checks MAC address
  #if different, tell user and terminate program
  #else display IP to user, read number 6.
  #then display a menu (the menu below, but make it fancy and work correctly)
def received(message):
  message = message.split(' ')
  if(message[0] == "OFFER"):
    check = checkMac(message[1])
    if(check == True):
      time = message[3] +" " +message[4] #this was necessary because the message is split by spaces
      checkTime = checkTimeStamp(time)#check whether timestamp is expired
      if(checkTime == True):#true means it has not expired
        request(message[2])
    elif(check == False):#MAC was not from this client
      pass #ignore
    
  if(message[0]== "ACKNOWLEDGE"):
    print("message is ack") #debugging
    check = checkMac(message[1])
    if(check == False):
      print("Error: MAC Address Fail")
      sys.exit()
    elif(check == True):
      ipAddress = message[2]
      print("Address " +ipAddress +" has been assigned to this client. TTL " +message[3] +" " +message[4])
      menu()
    
  if(message[0]== "DECLINE"):
    print("Server declined connection, please try again later.")
    sys.exit()

def checkMac(message):
  if(message == MAC):
    return True
  else:
    return False

    
def request(ipOffer):
  request = "REQUEST " + str(MAC) + " " + str(ipOffer)
  print("Client sending -> " +str(request)) #debugging
  clientSocket.sendto(request.encode(),(SERVER_IP, SERVER_PORT))

def checkTimeStamp(time): #will return true if not expired, false if expired
  timestamp = datetime.fromisoformat(isotimestring)
  timeFromServer = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
  difference = timeFromServer - timestamp
  if(difference.seconds > 0):
    return True
  else:
    return False


#the menu:
  #release (read number 8)
  #renew (read number 9)
  #quit 
def menu():
  while True:
    choice = 0
    print("Please choose from the options below:")
    print("Enter 1 to Release")
    print("Enter 2 to Renew")
    print("Enter 3 to Quit")
    choice = input("Choice is: ")

    if(choice == 1):
      release()
    elif(choice == 2):
      renew()
    elif(choice == 3):
      sys.exit()


discover()#Sending something to the server
message = listen()#listen for OFFER
received(message)#interpret message
message = listen()#listen for additional messages

