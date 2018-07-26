#!/usr/bin/env python
# -*- coding: utf-8 -*-
### a really dumb script to parse the list of documents in error from the intranet.

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as BSoup
import time, random, sys
from datetime import timedelta, datetime   
import redis
import json
opts = Options()
opts.set_headless()
assert opts.headless  # operating in headless mode
import os
import logging

import hashlib




class notAdjustable(object):
    lastmod= ""
    name = ""
    pages = ""
    filing = ""
    error = ""
    errormessages= []
    lxt=""
    number=""
    output=""
    hashstr =""
    profil = ""
    tool=""
    producer =""
    pdfversion = ""
    size = ""

    def toDict(self):
        return {
            'hash' : self.hashstr,
            'lastmod' : self.lastmod,
            'name' : self.name,
            'pages' : self.pages,
            'lxt' : self.lxt,
            'profil' : self.profil,
            'errors' : self.errormessages,
            'output' : self.output,
            'tool': self.tool,
            'size': self.size,
            'producer' : self.producer,
            'pdfversion': self.pdfversion
        }
        
nonAjustables = []
s = redis.StrictRedis(host='redis-rcsl', port=6379, db=8)
r = redis.StrictRedis(host='redis-rcsl', port=6379, db=1)
browser = Firefox(options=opts)
status = {'login':False, 'doclist':False,'docinfo':False}
s.set('status', status)

def login(browser):
    
  
    

    url = "https://login.intranet.etat.lu/login/TAMLoginServlet?TAM_OP=cert_login&AUTHNLEVEL=&ERROR_CODE=0x00000000&ERROR_TEXT=Successful+completion&FAILREASON=&HOSTNAME=mjrcs.intranet.etat.lu&METHOD=GET&PROTOCOL=https&REFERER=&URL=%2Fmjrcs-intranet%2F&redirectUrl=https%3A%2F%2Fmjrcs.intranet.etat.lu%2Fmjrcs-intranet%2F&authMode=UP"

    
    browser = Firefox(options=opts)
    browser.get(url)

    
    username_input = browser.find_element_by_id('username')
    status.update({'login':True})
    s.set('status', status)

    
    status.update({'login':False})
    s.set('status', status)
    time.sleep(10)
        


    password_input = browser.find_element_by_id('password')
    u=os.environ['IAM_USER']
    p=os.environ['IAM_PASSWORD']

    if username_input:
        username_input.send_keys(u)
    if password_input:
        password_input.send_keys(p)

    button_submit=browser.find_element_by_id('connection')
    button_submit.click()
    loggedin=True
    return browser


browser = login(browser)


