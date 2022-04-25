#!/usr/bin/env python3
import socket
from ipaddress import IPv4Interface
from datetime import datetime, timedelta


# Time operations in python
isotimestring = datetime.now().isoformat()
timestamp = datetime.fromisoformat(isotimestring)
#60secfromnow = timestamp + timedelta(seconds=60)

# Choose a data structure to store your records
records = [] #list, will use nested lists :)
#record num = list placement (up to 14 total records will be stored)
#MAC address
#IP address (192.168.45.(1 to 14)) = 14 recorded ip addresses
#timestamp 
#ACKED

# List containing all available IP addresses as strings
ip_addresses = [ip.exploded for ip in IPv4Interface("192.168.45.0/28").network.hosts()]

# Parse the client messages
def parse_message(message):  #This is a hot mess btw
  message = str(message).split(' ')
  #print(message)
  return message


  #  ~!~  i m p o r t a n t  ~!~
#Server never assigns more than one IP to a MAC address at a time
#or sets same IP to multiple MACs.
#When client sends a RELEASE and then a RENEW, it gets the address it had b4
#We have to have print statements for each step

def dhcp_operation(parsed_message):
    request = str(parsed_message[0])
    request = request[2:]
    #print (request) for debugging
   
    print("REQUEST IS: ")
    if request == "LIST":
      print('request == LIST')#just a print statement to see if it is being received
      #idk, something about an admin client. Read step 12?
      pass
    elif request == "DISCOVER":#When server receives DISCOVER:
      MAC = str(parsed_message[1])
      if records: #records is true when not empty, false if empty
        #check if MAC address exists in list or not
        #if found, check if timestamp expired
        #if not expired set ACKED to true, send ACKNOWLEDGE 
        #if expired, look at third bullet point for updating
        #if no MAC address was found:
        #check pool of IP that has not been occupied by clients
        #if last IP was searched, check timestamps
        #if timestamp expired, use IP for new request
          #update record with new MAC and expiration time
          #set ACKED to FALSE
        #if NO EXPIRED TIMESTAMP, send client a DECLINE
        #store info in record, idk look @ last bullet point before 4
        pass 
      else: #no records exist and records is empty, so add to records and offer
        ip = "192.168.45.1" #IP for first record
        timestamp = datetime.fromisoformat(isotimestring) 
        u60secfromnow = timestamp + timedelta(seconds=60)#timestamp expires in 60 seconds
        #newRecord = [num in records, client's MAC, New IP address, timestamp, ACK]
        newRecord = [1, MAC, ip, u60secfromnow, False]
        records.append(newRecord)#store in record
        #reply with OFFER containing MAC, assigned IP, u60secondsfromnow
        offer = "OFFER" +MAC +str(ip) +str(u60secfromnow) #offer message
        return offer
       
        
      
    elif request == "REQUEST":
      print('request == REQUEST')#just a print statement to see if it is being received
      #when server receives REQUEST, check if IP matches IP of record
      #if not then send a DECLINE
      #otherwise check if timestamp expired
      #if expired send DECLINE
      #otherwise set ACKED to TRUE in record and send ACKNOWLEDGE
      pass
    elif request == "RELEASE":
      print('request == RELEASE')#just a print statement to see if it is being received
      #when receive a RELEASE, check records and release IP by making it expired
      #set ACKED to FALSE
      #if the IP was not found somehow then do nothing 
      pass
    elif request == "RENEW":
      print('request == RENEW')#just a print statement to see if it is being received
      #if receive RENEW, check records and renew IP address by resetting timestamp
      #set ACKED to TRUE
      #send ACKNOWLEDGE to client
      #if IP was somehow not found, check pool of IP that has not been occupied by clients
      #same steps as Discover, soooooo...
       #if last IP was searched, check timestamps
        #if timestamp expired, use IP for new request
          #update record with new MAC and expiration time
          #set ACKED to FALSE
        #if NO EXPIRED TIMESTAMP, send client a DECLINE
      #if it succeeded in switching IP addresses, then send new MAC with an OFFER message and set ACKED to FALSE
      pass

# Start a UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Avoid TIME_WAIT socket lock [DO NOT REMOVE]
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

SERVER_IP = socket.gethostname() #a trial, idk if this works? it should?
server.bind((SERVER_IP, 9000)) #server.bind(("", 9000))
print("DHCP Server running...")

try:
    while True:
        message, clientAddress = server.recvfrom(4096)
        print("Server received <- " +str(message.decode()))#a message to show received message
        parsed_message = parse_message(message)#so bad

        response = dhcp_operation(parsed_message)#being worked on
        print("Server sending -> " +(response))
        server.sendto(response.encode(), clientAddress)
except OSError:
    pass
except KeyboardInterrupt:
    pass

server.close()
