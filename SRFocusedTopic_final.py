from __future__ import unicode_literals, absolute_import, print_function
import json
import requests
import re
import bdblib
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d
        
        

def task(env, query, send_email):
    """
    SRFocusedTopic Search
    
    This tool is a kind of advanced option for Topic search
    to make grouping search output based on TAC SR#. 
    It will help TAC engineer to use Topic search more efficiently
    to find relevant result for the issue. 
    because all of search output can be displayed as main TAC SR# <title> 
    and subsidiary composed of others. 
      
      - CDET/DDTS (linked defects) 
      - Newsgroup 
      - TechZone
    
    Parameters:
    - <Search Keyword (query)>  :  
        Search Keyword should be specific based on your issue. 
    - <The result may take a while, Send email with results? (send email)> : 
        you don't have to wait for the result. it will send email with the result.
    
    """
    try:
        data_c3 = topic_query(env, query, ['table:c3'], "100")
        json_str_c3_docu = json.dumps(data_c3['documents'])
        dict_c3 = json.loads(json_str_c3_docu, object_hook=JSONObject)
    except Exception as E:
        logger.info('C3 failed {}'.format(E))
        print('no c3 data')
        return
    
    
    try:
        data_news = topic_query(env, query, ["table:news"], "200")
        json_str_news_docu = json.dumps(data_news['documents'])
        dict_news = json.loads(json_str_news_docu, object_hook=JSONObject)
    except Exception as E:
        logger.info('News failed {}'.format(E))
        pass
    
    
    try:
        data_tech = topic_query(env, query, ["table:techzone"], "200")

        json_str_tech_docu = json.dumps(data_tech['documents'])
        dict_tech = json.loads(json_str_tech_docu, object_hook=JSONObject)
    except Exception as E:
        logger.info('TZ failed {}'.format(E))
        pass
    
    

    
    
    
    ### ==============================  #### 
    ### SR list prepare ###
    
    
    SR_Number = []

    i = 0

    while i < len(dict_c3):
        SR_Number.append(dict_c3[i].fields.identifier[0].encode('ascii','ignore'))
        i = i + 1
        

    html = []

    for i in range(len(SR_Number)):
        html.append("")
        
    
    
    
    ### ==============================  #### 
    ### Linked defects grouping based on SR ###
    
    SR_index = 0
    index = 0
    
    if 'documents' in data_c3.keys():
        
        while SR_index < len(SR_Number):

            html[SR_index] += '<table border="1">'
            html[SR_index] += '<tr><th>%s'%(dict_c3[SR_index].fields.identifier[0].encode('ascii','ignore')) + '</th>'

            html[SR_index] += '<td><table border="1">'
            html[SR_index] += '<tr><th width="50">CSOne</th><td width="750"><ul>' + '<a href = "%s" target="_blank">%s</a>'\
                              %(dict_c3[SR_index].fields.uri[0].encode('ascii','ignore'),dict_c3[SR_index].fields.title[0].encode('ascii','ignore')) +\
                              '</ul></td></tr>'
            
            if 'linkeddefects' in data_c3['documents'][SR_index]['fields'].keys():
                defects_list = dict_c3[SR_index].fields.linkeddefects[0].encode('ascii','ignore').split()
                defects_index = 0
            
                while defects_index < len(defects_list):
                    start_time = time.clock()
                    html[SR_index] += '<tr><th width="50">Defect</th><td width="750"><ul>' + \
                                      '<a href = "%s">%s</a>'%('https://wwwin-tools.cisco.com/casekwery/getServiceRequest.do?id='+ \
                                      defects_list[defects_index], defects_list[defects_index] + " - " + topic_query(env, defects_list[defects_index])) +\
                                      '</ul></td></tr>'

                    logger.info(time.clock() - start_time)
                    defects_index = defects_index + 1
                    time.sleep(0.4)   #Defined limits: Requests per sec: not to exceed - 1
                
            index = 0
            SR_index = SR_index + 1
            
    else:
        print("no c3 data")
        

    ### ==============================  #### 
    ### Newsgroup  grouping based on SR ###        
        
    SR_index = 0
    index = 0
    
    if 'documents' in data_news.keys():
        while SR_index < len(SR_Number):                
            while index < len(dict_news):
                match = re.search(SR_Number[SR_index], dict_news[index].fields.title[0].encode('ascii','ignore'))
                
                if match > 1:
                    html[SR_index] += '<tr><th width="50">News</th><td width="750"><ul>' +\
                                      '<a href = "%s" target="_blank">%s</a>'%(dict_news[index].fields.uri[0].encode('ascii','ignore'),\
                                                                               dict_news[index].fields.title[0].encode('ascii','ignore')) +\
                                      '</ul></td></tr>'
                                  
                    break
            
                else:
                    index = index + 1
                
            index = 0
            SR_index = SR_index + 1
            
    else:
        print("no news data")
        
    
    ### ==============================  #### 
    ### TechZone  grouping based on SR ###
    
    
    SR_index = 0
    index = 0
    
    
    
    
    if 'documents' in data_tech.keys():
        
        while SR_index < len(SR_Number):
            while index < len(dict_tech):
                                              
                match = re.search(SR_Number[SR_index], dict_tech[index].fields.title[0].encode('ascii','ignore'))
                if match > 1:            
                    html[SR_index] += '<tr><th width="50">TZ</th><td width="750"><ul>' +\
                                      '<a href = "%s" target="_blank">%s</a>'%(dict_tech[index].fields.uri[0].encode('ascii','ignore'),\
                                                                               dict_tech[index].fields.title[0].encode('ascii','ignore')) + \
                                      '</ul></td></tr>'
                
                    break
            
                else:
                    index = index + 1
                
            index = 0
            SR_index = SR_index + 1
        
    else:
        print("no tz data")
        
            
    #----------- HTML fianlize -----------#
    
    html.sort(key=len, reverse=True)
    html = [x for x in html if re.search(r'<th width="50">[DNT]', x)]
    
    htmlpage = '</table></tr></table>'.join(html)
    htmlpage += '</table></tr></table>'
    
    result = bdblib.TaskResult()
    result.append(bdblib.HTML(htmlpage))
    
    
    #---------send emailHTML--------------#
    
    if send_email==True:
        now = time.localtime()
        Head = "SRFocusedTopic Result<br/>"
        Head += "Searched on {}-{}-{}. <br/>".format(now.tm_year, now.tm_mon, now.tm_mday)
        Head += "<br/>"
        Tail = "<br/>Thanks"
        addrFrom = "no-reply@cisco.com"
        addrTo = "{}@cisco.com".format(env.user_name)
        addrCc = "myeokim@cisco.com"
        subject = "SRFocusedTopic Result for {} on {}-{}-{}".format(query, now.tm_year, now.tm_mon, now.tm_mday)
        #htmlBody = Head + htmlpage + Tail
        htmlBody = htmlpage 
        emailHTML(addrFrom, addrTo, addrCc, subject, htmlBody)
    

    return result