while True:
    
    logging.warning("Querying document list :")
    browser.get("https://mjrcs.intranet.etat.lu/mjrcs-intranet/jsp/secured/ListSealDocumentTrackingAction.action?FROM=FROM_MAIN_MENU")    

    
    try:
        startdate_input =browser.find_element_by_id("START_DATE")
        status.update({'doclist':True})
        logging.warning("Document List Successful")
        s.set('status', status)
    except:
        status.update({'doclist':False})
        s.set('status', status)
        time.sleep(10)

        logging.error("Failed")
        browser = login(browser)
        continue

    startdate_input.clear()
 


    d = datetime.today() - timedelta(days=5)
    daysAgo = d.strftime("%d/%m/%Y")




    startdate_input.send_keys(daysAgo)
    startdate_input.send_keys(Keys.TAB)
    time.sleep(1)

    browser.find_element_by_id("STATUS").send_keys("N")
    
    browser.find_element_by_tag_name("button").click()


    try:
        bs_obj = BSoup(browser.page_source, 'html.parser')
    except:
        continue
    #the following can fail if the intranet is down, which then crashes the script.
    try:
        rows = bs_obj.find('table',{'id':'SEAL_DOCUMENT_TRACKING'}).find('tbody').find_all('tr')
        status.update({'docinfo':True})
        s.set('status', status)
    except:
        status.update({'docinfo':False})
        s.set('status', status)
        time.sleep(10)

        logging.error("Failed")
        browser = login(browser)
        continue
        

    #list of already known hash strings of last modification datetime + doc title to avoid querying error messages 
    #for docments we already know about
    hashstrs = []
    for obj in nonAjustables:
        hashstrs.append(obj.hashstr)
    logging.warning(f"Memory containts {len(hashstrs)!s}")

    current_list=[]
    
    for row in rows:        
        cells = row.find_all('td')
        error = cells[8].get_text() 
        if error =="Non ajustable":
            
            doc = notAdjustable()
            doc.error=error
            doc.name = cells[5].get_text()
            doc.size = cells[6].get_text()
            doc.pages = cells[7].get_text()
            doc.lastmod = cells[4].get_text()
            doc.lxt = cells[2].get_text()
            id = f"{doc.name!s}{doc.lastmod!s}{doc.size!s}".encode()
            doc.hashstr = f"{hashlib.sha256(id).hexdigest()!s}"
            current_list.append(doc.hashstr)
            
            tdlink = cells[1]
            link = tdlink.find("a")            
            inner = link['onclick']
            doc.filing = inner[31:41]
            doc.number = inner[42:43]
            

            if doc.hashstr not in hashstrs:
                nonAjustables.append(doc)    
                doc.errormessages = []
                logging.warning(f"Getting new file info {doc.name!s}")
                browser.get(f"https://mjrcs.intranet.etat.lu/mjrcs-intranet/jsp/secured/ListSealDocumentTrackingDetailAction.action?idDossierSealDocument={doc.filing!s}&numDocSealDocument={doc.number!s}")
                content = browser.find_element_by_id('content')

                try:
                    tree = content.find_element_by_class_name('tree')
                    logging.warning("Success")
                except:
                    logging.error("Failed - skipping")
                    continue

                elements = tree.find_elements_by_tag_name("a")
                for element in elements:
                
                    msg = element.get_attribute('innerHTML')
                  
                    if "CIE_publications" in msg:
                        doc.profil = "publication"
                    if "CIE_strong" in msg:
                        doc.profil = "strong"
                    if "CIE_medium" in msg:
                        doc.profil = "medium"
                    if "CreatorTool :" in msg:
                        doc.tool = msg.split(":")[1].strip()
                    if "PDFVersion :" in msg:
                        doc.pdfversion = msg.split(":")[1].strip()
                    if "Producer :" in msg:
                        doc.producer = msg.split(":")[1].strip()


                redelements = tree.find_elements_by_class_name('red')

           


                messages = []
                for element in redelements[2:]:
                    msg = element.find_element_by_tag_name("a").get_attribute('innerHTML')

                    if msg not in ["PDF","SSS_RULESET_DEF_NAME","CompareWithPDFA1B", "PDF","Convert_to PDFA1B_for_CIE_publications (2018-01-30)", "Convert_to PDFA1B_for_CIE_strong (2018-01-30)", "Convert_to PDFA1B_for_CIE_medium (2018-01-30)"]:

                        links = element.find_elements_by_tag_name("a")
                        for link in links[1:]:
                            messages.append(link.get_attribute('innerHTML'))
                            #print (f"{doc.name!s} : {link.get_attribute('innerHTML')!s}")
                doc.errormessages = messages
                
    for doc in nonAjustables:
        if doc.hashstr not in current_list:
            logging.warning("removed 1 doc from memory")
            nonAjustables.remove(doc)
        

    
    for doc in nonAjustables:
        if doc.hashstr not in hashstrs:
            doc.output= "\n"
            doc.output= f"{doc.output!s}********************************************************************************"
            doc.output= f"{doc.output!s}\n{doc.lastmod!s} : {doc.name!s}"
            doc.output= f"{doc.output!s}\n********************************************************************************"
            messages = dict()
            pages = []

            for errormessage in doc.errormessages:

                if ":" in errormessage:
                    message = errormessage.split(":")[1]
                    if message in messages.keys():
                        pages = messages[message]
                        pages.append(errormessage.split(":")[0].replace("Page ",""))
                        
                        messages.update({message:pages})
                    else:
                        messages.update({message:[errormessage.split(":")[0].replace("Page ","")]})
                    
                else:
                    messages.update({errormessage: []})
            for message in messages.keys():
                if len(messages[message]) > 0:
                    if len(messages[message])>10:
                        last = messages[message][-1]
                        messages[message] =messages[message][0:10]
                        messages[message].append("...")
                        messages[message].append(last)

                    doc.output= f"{doc.output!s}\n{message!s} on pages : {messages[message]!s}"
                else:
                    doc.output= f"{doc.output!s}\n{message!s}"
            
            #sys.stdout.buffer.write(doc.output.encode())
            

            json_items = json.dumps(doc.toDict())
            r.set(doc.hashstr, json_items)

            #I will send this object into a database with the hash as primary key
        
    
    

    
    rand = random.randint(30,35)
    logging.warning(f"sleeping for {rand!s} seconds")

    time.sleep(rand)        


        
