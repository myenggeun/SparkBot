from itty import *  
import urllib2  
import json  
  
  
def sendSparkGET(url):  
    """ 
    This method is used for: 
        -retrieving message text, when the webhook is triggered with a message 
        -Getting the username of the person who posted the message if a command is recognized 
    """  
    request = urllib2.Request(url,  
                            headers={"Accept" : "application/json",  
                                     "Content-Type":"application/json"})  
    request.add_header("Authorization", "Bearer "+bearer)  
    contents = urllib2.urlopen(request).read()  
    return contents  
     
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
    return contents  
     
 
 
@post('/')  
def index(request):  
    """ 
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark, 
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message, 
    further actions are taken. i.e. 
    /batman    - replies to the room with text 
    /batcave   - echoes the incoming text to the room 
    /batsignal - replies to the room with an image 
    """  
    webhook = json.loads(request.body)  
    print webhook['data']['id']  
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))  
    result = json.loads(result)  
    msg = None  
	
    if webhook['data']['personEmail'] != bot_email:  
        msg = result.get('text', '')  
        msg = msg.replace(bot_name, '')  
		
		url = "https://api.ciscospark.com/v1/rooms"  
		bearer = "YzM1N2M4ODAtNTZmYS00N2Y1LWExNjAtYzNkYzVlYWNkZTgzOWE0OGU1MzYtZTQw"

		request = urllib2.Request(url, headers={"Accept" : "application/json", "Content-Type":"application/json"})  
		request.add_header("Authorization", "Bearer "+bearer)  
		response = urllib2.urlopen(request).read()  



		t = response.split("id\":\"")

		k = len(t)
		print "number of room", k

		for j in range (1,k):
			roomid = t[j]
			roomid = roomid[0:76]
			roomid = roomid.encode("utf-8")
			print roomid
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": roomid, "text": msg})
			
    return "true"  
  
  
####CHANGE THESE VALUES#####  
bot_email = "BaseBall@sparkbot.io"  
bot_name = "BaseBall@spakbot.io"  
bearer = "NDRiMTRiOWUtMmNlNS00MGRkLWE3ZmUtMjk4NmE0N2IxYWMxNjE1NTVjOTMtNDA1"    
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"  
run_itty(server='wsgiref', host='0.0.0.0', port=8080)