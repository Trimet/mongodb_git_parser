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

                # if ":" in title:
                #     c = title.index(":")

                #     Issue.short_title = u''+title[0:c].decode("utf-8")


                # if ":" in title[c+1:]:
                #     z = title[c+1:].index(":")
                #     Issue.initiator = u''+title[z+1:c+z+1].decode("utf-8")


                initiator_re = re.compile(r":\W*:", re.DOTALL)

                initiator_array = initiator_re.findall(x["title"].encode("utf-8"))

                for initiator in initiator_array:
                    print initiator

                    Issue.initiator = initiator



                short_title_re = re.compile(r"\W*:", re.DOTALL)

                short_title_array = short_title_re.findall(x["title"].encode("utf-8"))

                for short_title in short_title_array:
                    print short_title

                    Issue.short_title = short_title

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
                "created" : issue.created_time,
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


# open_issues = get_issues(r)
# closed_issues = get_issues(r2)
# for issue in get_issues(r3):
#     closed_issues.append(issue)

# insert_open_in_mongo(open_issues)
# insert_closed_in_mongo(closed_issues)

clean_issues()

# conn = pymongo.Connection()
# db = conn.issues
# coll = db.issues

# stored_issues = db.issues.find( { "state" : "open" } ).distinct("git_id")

# print stored_issues