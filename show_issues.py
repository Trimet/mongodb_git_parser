#!/usr/bin/python2.6
# -*- coding: utf-8 -*-


import sys,os
import cgi
import cgitb; cgitb.enable()

import pymongo

print ("Content-Type: text/html; charset=utf-8\n")

print """
    <style>
        td{
            
            border-right: 1px dotted gray;
            padding: 5px 25px 5px;
            border-bottom: 1px dotted gray;
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

def get_git(sort="", fields=""):
    conn = pymongo.Connection()
    db = conn.issues
    coll = db.issues

    if not sort == "":
        sorting = []
        sort_array = sort.split(",")
        for sort_value in sort_array:
            sorting.append((sort_value,1))
    else:
        sorting = "created"


    a = ("org_subname",1)

    print sort, " | ", sort_array, " | ", sorting

    stored_issues = db.issues.find( { "$or" : [{ "responsible" : "vgulaev" },{"responsible" : "parshin"}], "created" : { "$gte" : "2013-03-18T01:01:01Z", "$lte" : "2013-03-24T01:01:01Z" } } ).sort( sorting )

    for issue in stored_issues:
        if issue["state"] == "open":
            print "<tr class='open'>"
        else:
            print "<tr class='closed'>"
        print "<td>", issue["git_id"], "</td>"
        print "<td>", issue["org_subname"].encode("utf-8"), "</td>"
        print "<td>", issue["title"].encode("utf-8"), "</td>"
        print "<td>", issue["initiator"].encode("utf-8"), "</td>"
        print "<td>", issue["responsible"], "</td>"
        print "<td>", issue["created"].replace("T"," ").replace("Z"," "), "</td>"
        if not issue["closed"] == None:
            print "<td>", issue["closed"].replace("T"," ").replace("Z"," "), "</td>"
        else:
            print "<td>", issue["closed"], "</td>"
        print "</tr>"

    # print 1
    # print stored_issues


get = cgi.FieldStorage()
if "sort" in get:
    sort = get["sort"].value
else:
    sort = ""

if "fields" in get:
    fields = get["fields"].value
else:
    fields = "" 


print "<table>"
get_git(sort, fields)
print "</table>"