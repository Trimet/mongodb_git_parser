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

def get_git():
    conn = pymongo.Connection()
    db = conn.issues
    coll = db.issues

    stored_issues = db.issues.find( { }).sort( [("org_subname",1), ("responsible", 1), ("initiator",1), ("closed",-1)] )

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

print "<table>"
get_git()
print "</table>"