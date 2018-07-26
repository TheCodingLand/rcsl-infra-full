# -*- coding: iso-8859-1 -*-
import datetime
import email
import imaplib
import mailbox
import codecs
import otXmlPost   
#import cgi
from xml.sax.saxutils import escape

import xml.etree.ElementTree as ET
host = 'mail.rcsl.lu'
userid = 'it@rcsl.lu'
passwd = 'Ctgsup*0322'
EMAIL_ACCOUNT = "it@rcsl.lu"
PASSWORD = "Ctgsup*0322"

mail = imaplib.IMAP4_SSL(host)
mail.login(EMAIL_ACCOUNT, PASSWORD)

mail.list()
mail.select('inbox')
result, data = mail.uid('search', None, "ALL") # (ALL/UNSEEN)
#status, email_ids = imap.search(None, '(ALL)') 
i = len(data[0].split())


ot = otXmlPost.otXml()
XmlResponse = ot.queryObjects(r'01. ITSM - Categories', ["Title,Path"])

categories = []
class Category:
	def __init__(self):
		self.title = ""
		self.path= ""
		self.number =""
		self.id = ""
		
		


tree = ET.fromstring(XmlResponse)
root= tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
for child in root:
	category = Category()
	category.id = child.attrib['id']
               #print child.attrib['id']
	for attribute in child:
		if attribute.get('name') =='Title':
			category.title = attribute.text
		if attribute.get('name') =='Number':
			category.number=attribute.text
		if attribute.get('name')== 'Path':
			category.path= attribute.text
		if attribute.get('o')== 'Path':
			category.path= attribute.text
	if "CTG" in category.path:
		categories.append(category)
#for cat in categories:
	#print cat.title + " : " + cat.id
                            


def create_ticket(title, description, user, category, solution, timespent, state):
	print "User : " + user
	
	if "julien" in user.lower():
		UserDisplayName = "Lebourg Julien"
	elif "sebastien" in user.lower():
		UserDisplayName = "Lentz Sebastien"
	elif "kristian" in user.lower():
		UserDisplayName = "Vuori Kristian"
	elif "fred" in user.lower():
		UserDisplayName = "Colin Frederique"
	else:
		print "User not found"
		return "User Not Found"
	if "progress" in state.lower():
		state = "In progress"
	if "new" in state.lower():
		state = "New"
	if "solved" in state.lower():
		state = "Solved"
	
	
	catnumber = ""
	print "CATEGORY :" + category.lower()
	if category != "":
		for cat in categories:
			#print cat.title
			if category.lower() in cat.title.lower():
				catnumber = "%s" % cat.id
	if catnumber == "":
		catnumber = "706057"
		
		

	
	
	ot = otXmlPost.otXml()
	XmlResponse = ot.addIncident_rawDesc(title, description, UserDisplayName, catnumber, solution)
	tree = ET.fromstring(XmlResponse)
	root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')
	IncidentId = root.attrib['objectId']
	key = "Applicant"
	type = "userdisplayname"
	ot = otXmlPost.otXml()
	XmlResponse = ot.modifyTicketRef(type, IncidentId, key, UserDisplayName)

	ot = otXmlPost.otXml()
	XmlResponse = ot.modifyTicket('LongIntVal', IncidentId, 'TimeSpent', timespent)
	ot = otXmlPost.otXml()
	XmlResponse = ot.modifyTicket('StringVal', IncidentId, 'Source', 'Internal Issues')
	
	ot = otXmlPost.otXml()
	key = "Responsible"
	XmlResponse = ot.modifyTicketRef(type, IncidentId, key, UserDisplayName)
	
	#ot = otXmlPost.otXml()
	#xmlresponse = ot.modifyRefValTicket(EventId, "RelatedIncident", IncidentId)
	
	#ot = otXmlPost.otXml()
	#XmlResponse= ot.modifyTicket('DateTimeVal', IncidentId, 'Creation Date','%s' % EventDate)
	ot = otXmlPost.otXml()
	XmlResponse = ot.modifyTicket('StringVal', IncidentId, 'State', state)
	
	return IncidentId
	

from email.header import decode_header
def getheader(header_text, default="ascii"):
	"""Decode the specified header"""

	headers = decode_header(header_text)
	header_sections = [unicode(text, charset or default)
					   for text, charset in headers]
	return u"".join(header_sections)

def ensure_unicode(v):
	if isinstance(v, str):
		v = v.decode('iso-8859-1').encode('utf8')
	return unicode(v)

	
