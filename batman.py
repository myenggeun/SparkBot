from itty import *  
import urllib2  
import json  
import random  
  
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
	
	rn = ["0", "0", "0"]
	rn[0] = str(random.randrange(1, 9, 1))
	rn[1] = rn[0]
	rn[2] = rn[0]

	while (rn[0] == rn[1]):
		rn[1] = str(random.randrange(1, 9, 1))

	while (rn[0] == rn[2] or rn[1] == rn[2]):
		rn[2] = str(random.randrange(1, 9, 1))

	#print(rn)

	t_cnt = 0 # 시도횟수
	s_cnt = 0 # 스트라이크 갯수
	b_cnt = 0 # 볼 갯수
	
	
	print("Let's start baseball game !!!")
	print("---------------------------")

	while ( s_cnt < 3 ):
		num = str(input("Put any 3 numbers : "))

		s_cnt = 0
		b_cnt = 0

		for i in range(0, 3):
			for j in range(0, 3):
				if(num[i] == str(rn[j]) and i == j):
					s_cnt += 1
				elif(num[i] == str(rn[j]) and i != j):
					b_cnt += 1
                
		print("Result : [" ,s_cnt, "] Strike [" ,b_cnt, "] Ball")
		t_cnt += 1

	print("---------------------------")
	print("Great, you did it in" , t_cnt , "times")
	
	"""
    if webhook['data']['personEmail'] != bot_email:  
        in_message = result.get('text', '').lower()  
        in_message = in_message.replace(bot_name, '')  
        if 'batman' in in_message or "whoareyou" in in_message:  
            msg = "I'm Batman!"  
        elif 'batcave' in in_message:  
            message = result.get('text').split('batcave')[1].strip(" ")  
            if len(message) > 0:  
                msg = "The Batcave echoes, '{0}'".format(message)  
            else:  
                msg = "The Batcave is silent..."  
        elif 'batsignal' in in_message:  
            print "NANA NANA NANA NANA"  
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})  
        if msg != None:  
            print msg  
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})  
    return "true"  
    """  
  
####CHANGE THESE VALUES#####  
bot_email = "BaseBall@sparkbot.io"  
bot_name = "BaseBall@spakbot.io"  
bearer = "NDRiMTRiOWUtMmNlNS00MGRkLWE3ZmUtMjk4NmE0N2IxYWMxNjE1NTVjOTMtNDA1"    
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"  
run_itty(server='wsgiref', host='0.0.0.0', port=8080)