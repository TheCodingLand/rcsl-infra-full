# -*- coding: iso-8859-1 -*-
import sys
#from ot_queries_rewrite import *
from ot_queries import *

def ensure_uicode(strToEncode):
    #return strToEncode.decode('utf8', 'replace')
    return strToEncode

def createTicket(title,description,username):
    ticketId = addincident_query(title, description, username)
    print "your ticket ID is : %s" % (ticketId)

def getMyTickets(username):
    findMytickets(username)


if sys.argv[1] == "create":
    createTicket("%s" % ensure_uicode(sys.argv[2]), "%s" % ensure_uicode(sys.argv[3]), "%s" % ensure_uicode(sys.argv[4].replace(".", " ")))

if sys.argv[1] == "get":
    getMyTickets(ensure_uicode(sys.argv[2].replace(".", " ")))


if sys.argv[1] == "fermer":
    closeTicket(sys.argv[2].replace(" ", ""),sys.argv[3].replace(".", " "), sys.argv[4])

if sys.argv[1] == "search":
    searchTicket(sys.argv[2],sys.argv[3].replace(".", " "),sys.argv[4])

if sys.argv[1] == "assigncategory":
    assigncategory(sys.argv[2],sys.argv[3])

if sys.argv[1] == "admin":
    findAdmintickets(sys.argv[2].replace(".",""))

if sys.argv[1] == "classement":
    classement(sys.argv[2].replace(".",""))

if sys.argv[1] == "listcategories":
    list_categories()
#if sys.argv[1] == "search":
#    CreateTicket("%s" % ensure_uicode(sys.argv[2]), "%s" % ensure_uicode(sys.argv[3]), "%s" % ensure_uicode(sys.argv[4].replace(".", " ")))

#if sys.argv[1] == "searchuser":
#    CreateTicket("%s" % ensure_uicode(sys.argv[2]), "%s" % ensure_uicode(sys.argv[3]), "%s" % ensure_uicode(sys.argv[4].replace(".", " ")))

if sys.argv[1] == "test":
    print "test"
    print "caracteres speciaux : àèé".decode('latin1').encode('utf-8')
    print "pas de caractres speciaux"

exit(1)