#----------------- topic_query ----------------------#


def topic_query(env, query, source=["table:cdets"], hits="1"):
    # Topic query API 
    
    json_string = '''{
    "appId": "cc7adc91e5",
    "query": "Need to Fill",
    "hits": "Need to Fill",
    "filterQuery": ["Need to Fill"],
    "fields":["identifier,linkeddefects"],
    "securityRealmId": ["cisco"],
    "securityPrincipalId": ["myeokim"],
    "securityPrincipalName": ["myeokim"],
    "useragent": ["mozilla"],
    "userIpaddress": ["127.0.0.1"],
    "clientHost": ["clientHost"],
    "clientIpaddress": ["127.0.0.1"],
    "appName": ["Topic Tool"],
    "appOwner": ["myeokim"]}'''
    json_req = json.loads(json_string)



    #Header
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=utf-8'}

    #Topic API URL
    url = 'https://wsgi.cisco.com/cso/search/SearchExtService'

    json_req['query'] = query
    json_req['filterQuery'] = source
    json_req['hits'] = hits
    
    payload = 'query=' + json.dumps(json_req) + '&src=TOPIC'

    result = requests.post(url, data=payload, headers=headers, cookies=env.cookies)
    data= result.json()
    
    if json_req['filterQuery'] == ["table:cdets"]:
        json_str_cdets_docu = json.dumps(data['documents'])    
        dict_cdets = json.loads(json_str_cdets_docu, object_hook=JSONObject)
        defect_title = dict_cdets[0].fields.title[0].encode('ascii','ignore')
        return defect_title
    
    return data





#-----emailHTML function --------
def emailHTML(addrFrom, addrTo, addrCc=None, subject=None, htmlBody=None):
    """ 
    This script allows you to send a HTML email. Eg: useful when you want to send preformatted text, etc,
    with all the flexibility of html to build the body

    Parameters:
    <addrFrom> From email address
    <addrTo> To email address (comma separated)
    <addrCc> Cc email address (comma separated)
    <subject> Email subject
    <htmlBody> Email body. Include any html tags you need.

    Returns:
    - None. Email just sent.
    """
    
    #Mail server
    smtp_server = 'outbound.cisco.com'

    # HTML MIME type email
    msg = MIMEMultipart('alternative')
    msg['To'] = addrTo
    if addrCc:
        msg['Cc'] = addrCc
        msg['From'] = addrFrom
    if subject:
        msg['Subject'] = subject
    if htmlBody:
        txtEmail = MIMEText(htmlBody, 'plain')
        htmlEmail = MIMEText(htmlBody, 'html')
        msg.attach(txtEmail)
        msg.attach(htmlEmail)

        # Send it
    s = smtplib.SMTP(smtp_server)
    s.sendmail(addrFrom, addrTo.split(",") + addrCc.split(","), msg.as_string())
    s.quit()



    