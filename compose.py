#!/usr/bin/python2.6
# -*- coding: utf-8 -*-


import sys,os
import cgi
import cgitb; cgitb.enable()

import pymongo

print ("Content-Type: text/html; charset=utf-8\n")

conn = pymongo.Connection()
db = conn.issues
coll = db.issues

html_string = """<!DOCTYPE html>
<html>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<head>
    Подбор
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js" type="text/javascript"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.0/jquery-ui.min.js" type="text/javascript"></script>
    <script src="index.js" type="text/javascript"></script>
</head>
<body>
    <form method="GET" action="show_issues.py">
        <select id="org_name" name="org_name" multiple>"""

org_subnames = db.issues.find( {} ).distinct("org_subname")
for org_subname in org_subnames:
    html_string = html_string + '<option value="'+org_subname.encode("utf-8")+'">'+org_subname.encode("utf-8")+'</option>'          
            
html_string = html_string + """ </select>
        <select id="initiator" name="initiator" multiple>"""
initiators = db.issues.find( {} ).distinct("initiator")
for initiator in initiators:
    html_string = html_string + '<option value="'+initiator.encode("utf-8")+'">'+initiator.encode("utf-8")+'</option>'          
html_string = html_string + """</select>
        <select id="responsible" name="responsible" multiple>"""
responsibles = db.issues.find( {} ).distinct("responsible")
for responsible in responsibles:
    html_string = html_string + '<option value="'+responsible.encode("utf-8")+'">'+responsible.encode("utf-8")+'</option>'          
html_string = html_string + """</select>
        <br />

         
        <div class="dateChooser">
                Показать задачи в период: <input type="textarea" name="dateFrom" class="dateInput dateFrom" /> - <input type="textarea" name="dateTo" class="dateInput dateTo" />                
        </div>
        <input type="button" value="Выбрать" id="submit_button" />
    </form>
</body>
</html> """

print html_string