#-*- coding:utf-8 -*-

import requests, re, pymongo

# r = []
# for x in range(2):

r = requests.get('https://api.github.com/repos/vgulaev/trimet_it/issues?page=1&per_page=200')
# r2 = []
# for x in range(7):

r2 = requests.get('https://api.github.com/repos/vgulaev/trimet_it/issues?page=1&per_page=200&state=closed')
r3 = requests.get('https://api.github.com/repos/vgulaev/trimet_it/issues?page=2&per_page=200&state=closed')
# print r.status_code

# print (r.text).encode("utf-8")


class GIT_Issue():
    title = ""
    body = ""
    label = ""
    created_date = ""
    closed_date = ""
    created_time = ""
    closed_time = ""
    initiator = ""
    responsible = ""
    state = ""
    git_id = ""
    short_title = ""
    org_subname = ""

    def __init__(self):
        pass

def get_issues(r):

    open_issues = []
    # for r in r_array:
    if r.status_code == 200:

        issues = r.json()

        for x in issues:

            Issue = GIT_Issue()

            if "labels" in x:
                for label in x["labels"]:
                    print label["name"].encode("utf-8")

                    Issue.label = label["name"].encode("utf-8")
                
            if "number" in x:
                print x["number"]

                Issue.git_id = x["number"]

            if "title" in x:
                print x["title"].encode("utf-8")

                title = x["title"].encode("utf-8")

                if ":" in title:
                    title_array = title.split(":")
                    Issue.org_subname = title_array[0]


                if title_array.__len__() > 2:
                    Issue.initiator = title_array[1]


                Issue.title = x["title"].encode("utf-8")

            if "body" in x:
                print x["body"].encode("utf-8")

                Issue.body = x["body"].encode("utf-8")

            if "state" in x:
                print x["state"].encode("utf-8")

                Issue.state = x["state"].encode("utf-8")

            if "assignee" in x:
                # print type(x["assignee"]), " ", dict
                if type(x["assignee"]) == dict: 
                    
                    if "login" in x["assignee"]:
                        print x["assignee"]["login"].encode("utf-8")

                        Issue.responsible = x["assignee"]["login"].encode("utf-8")

            if "created_at" in x:
                print x["created_at"]

                Issue.created_time = x["created_at"]

                Issue.created_date = x["created_at"].split("T")[0]


            if "closed_at" in x:
                print x["closed_at"]


                Issue.closed_time = x["closed_at"]
                if x["closed_at"] != None:
                    Issue.closed_date = x["closed_at"].split("T")[0]

            print "---------"

            open_issues.append(Issue)

    return open_issues



def insert_open_in_mongo(issues):
    conn = pymongo.Connection()
    db = conn.issues
    coll = db.issues

    new_issues_gid = []
    for issue in issues:
        new_issues_gid.append(issue.git_id)

    stored_issues_gid = db.issues.find( { "state" : "open" } ).distinct("git_id")

    if stored_issues_gid.__len__() > 0:

        for issue in issues:
            if issue.git_id in stored_issues_gid:
                # print issues
                issue = ""
                # issues2 = issues.remove(issue)
                # issues = issues2

        for gid in stored_issues_gid:
            if gid not in new_issues_gid:
                coll.remove( { "git_id" : gid } ) 

    
    for issue in issues:
        if issue != "":
            doc = {
                "git_id" : issue.git_id,
                "title" : issue.title,
                "short_title" : issue.short_title,
                "org_subname" : issue.org_subname,
                "label" : issue.label,
                "body" : issue.body,
                "created_date" : issue.created_date,
                "created" : issue.created_time,
                "closed_date" : issue.closed_date,
                "closed" : issue.closed_time,
                "initiator" : issue.initiator,
                "responsible" : issue.responsible,
                "state" : issue.state
            }

        coll.save(doc)


def insert_closed_in_mongo(issues):
    conn = pymongo.Connection()
    db = conn.issues
    coll = db.issues

    new_issues_gid = []
    for issue in issues:
        # print issue
        new_issues_gid.append(issue.git_id)

    stored_issues_gid = db.issues.find( { "state" : "closed" } ).distinct("git_id")

    if stored_issues_gid.__len__() > 0:

        for issue in issues:
            if issue.git_id in stored_issues_gid:
                issue = ""
                # issues = issues.remove(issue)

        ### git api return only limited number on page
        for gid in stored_issues_gid:
            if gid not in new_issues_gid:
                coll.remove( { "git_id" : gid } ) 

    
    for issue in issues:
        if issue != "":
            doc = {
                "git_id" : issue.git_id,
                "title" : issue.title,
                "short_title" : issue.short_title,
                "org_subname" : issue.org_subname,
                "label" : issue.label,
                "body" : issue.body,
                "created_date" : issue.created_date,
                "created" : issue.created_time,
                "closed_date" : issue.closed_date,
                "closed" : issue.closed_time,
                "initiator" : issue.initiator,
                "responsible" : issue.responsible,
                "state" : issue.state
            }

        coll.save(doc)

    

def clean_issues():
    conn = pymongo.Connection()
    db = conn.issues
    coll = db.issues

    stored_issues_gid = db.issues.find().distinct("git_id")
    for gid in stored_issues_gid:
        issues_copies = db.issues.find( { "git_id" : gid } )
        i = issues_copies.count()
        for copy in issues_copies:
            if i > 1:
                db.issues.remove( copy )

            i = i - 1
            print copy
        print "----"
        # if stored_issues_gid.count(gid) > 1:
        #     print "to del"
        #     coll.remove( gid, True) 


open_issues = get_issues(r)
closed_issues = get_issues(r2)
for issue in get_issues(r3):
    closed_issues.append(issue)

insert_open_in_mongo(open_issues)
insert_closed_in_mongo(closed_issues)

clean_issues()

# conn = pymongo.Connection()
# db = conn.issues
# coll = db.issues

# stored_issues = db.issues.find( { "state" : "open" } ).distinct("git_id")

# print stored_issues