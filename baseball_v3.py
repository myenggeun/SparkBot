from itty import *  
import urllib2  
import json  
import random  

roomid_list = []
roomid_rn_dict = {}
image_index = 0
image_index_1 = 0



out = ["https://s-media-cache-ak0.pinimg.com/236x/f6/92/1d/f6921df5885460eeef55fe210d63dbde.jpg",\
        "http://i164.photobucket.com/albums/u4/jmendez2005/ThreeStrikes.jpg",\
        "https://s-media-cache-ak0.pinimg.com/564x/32/42/16/32421612cde253bee08f66b4155d0ca2.jpg",\
        "https://media1.popsugar-assets.com/files/thumbor/Kk2c3wwG7m9HhBWsuNah0UHs_o0/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2016/07/15/748/n/1922398/9ab0a3377e43d629_FFN_OHPIX_LAWRENCE_I_07142016_52122442/i/Iskra-Lawrence-Bikini-Beach-Miami-July-2016.jpg",\
        "http://bestanimations.com/Humans/Sexy/candice-swanepoel-hot-girl-gif-3.gif",\
        "http://bestanimations.com/Humans/Sexy/victoria-secret-hot-girls-1.gif",\
        "http://bestanimations.com/Humans/Sexy/victoria-secret-hot-girls-3.gif",\
        "http://bestanimations.com/Humans/Sexy/funny-hot-guy.gif",\
        "http://bestanimations.com/Humans/Sexy/sexy-hot-girl-animated-gif-12.gif",\
        "http://bestanimations.com/Humans/Sexy/kate-upton-hot-blond-girl-22.gif",\
        "http://bestanimations.com/Humans/funny-animated-guy-gif-1.gif",\
        "http://bestanimations.com/Humans/Sexy/kate-upton-hot-blond-girl-29.gif",\
        "http://bestanimations.com/Humans/Sexy/Blondes/sexy-hot-blond-animated-gif-13.gif",\
        "http://bestanimations.com/Humans/Sexy/Blondes/sexy-hot-blond-animated-gif-11.gif",\
        "http://bestanimations.com/Humans/Sexy/Brunettes/sexy-hot-brunette-animated-gif-7.gif",\
        "http://bestanimations.com/Humans/Sexy/sexy-hot-girl-animated-gif-5.gif",\
        "http://bestanimations.com/Humans/Sexy/sexy-hot-girl-animated-gif-53.gif",\
        "http://bestanimations.com/Humans/Sexy/Blondes/hot-blond-girl-4.gif",\
        "http://bestanimations.com/Humans/Sexy/victoria-secret-hot-girls-1.gif"
        ]

out_1 = ["http://bestanimations.com/Humans/Sexy/sexy-hot-girl-animated-gif-14.gif",\
        "http://bestanimations.com/Humans/Sexy/sexy-hot-girl-animated-gif-8.gif",\
        "http://bestanimations.com/Humans/Sexy/sexy-hot-girl-animated-gif-47.gif",\
        "http://bestanimations.com/Humans/Sexy/Blondes/sexy-hot-blond-animated-gif-9.gif",\
        "http://bestanimations.com/Humans/Sexy/Brunettes/sexy-hot-brunette-animated-gif-7.gif",\
        "http://bestanimations.com/Humans/Sexy/Brunettes/sexy-brunette-girl-animated-gif-2.gif"
        ]

"""
out = ["http://bestanimations.com/Humans/Sexy/funny-hot-guy.gif",\
        "http://i164.photobucket.com/albums/u4/jmendez2005/ThreeStrikes.jpg",\
        "http://bestanimations.com/Humans/funny-animated-guy-gif-1.gif",\
        "http://bestanimations.com/Humans/Sexy/kate-upton-hot-blond-girl-22.gif"]
        

out_1 = ["http://bestanimations.com/Humans/Sexy/funny-hot-guy.gif",\
        "http://i164.photobucket.com/albums/u4/jmendez2005/ThreeStrikes.jpg",\
        "http://bestanimations.com/Humans/funny-animated-guy-gif-1.gif",\
        "http://bestanimations.com/Humans/Sexy/kate-upton-hot-blond-girl-22.gif"]
"""       
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
    """
    result_membership = sendSparkGET('https://api.ciscospark.com/v1/memberships/{0}'.format(webhook['data']['id']))
    result_membership = json.loads(result_membership)
    
    print result_membership
    """
    
    msg = None 
    
    
    
    
    if webhook['data']['personEmail'] != bot_email:  
        in_message = result.get('text', '').lower() 
        in_message = in_message.replace("baseball ", '')  
        
        if 'start' in in_message or 'hi' in in_message or 'hello' in in_message or 'help' in in_message:
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
            msg = "Put any 3 number (witnin 1-9, ex: @baseball 234) :"
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

            
            global t_cnt
            t_cnt = 1
            print t_cnt
            
            
        else:  #3 numbers is typed             
            #t_cnt = 0# try count
            global image_index
            global image_index_1
            
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
				    
            #t_cnt += 1
            
            
            if s_cnt == 3:
                print image_index
                if image_index < len(out)-1:
                    image_index += 1
                else:
                    image_index = 0
                print image_index
                
                if image_index_1 < len(out_1)-1:
                    image_index_1 += 1
                else:
                    image_index_1 = 0
                print image_index_1
                
                msg = "Result : [ {} ] Strike [ {} ] Ball".format(s_cnt,b_cnt)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                msg = "Great, you did it in {} times".format(t_cnt)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                rn = ["0", "0", "0"]  
                roomid_rn_dict[roomid] = rn
                
                if t_cnt < 6:
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": out_1[image_index_1]}) 
                else:
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": out[image_index]}) 
                  
                msg = "one more ?  then say \"start\" again"
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
        
            else:
                if roomid_rn_dict[roomid] == ["0", "0", "0"]:
                    msg = "say \"start\" again"
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                else:    
                    msg = "Result : [ {} ] Strike [ {} ] Ball".format(s_cnt,b_cnt)
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                    msg = "Put any 3 number (witnin 1-9, ex: @baseball 234) :"
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
                    t_cnt += 1
                    print t_cnt
                
    return "true"  

    
    
    
  
####CHANGE THESE VALUES#####  
bot_email = "BaseBall@sparkbot.io"  
bot_name = "baseball"  
bearer = "NDRiMTRiOWUtMmNlNS00MGRkLWE3ZmUtMjk4NmE0N2IxYWMxNjE1NTVjOTMtNDA1"    
 
run_itty(server='wsgiref', host='0.0.0.0', port=8080)