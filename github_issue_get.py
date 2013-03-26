#-*- coding:utf-8 -*-

import requests, re, pymongo

r = requests.get('https://api.github.com/repos/vgulaev/trimet_it/issues')
r2 = requests.get('https://api.github.com/repos/vgulaev/trimet_it/issues?state=closed')

# print r.status_code

# print (r.text).encode("utf-8")


class GIT_Issue():
    title = ""
    body = ""
    label = ""
    created_time = ""
    closed_time = ""
    initiator = ""
    responsible = ""
    state = ""
    git_id = ""

    def __init__(self):
        pass

def get_issues(r):

    open_issues = []
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

                initiator_re = re.compile(r"\:.*\:", re.DOTALL)

                initiator_array = initiator_re.findall(x["title"].encode("utf-8"))

                for initiator in initiator_array:
                    print initiator

                    Issue.initiator = initiator

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

            if "closed_at" in x:
                print x["closed_at"]

                Issue.closed_time = x["closed_at"]

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
                issues.remove(issue)

        for gid in stored_issues_gid:
            if gid not in new_issues_gid:
                coll.remove( { "git_id" : gid } ) 

    
    for issue in issues:

        doc = {
            "git_id" : issue.git_id,
            "title" : issue.title,
            "label" : issue.label,
            "body" : issue.body,
            "created" : issue.created_time,
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
        new_issues_gid.append(issue.git_id)

    stored_issues_gid = db.issues.find( { "state" : "closed" } ).distinct("git_id")

    if stored_issues_gid.__len__() > 0:

        for issue in issues:
            if issue.git_id in stored_issues_gid:
                issues.remove(issue)

        for gid in stored_issues_gid:
            if gid not in new_issues_gid:
                coll.remove( { "git_id" : gid } ) 

    
    for issue in issues:

        doc = {
            "git_id" : issue.git_id,
            "title" : issue.title,
            "label" : issue.label,
            "body" : issue.body,
            "created" : issue.created_time,
            "closed" : issue.closed_time,
            "initiator" : issue.initiator,
            "responsible" : issue.responsible,
            "state" : issue.state
        }

        coll.save(doc)



open_issues = get_issues(r)
closed_issues = get_issues(r2)

insert_open_in_mongo(open_issues)
insert_closed_in_mongo(closed_issues)


# conn = pymongo.Connection()
# db = conn.issues
# coll = db.issues

# stored_issues = db.issues.find( { "state" : "open" } ).distinct("git_id")

# print stored_issues