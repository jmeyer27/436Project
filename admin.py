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


def list():
  discover = "LIST " + str(MAC)
  clientSocket.sendto(discover.encode(), (SERVER_IP, SERVER_PORT))


# LISTENING FOR RESPONSE
def listen():
  print("The admin is waiting for a message.")#the program is running and waiting for a message
  message, _ = clientSocket.recvfrom(4096)
  print("Admin received <- " +message.decode())
  return str(message.decode())

def received(message):
  print(message)


list()#Sending something to the server
message = listen()#listen for response
received(message)#show list to user