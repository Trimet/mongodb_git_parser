#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

### script for log parsing. shouldn't be here actually, would move someday ### 

import sys,os
import cgi
import cgitb; cgitb.enable()

import pymongo

print ("Content-Type: text/html; charset=utf-8\n")

print """
    <style>
        td{
            
            /*border-right: 1px dotted gray;*/
            padding: 5px 25px 5px;
            /*border-bottom: 1px dotted gray;*/
            background-color:#faeedd;
        }
        tr.open{
            font-size:11px;
            color:#45161c;
        }
        tr.closed{
            font-size:10px;
            color:#1f4037;
        }
    </style>
"""

conn = pymongo.Connection()
db = conn.logs
coll = db.terminal

user_name = "user"

logs = coll.find( { 'field5' : { '$regex' : user_name } } )
# logs = coll.find()

# file_obj = open(user_name+".csv", "w")
user = ""

print "<table>"

for log in logs:

        print "<tr>"
        print "<td>", log[u"Дата и время"], "</td>"
        user = user + "'" + log[u"Дата и время"].replace("\n","") + "'" + ","
        print "<td>", str(log[u"Код события"]), "</td>"
        user = user + "'" + str(log[u"Код события"]).replace("\n","") + "'" + ","
        text_array = log[u"field5"].encode("utf-8").split(":")
        # for text in text_array:

            # print "<td>", text, "</td>"
        # try:
        print "<td>", text_array[1], "</td>"
        user = user + "'" + text_array[1].replace("\n","").decode("utf-8") + "'" + ","
        # except:
        #     print "<td></td>"
        #     user = user + ","

        # try:
            
        user = user + "'" + text_array[3].replace("Код сеанса", "").replace("\n","").decode("utf-8") + "'" + ","
        print "<td>", text_array[3].replace("Код сеанса", ""), "</td>"
        # except:
        #     print "<td></td>"
        #     user = user + ","

        try:
            
            user = user + "'" + text_array[4].replace("Адрес сети источника", "").replace("\r\n","").replace("\n","").encode("utf-8") + "'" + ","
            print "<td>", text_array[4].replace("Адрес сети источника", ""), "</td>"
        except:
            print "<td></td>"
            user = user + ","

        try:
            print "<td>", text_array[5], "</td>"
            user = user + "'" + text_array[5].replace("\n","") + "'" + ";\n"
        except:
            print "<td></td>"
            user = user + ";\n"

        print "</tr>"

print "</table>"

# file_obj.write(user.encode("utf-8"))
# file_obj.close()

