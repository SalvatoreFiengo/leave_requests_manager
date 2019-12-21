from bson.objectid import ObjectId
from flask import redirect
import datetime
"""mock used in error.html in which there is no need to retrieve the actual data"""
mock_requests = {
    "approved": 0,
    "rejected": 0,
    "to_be_approved": 0,
    "all_requests": 0
}
""" default error for error.html """
error = "default"


def get_items_number_by_status(collection):
    """function to get the number of requests and fill badges in dashboard controller"""
    results = {}
    all_results = 0
    approved = 0
    rejected = 0
    to_be_approved = 0
    for item in collection.find():
        if item["leave_request"]:
            for request in item["leave_request"]:
                if request["deleted"] == False:
                    all_results = all_results+1
                    if request["approved"] == True:
                        approved = approved+1
                    elif request["rejected"] == True:
                        rejected = rejected+1
                    elif request["approved"] == False and request["rejected"] == False:
                        to_be_approved = to_be_approved+1
    results = {
        "approved": approved,
        "rejected": rejected,
        "to_be_approved": to_be_approved,
        "all_requests": all_results
    }
    return results


def get_users_by_req(req):
    """when request contain multiple users (add user in 'add new team' or 'edit team'), 
    function uses string manipulation to get last number or two numbers from user parameters in html, 
    check if 'supervisor' checkbox is checked and return users array object"""
    users = []
    for item in req:
        n = -2
        _id = ObjectId()
        if not item[n].isnumeric():
            n = -1
        sliced = item[n]
        if item.startswith('email') and req.get('checkuser_'+sliced, False) == 'on':
            users.append(
                {
                    'userId': _id,
                    'name': req['name_'+sliced].lower(),
                    'surname': req['surname_'+sliced].lower(),
                    'email': req[item].lower(),
                    'approver': True,
                    'role': req['role_'+sliced].lower()
                })
        elif item.startswith('email') and req.get('checkuser_'+sliced, False) == False:
            users.append(
                {
                    'userId': _id,
                    'name': req['name_'+sliced].lower(),
                    'surname': req['surname_'+sliced].lower(),
                    'email': req[item].lower(),
                    'approver': False,
                    'role': req['role_'+sliced].lower()
                })
    return users