def get_decoded_email_body(message_body):
	""" Decode email body.
	Detect character set if the header is not set.
	We try to get text/plain, but if there is not one then fallback to text/html.
	:param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
	:return: Message body as unicode string
	"""

	msg = email.message_from_string(message_body)

	text = ""
	if msg.is_multipart():
		html = None
		for part in msg.get_payload():

			#print "%s, %s" % (part.get_content_type(), part.get_content_charset())

			if part.get_content_charset() is None:
				# We cannot know the character set, so return decoded "something"
				text = "Description"
				continue

			charset = part.get_content_charset()

			if part.get_content_type() == 'text/plain':
				text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

			if part.get_content_type() == 'text/html':
				html = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

		if text is not None:
			return text.strip()
		else:
			return html.strip()
	else:
		text = unicode(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
		return text.strip()

for x in range(i):
	latest_email_uid = data[0].split()[x]
	result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
	# result, email_data = conn.store(num,'-FLAGS','\\Seen') 
	# this might work to set flag to seen, if it doesn't already
	raw_email = email_data[0][1] #RAW email est STR (byte)
	#print isinstance(raw_email, str) TRUE
	raw_email_string = ensure_unicode(raw_email)
	#print raw_email_string
	
	
	email_message_body = get_decoded_email_body(raw_email_string)
	#print email_message_body.decode('utf-8')
	email_message = email.message_from_string(raw_email_string)
	
	
	
	#output_file = codecs.open("test"+str(x)+".txt", 'w',encoding='utf-8')
	#output_file.write(raw_email_string.encode('utf-8'))
	#output_file.close()
	file_name = "latestemails.txt"
	input_file = open("latestemails.txt", 'r')
	
	last_email_date = email.utils.parsedate_tz(input_file.readline())
	
	if last_email_date:
		last_email_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(last_email_date))
	# Header Details
	

	date_tuple = email.utils.parsedate_tz(email_message['Date'])
	if date_tuple:
		local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
		local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
	
	if local_date > last_email_date:
		email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
		email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
		subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
		subject = email.header.decode_header(email_message['Subject'])
		subject = getheader(email_message['Subject'])
		#print getheader(email_message['Subject'])
		#subject = subject.encode('latin-1')
		
		subject = ensure_unicode(subject)
		email_from = ensure_unicode(email_from)
		email_to = ensure_unicode(email_to)
		# Body details
		for part in email_message.walk():
			if part.get_content_type() == "text/plain":
				body = email_message_body.decode('utf-8')
				state = "New"
				timespent = "0"
				category = ""
				if body =="":
					body="description"
				else:
					if "(state :" in body.lower():
						try:
							start = body.lower().find("(state :")+len("(state :")
							print "start state : %s" % start
							end = body[start:].find(")")
							print "end state : %s" % end
							state = body[start:start+end].strip()
							print state
						except:
							state = "New"
					if "(time :" in body.lower():
						try:
							start = body.lower().find("(time :")+len("(time :")
							end = body[start:].find(")")
							timespent = body[start:start+end]
						except:
							timespent = "0"
					if "(category :" in body.lower():
						print "found field category"
					
						try:
							start = body.lower().find("(category :")+len("(category :")
							end = body[start:].find(")")
							category = body[start:start+end].strip()
							print "found category" + category
						except:
							category = ""
				#body = part.get_payload(decode=True)
				#print body
				
				#print "SUBJECT :" + subject
				#print "BODY :" + body
				
				
				#file_name = "email_" + str(x) + ".txt"
				#output_file = codecs.open(file_name, 'w', encoding='utf-8')
				
				#output_file.write(r'From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s' %(email_from, email_to,local_message_date, subject, body))
				#output_file.close()
				#print escape(subject)
				#print escape(body.encode('utf-8'))
				body = escape(body)
				subject = escape(subject)
				body = body.encode("ascii", "xmlcharrefreplace")
				body = repr(body).replace(r'\r\n', '&#x000d;&#x000a;')[1:-1]
				subject = subject.encode("ascii", "xmlcharrefreplace")
				
							
							
				#body.replace(r'\\\\', r'\\')
				
				print body
				create_ticket(subject, body, email_from, category, 'TODO', timespent, state)
				
				#Sauvegarder la date du dernier email
				file_name = "latestemails.txt"
				output_file = open(file_name, 'w+')
				output_file.write(email_message['Date'])
				output_file.close()
				
				
			else:
				continue
			
			
			
