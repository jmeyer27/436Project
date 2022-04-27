#!/usr/bin/env python3
import socket
from ipaddress import IPv4Interface
from datetime import datetime, timedelta


# Time operations in python
isotimestring = datetime.now().isoformat()
timestamp = datetime.fromisoformat(isotimestring)
#60secfromnow = timestamp + timedelta(seconds=60)

# A data structure to store your records
records = [] #list of lists

# List containing all available IP addresses as strings
ip_addresses = [ip.exploded for ip in IPv4Interface("192.168.45.0/28").network.hosts()]

# Parse the client messages
def parse_message(message):  #This is a hot mess btw
  message = str(message).split(' ')
  return message

def checkAssigned(address):
  #if matches return true
  #else return false
  pass

def checkTimeStamp(time):
  timestamp = datetime.fromisoformat(isotimestring)
  difference = time - timestamp
  if(difference.seconds > 0):
    return True
  else:
    return False
  

def dhcp_operation(parsed_message):
    request = str(parsed_message[0])
    request = request[2:]
   
    print("REQUEST IS: ")
    if request == "LIST":
      #Read step 12

      output = " "
      if records:
        for list in records:
          output += +str(list[0]) +" "+str(list[1]) +" " +str(list[2]) +" " +str(list[3])+" " +str(list[4]) +"\n"
      else:
        return "There were no records"

      
    
    elif request == "DISCOVER":#When server receives DISCOVER:
      requestMAC = str(parsed_message[1])
      requestMAC = requestMAC[:-1]
      if records: #records is true when not empty, false 
        countOfAddresses = 0
        for list in records:#Record = [num in records, client's MAC, New IP address, timestamp, ACK]
          countOfAddresses += 1
          if(list[1] == requestMAC): #finds MAC address in list
            if(checkTimeStamp(list[3])): #if timestamp was not expired
              list[4] = True #sets ACK to true
              ack = "ACKNOWLEDGE " + str(list[1]) +" " +str(list[2]) +" " +str(list[3])
              return ack
            else:#timestamp expired on found MAC address
              timestamp = datetime.fromisoformat(isotimestring) 
              u60secfromnow = timestamp + timedelta(seconds=60)
              list[3] = u60secfromnow #renew timestamp
              list[4] = False #set ACKED to False
              offer = "OFFER " +str(list[1]) +" " +str(list[2]) +" " +str(list[3])
              return offer
        if(countOfAddresses < 14): #there are still IP left, and MAC was not in list
          countOfAddresses += 1
          nextIP = "192.168.45." +str(countOfAddresses) #next ip is next available
          timestamp = datetime.fromisoformat(isotimestring) #todo expiration is 60 seconds
          u60secfromnow = timestamp + timedelta(seconds=60)
          #newRecord = [num in records, client's MAC, New IP address, timestamp, ACK]
          newRecord = [countOfAddresses, requestMAC, nextIP, u60secfromnow, False]
          records.append(newRecord)#store info in record
          offer = "OFFER " +requestMAC +" " +str(nextIP) +" "+str(u60secfromnow) #offer message
          return offer
        else: #all 14 IPs are being used
          for list in records:#Record = [num in records, client's MAC, New IP address, timestamp, ACK]
            if(checkTimeStamp(list[3])): #if timestamp was not expired
              pass #do nothing, those are ok
            else: #timestamp expired
              list[1] = parsed_message[1] #sets the MAC to the IP
              timestamp = datetime.fromisoformat(isotimestring) 
              u60secfromnow = timestamp + timedelta(seconds=60) #new timestamp w 60 second expiration
              list[3] = u60secfromnow #renew timestamp
              list[4] = False #set ACKED to False
              offer = "OFFER " +str(list[1]) +" " +str(list[2]) +" " +str(list[3])
              return offer
          decline = "DECLINE "+str(parsed_message[1]) +str(parsed_message[2]) 
          return decline
      else: #no records exist and records is empty, so add to records and offer
        ip = "192.168.45.1" #IP for first record
        timestamp = datetime.fromisoformat(isotimestring) 
        u60secfromnow = timestamp + timedelta(seconds=60)#timestamp expires in 60 seconds
        #newRecord = [num in records, client's MAC, New IP address, timestamp, ACK]
        newRecord = [1, requestMAC, ip, u60secfromnow, False]
        records.append(newRecord)#store in record
        #reply with OFFER containing MAC, assigned IP, u60secondsfromnow
        offer = "OFFER " +requestMAC +" " +str(ip) +" "+str(u60secfromnow) #offer message
        return offer
        #end discover
       
      
    elif request == "REQUEST": 
      match = False
      word = str(parsed_message[2])
      word = word[:-1]#this is because the client adds ' to the end of messages
      for list in records:
        if(list[1] == parsed_message[1]): #finds MAC address in list 
          if(list[2] == word): #makes sure IP associated with MAC is the one it sent
            match = True 
            if(checkTimeStamp(list[3])): #if timestamp was not expired
              list[4] = True #sets ACK to true
              ack = "ACKNOWLEDGE " + str(parsed_message[1]) +" " +word +" " +str(list[3])
              return ack
            else: #timestamp was expired, decline
              decline = "DECLINE "+str(parsed_message[1]) +str(parsed_message[2]) 
              return decline  
      if(match):#if the request was matched
        pass#this is taken care of in the above scenario
      else: #no match was found, send decline
        decline = "DECLINE "+str(parsed_message[1]) +str(parsed_message[2]) 
        return decline
      #end request here
        
      
    elif request == "RELEASE":
      for list in records:#Record = [num in records, client's MAC, New IP address, timestamp, ACK]
        if(list[1] == parsed_message[1]): #finds MAC address in list
          timestamp = datetime.fromisoformat(isotimestring)
          list[3] = timestamp#if found, make timestamp = current time (expiring it)
          list[4] = False #sets ACK to False
        else: #MAC not found
          pass #nothing happens
      #end RELEASE

      
    elif request == "RENEW":
      for list in records:#Record = [num in records, client's MAC, New IP address, timestamp, ACK]
        if(list[1] == parsed_message[1]): #finds MAC address in list
          timestamp = datetime.fromisoformat(isotimestring) 
          u60secfromnow = timestamp + timedelta(seconds=60) #new timestamp w 60 second expiration
          list[3] = u60secfromnow #renew timestamp
          list[4] = True #set ACKED to true
          ack = "ACKNOWLEDGE " + str(parsed_message[1]) +" " +str(list[2]) +" " +str(list[3])
          return ack
        else: #mac not found          ~ ~ ~TODO~ ~ ~
          for list in records:#Record = [num in records, client's MAC, New IP address, timestamp, ACK]
            if(checkTimeStamp(list[3])): #if timestamp was not expired
              pass #do nothing, those are ok
            else:#timestamp was expired
              list[1] = requestMAC #sets the MAC to the IP
              timestamp = datetime.fromisoformat(isotimestring) 
              u60secfromnow = timestamp + timedelta(seconds=60) #new timestamp w 60 second expiration
              list[3] = u60secfromnow #renew timestamp
              list[4] = False #set ACKED to False
              offer = "OFFER " +str(list[1]) +" " +str(list[2]) +" "+str(list[3]) #offer message
              return offer
          #no available records
          decline = "DECLINE "+str(parsed_message[1]) +str(parsed_message[2]) 
          return decline
      #end of RENEW



          
          
# Start a UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Avoid TIME_WAIT socket lock [DO NOT REMOVE]
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

SERVER_IP = socket.gethostname() 
server.bind((SERVER_IP, 9000)) #server.bind(("", 9000))
print("DHCP Server running...")

try:
    while True:
        message, clientAddress = server.recvfrom(4096)
        print("Server received <- " +str(message.decode()))#a message to show received message
        parsed_message = parse_message(message)#so bad

        response = dhcp_operation(parsed_message)
        if(response is None): #such as when a RELEASE was processed
          pass
        else:
          print("Server sending -> " +(response))
          server.sendto(response.encode(), clientAddress)
except OSError:
    pass
except KeyboardInterrupt:
    pass

server.close()
