

#-*- coding: utf-8 -*-



import urllib2  
import json  

def sendSparkPOST(url, data):  
    """ 
    This method is used for: 
        -posting a message to the Spark room to confirm that a command was received and processed 
    """  
    request = urllib2.Request(url, json.dumps(data),  
                            headers={"Accept" : "application/json",  
                                     "Content-Type":"application/json"})  
    request.add_header("Authorization", "Bearer "+bearer)  
    contents = urllib2.urlopen(request).read()
    print contents
    return contents
  
  
url = "https://api.ciscospark.com/v1/rooms"  
bearer = "YzM1N2M4ODAtNTZmYS00N2Y1LWExNjAtYzNkYzVlYWNkZTgzOWE0OGU1MzYtZTQw"

request = urllib2.Request(url, headers={"Accept" : "application/json", "Content-Type":"application/json"})  
request.add_header("Authorization", "Bearer "+bearer)  
response = urllib2.urlopen(request).read()  



t = response.split("id\":\"")

k = len(t)
print "number of room", k

for j in range (1,k):
  room = t[j]
  room = room[0:76]
  room = room.encode("utf-8")
  print room
  sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": room, "text": "test link", "markdown" : "[cisco](http://www.cisco.com)"})



