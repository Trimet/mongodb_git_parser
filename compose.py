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
    <style>
        select{
            height:200px;
        }
    </style>
</head>
<body>
    <form method="GET" action="show_issues.py">
        <select id="org_subname" name="org_subname" multiple>"""

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
                Показать задачи, открытые в период: <input type="textarea" name="dateFrom" class="dateInput dateFrom" /> - <input type="textarea" name="dateTo" class="dateInput dateTo" />                
        </div>
        <div class="dateChooser">
                Показать задачи, закрытые в период: <input type="textarea" name="dateFromClosed" class="dateInputClosed dateFromClosed" /> - <input type="textarea" name="dateToClosed" class="dateInputClosed dateToClosed" />                
        </div>
        <div>
            Отсортировать по параметрам: <input type="textarea" name="sort" id="sort" />
            <a href=# id="add_sort">+</a>
            <select id="sort_select">
                <option value="org_subname">Название организации</option>
                <option value="responsible">Ответственный</option>
                <option value="initiator">Кто назначил</option>
                <option value="created">Время создания</option>
                <option value="closed">Время закрытия</option>
                <option value="created_date">Дата создания</option>
                <option value="closed_date">Дата закрытия</option>
                <option value="state">Закрыто или нет</option>
            </select>
        </div>
        <input type="submit" />
    </form>
</body>
</html> """

print html_string