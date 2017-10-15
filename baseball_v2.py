from itty import *  
import urllib2  
import json  
import random  

roomid_list = []
roomid_rn_dict = {}

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
    print webhook['data']['roomId']
    
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))  
    result = json.loads(result) 
    
    roomid = str(result.get('roomId', ''))
    print roomid
    #print result
    print type(roomid)
    
    
    

    msg = None 
    
    
    
    
    if webhook['data']['personEmail'] != bot_email:  
        in_message = result.get('text', '').lower() 
        in_message = in_message.replace("baseball ", '')  
        
        if 'start' in in_message:
            global rn
            rn = ["0", "0", "0"]
            rn[0] = str(random.randrange(1, 9, 1))
            rn[1] = rn[0]
            rn[2] = rn[0]

            while (rn[0] == rn[1]):
                rn[1] = str(random.randrange(1, 9, 1))

            while (rn[0] == rn[2] or rn[1] == rn[2]):
                rn[2] = str(random.randrange(1, 9, 1))
            
            
            roomid_rn_dict[roomid] = rn
            
            
            print rn
            print roomid_rn_dict
            
            msg = "Let's start baseball game"
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
            msg = "Put any 3 number:"
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
            
            global t_cnt
            t_cnt = 1
            print t_cnt
            
        else:  #3 digits is typed             
            #t_cnt = 0# try count
            s_cnt = 0 # strike count
            b_cnt = 0 # ball count
            
            num = str(in_message)
            print num
            
            for i in range(0, 3):
	            for j in range(0, 3):
		            if(num[i] == str(roomid_rn_dict[roomid][j]) and i == j):
			            s_cnt += 1
		            elif(num[i] == str(roomid_rn_dict[roomid][j]) and i != j):
			            b_cnt += 1
				    
            #t_count += 1
            
            if s_cnt == 3:
                msg = "Result : [ {} ] Strike [ {} ] Ball".format(s_cnt,b_cnt)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                msg = "Great, you did it in {} times".format(t_cnt)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                msg = "one more ?  then say \"start\" again"
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
            
            else:
                msg = "Result : [ {} ] Strike [ {} ] Ball".format(s_cnt,b_cnt)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                msg = "Put any 3 number:"
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                t_cnt += 1
                print t_cnt
                
    return "true"  

    
    
    
  
####CHANGE THESE VALUES#####  
bot_email = "BaseBall@sparkbot.io"  
bot_name = "baseball"  
bearer = "NDRiMTRiOWUtMmNlNS00MGRkLWE3ZmUtMjk4NmE0N2IxYWMxNjE1NTVjOTMtNDA1"    
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"  
run_itty(server='wsgiref', host='0.0.0.0', port=8080)
