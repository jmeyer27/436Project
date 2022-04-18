#!/usr/bin/env python3
import uuid
import socket
from datetime import datetime
import sys

# Time operations in python
# timestamp = datetime.fromisoformat(isotimestring)

# Extract local MAC address [DO NOT CHANGE]
MAC = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1]).upper()

# SERVER IP AND PORT NUMBER [DO NOT CHANGE VAR NAMES]
SERVER_IP = "10.0.0.100"
SERVER_PORT = 9000


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def discover():
  # Sending DISCOVER message
  discover = "DISCOVER " + MAC
  clientSocket.sendto(discover.encode(), (SERVER_IP,   SERVER_PORT))

def release():
  release = "RELEASE " + MAC #need to add ip address
  clientSocket.sendto(release.encode(), (SERVER_IP,   SERVER_PORT))

def renew():
  renew = "RENEW " + MAC #need to add ip address
  clientSocket.sendto(renew.encode(), (SERVER_IP,   SERVER_PORT))


print("The client is waiting for a message.")#a lil' thang to show the program is running and waiting for a message

# LISTENING FOR RESPONSE
message, _ = clientSocket.recvfrom(4096)


print("The client received something in its socket.")#just seeing if this is working

#if client receives OFFER, checks if messages MAC is the same as the MAC it sent
  #if yes, checks if timestamp is expired
    #if not expired, send REQUEST w/ MAC and IP and timestamp

#if received a DECLINE message, tell user it was declined and terminate

#if received ACKNOWLEDGE, checks MAC address
  #if different, tell user and terminate program
  #else display IP to user, read number 6.
  #then display a menu (the menu below, but make it fancy and work correctly)

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
