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

def get_query_string(field_name,field_array):
    if field_array != "":
        field_value_struct = {}
        if field_array.__len__() > 1:
            
            field_value_struct["$or"] = []
            for field in field_array:
                field_value_struct["$or"].append( { field_name : { "$regex" : u""+field.decode("utf-8") } } )
                # print value
        else:
            for field in field_array:
                field_value_struct[field_name] = { "$regex" : u""+field.decode("utf-8") }
        return field_value_struct
    else:
        return ""

def get_git(sort="", date_range="", initiator_array="", org_subname_array="", responsible_array=""):
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
        # print date_range
        date_array = date_range.split(",")
        date_from = date_array[0]
        date_to = date_array[1]
        date_struct = {}
        date_struct["created_date"] = {}
        if date_from != "":
            date_struct["created_date"]["$gte"] = date_from.encode("utf-8")
        if date_to != "":
            date_struct["created_date"]["$lte"] = date_to.encode("utf-8")
        if date_struct["created_date"].__len__() != 0:
            fields_query["$and"].append(date_struct)

    # if initiator_array != "":
    #     # initiator_value_struct
    #     if initiator_array.__len__() > 1:
    #         initiator_value_struct = {}
    #         initiator_value_struct["$or"] = []
    #         for initiator in initiator_array:
    #             initiator_value_struct["$or"].append( { "initiator" : { "$regex" : u""+initiator.decode("utf-8") } } )
    #             # print value
    #     else:
    #         initiator_value_struct["initiator"] = { "$regex" : u""+initiator.decode("utf-8") }
    #     fields_query["$and"].append(initiator_value_struct)

    if initiator_array != "":
        initiator_query = get_query_string("initiator", initiator_array)
        if initiator_query.__len__() != 0:
            fields_query["$and"].append(initiator_query)

    if responsible_array != "":
        responsible_query = get_query_string("responsible", responsible_array)
        if responsible_query.__len__() != 0:
            fields_query["$and"].append(responsible_query)

    if org_subname_array != "":
        org_subname_query = get_query_string("org_subname", org_subname_array)
        if org_subname_query.__len__() != 0:
            fields_query["$and"].append(org_subname_query)

    if fields_query["$and"].__len__() == 0:
        fields_query = {}

    # print sort, " | ", sort_array, " | ", sorting

    # { "$or" : [{ "responsible" : "vgulaev" },{"responsible" : "parshin"}], "created" : { "$gte" : "2013-03-18T01:01:01Z", "$lte" : "2013-03-24T01:01:01Z" } }

    # ?sort=created_date,org_subname,responsible,initiator,state&date_range=2013-03-18T01:01:01Z,2013-03-20T01:01:01Z&fields=responsible.vgulaev|parshin

    # print fields_query

    stored_issues = db.issues.find( fields_query ).sort( sorting )

    # stored_issues = db.issues.find( { "$and" : [{ "created_date" : { "$gte" : u"2013-03-18" } }] } ).sort( sorting )

    for issue in stored_issues:
        # print issue
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

if "dateFrom" in get:
    
    df = get["dateFrom"].value
    # print type(df)
    date_from_array = df.split("/")
    date_range = date_range+date_from_array[2]+"-"+date_from_array[0]+"-"+date_from_array[1]

if "dateTo" in get:
    # print 1
    dt = get["dateTo"].value
    # print type(dt)
    date_to_array = dt.split("/")
    date_range = date_range+","+date_to_array[2]+"-"+date_to_array[0]+"-"+date_to_array[1]
else:
    date_range = date_range+","

initiator_array = []
if "initiator" in get:
    if type(get["initiator"]) == list:
        for initiator in get["initiator"]:
            initiator_array.append( initiator.value )
    else:
        initiator_array.append( get["initiator"].value )
else:
    initiator = ""

org_subname_array = []
if "org_subname" in get:
    if type(get["org_subname"]) == list:
        for org_subname in get["org_subname"]:
            org_subname_array.append( org_subname.value )
    else:

        org_subname_array.append( get["org_subname"].value )
else:
    org_subname = ""

responsible_array = []
if "responsible" in get:
    if type(get["responsible"]) == list:
        for responsible in get["responsible"]:
            responsible_array.append( responsible.value )
    else:
        # print get["responsible"].value
        responsible_array.append( get["responsible"].value )
else:
    responsible = ""

# print initiator_array

print "<table>"
get_git(sort, date_range, initiator_array, org_subname_array, responsible_array)
print "</table>"