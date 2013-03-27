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

def get_git(sort="", fields="", date_range=""):
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

    fields_query = { "$and" : [] }

    if date_range != "":
        date_array = date_range.split(",")
        date_from = date_array[0]
        date_to = date_array[1]
        date_struct = {}
        date_struct["created"] = {}
        if date_from != "":
            date_struct["created"]["$gte"] = date_from
        if date_to != "":
            date_struct["created"]["$lte"] = date_to

        fields_query["$and"].append(date_struct)

    if fields != "":
        fields_array = fields.split(",")
        for field in fields_array:
            key = field.split(".")[0]
            value = field.split(".")[1]
            value_struct = {}
            if "|" in value:
                value_array = value.split("|")
                
                value_struct["$or"] = []

                for value in value_array:
                    value_struct["$or"].append( { key : value.decode("utf-8") } )

            else:
                value_struct[key] = value.decode("utf-8")

            fields_query["$and"].append(value_struct)

    if fields_query["$and"].__len__() == 0:
        fields_query = {}

    # print sort, " | ", sort_array, " | ", sorting

    # { "$or" : [{ "responsible" : "vgulaev" },{"responsible" : "parshin"}], "created" : { "$gte" : "2013-03-18T01:01:01Z", "$lte" : "2013-03-24T01:01:01Z" } }

    # ?sort=created_date,org_subname,responsible,initiator,state&date_range=2013-03-18T01:01:01Z,2013-03-20T01:01:01Z&fields=responsible.vgulaev|parshin

    print fields_query

    stored_issues = db.issues.find( fields_query ).sort( sorting )

    for issue in stored_issues:
        print issue
        if issue["state"] == "open":
            print "<tr class='open'>"
        else:
            print "<tr class='closed'>"
        print "<td>", issue["git_id"], "</td>"
        print "<td>", issue["org_subname"].encode("utf-8"), "</td>"
        print "<td>", issue["short_title"].encode("utf-8"), "</td>"
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

if "date_range" in get:
    date_range = get["date_range"].value
else:
    date_range = ""


print "<table>"
get_git(sort, fields, date_range)
print "</table>"