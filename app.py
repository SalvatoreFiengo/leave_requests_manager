import os
import datetime
import myCalendar
import helper

from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import env


app = Flask(__name__)


app.config["MONGO_DBNAME"]="leave_request_manager"
app.config["MONGO_URI"]=os.environ.get("MONGO_URI")

mongo = PyMongo(app)

# home redirected to dashboard
@app.route('/')

def home():
    return redirect(url_for('dashboard'))

# dashboard overview - calendar plus holiday table filtered by month
@app.route('/dashboard')

def dashboard():
    dayNames=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    current_date= datetime.datetime.now()
    year=int(current_date.strftime("%Y"))
    month=current_date.strftime("%m")
    input_month=int(month)
    month_name=myCalendar.get_month_long_name(input_month)
    current_day=current_date
    days=myCalendar.get_calendar_by_year_month(year,input_month)
    last_day=myCalendar.last_day_of_month(year,input_month)
    date_from=datetime.datetime(year,input_month,1,0,0,0)
    date_to=datetime.datetime(year,input_month,last_day,0,0,0) 
    crumbname=month_name+"-"+str(year)
    calendar_filter=mongo.db.userslist.find(
                {
                "leave_request.from":
                    {"$gte":date_from},
                "leave_request.to":
                    {"$lte":date_to}
                })
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    return render_template(
            'leaveRequestTable.html',
            calendar=True,
            filtered=False,
            crumbname=crumbname,
            userslist=calendar_filter,
            days=days,
            dayNames=dayNames,
            month_name=month_name,
            today=current_day,
            month=month,
            input_month=input_month,
            year=year,
            requests=requests
            )

# dashboard leave requests menu 
@app.route('/dashboard/<status>',methods=["GET"])

def leave_requests_datatable(status):

    userslist = mongo.db.userslist.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)

    if status == 'approved_requests':
        approved_status=True
        users=mongo.db.userslist.find({'leave_request.approved': approved_status})
        return render_template('leaveRequestTable.html',userslist=users,requests=requests,crumbname=status,approval="approved",filtered=True,calendar=False)
    
    elif status == 'rejected_requests':
        rejected_status=True
        users=mongo.db.userslist.find({'leave_request.rejected': rejected_status})
        return render_template('leaveRequestTable.html',userslist=users,requests=requests,crumbname=status,approval="rejected",filtered=True,calendar=False)
    
    elif status == 'to_be_approved':
        approved_status=False
        rejected_status=False
        users = mongo.db.userslist.find({'leave_request.rejected': rejected_status,'leave_request.approved': approved_status})
        return render_template('leaveRequestTable.html',userslist=users,requests=requests,crumbname=status,approval="to_be_approved",filtered=True,calendar=False)
    
    elif status == 'all_requests':
        return render_template('leaveRequestTable.html',userslist=userslist,requests=requests,crumbname=status,filtered=False)
    else:
        return redirect(url_for('dashboard'))

# click on buttons approve/reject/delete will update leave request accordingly
@app.route('/dashboard/<status>', methods=["POST"])

def get_approval(status):
    req = request.form.to_dict()

    if req['approval']:
        mongo.db.userslist.update(
            {'_id':ObjectId(req['user_id']),'leave_request._leaveId':ObjectId(req['leave_id'])},
            {'$set':{'leave_request.$.'+req["approval"] : True}},**{'upsert':False})
    else:
        print('error')
    
    if req["approval"]=='approved':
        return redirect(url_for('leave_requests_datatable',status=status))  

    elif req["approval"]=='rejected':
        return redirect(url_for('leave_requests_datatable',status=status))

    else:
        return redirect(url_for('leave_requests_datatable',status=status))

# route to calendar passing date, leave requests table results filtered accordingly to selected month
@app.route('/dashboard/calendar/<year>/<month>')
@app.route('/dashboard/calendar/<year>/<month>/<day>')

def calendarview(year,month,day=""):
    
    dayNames=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    year_month=myCalendar.year_month_flow(int(year),int(month))
    year=year_month[0]
    input_month=year_month[1] 
    input_day=int(day) if day else 1 
    input_date=datetime.datetime(year,input_month,input_day,0,0,0)
    month=input_date.strftime('%m')
    month_name=myCalendar.get_month_long_name(input_month)
    days=myCalendar.get_calendar_by_year_month(year,input_month)
    last_day=myCalendar.last_day_of_month(year,input_month)
    selected_date= input_date if day else ""
    today_date=selected_date if day else datetime.datetime.now()
    crumbname=selected_date.strftime('%d-%m-%y') if day else month_name+"-"+str(year)
    date_from=input_date if day else datetime.datetime(year,input_month,1,0,0,0) 
    date_to=input_date if day else datetime.datetime(year,input_month,last_day,0,0,0) 
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    calendar_filter=mongo.db.userslist.find({
                "leave_request.from":
                    {"$lte":date_from},
                "leave_request.to":
                    {"$gte":date_to}
                }) if day else mongo.db.userslist.find(
                {
                "leave_request.from":
                    {"$gte":date_from},
                "leave_request.to":
                    {"$lte":date_to}
                })
    return render_template(
            'leaveRequestTable.html',
            userslist=calendar_filter,
            calendar=True,
            days=days,
            crumbname=crumbname,
            dayNames=dayNames,
            year=year,
            month=month,
            input_month=input_month,
            month_name=month_name,
            selected_date=selected_date,
            today=today_date,
            requests=requests,
            bin=False
            )

# route to form to submit a leave request 
@app.route('/leave_request')

def leave_request():
    userslist = mongo.db.userslist.find()
    teams = mongo.db.team.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('leaveRequest.html',userslist=userslist,teams=teams,requests=requests,crumbname="New Leave Request")

# form to submit leave requests - crud create 
@app.route('/insert_leave_request',methods=['POST'])

def insert_leave_request():
    req = request.form.to_dict()
    _leaveId = ObjectId()
    date_from= datetime.datetime.strptime(req['from'],"%d-%m-%Y")
    date_to= datetime.datetime.strptime(req['to'],"%d-%m-%Y")
    mongo.db.userslist.update(
    {'_id':ObjectId(req['user_id'])},
    {'$addToSet':
        {'leave_request':
            {'reason':req['reason'],
            'from': date_from,
            'to':date_to,
            'approved':False,
            'rejected':False,
            'deleted':False,
            'comments':req['comments'],
            '_leaveId':ObjectId(_leaveId)}}})
    return redirect(url_for('dashboard'))

# teams view and filter by team name via 'controller select team' 
@app.route('/teams', methods=["GET","POST"])
def teams():
    req=request.form.to_dict()
    team=req["team"] if req else ""
    filtered=True if team else False
    teams=mongo.db.team.find()
    selected_team=mongo.db.team.find_one({'_id':ObjectId(team)}) if team else ""
    crumbname=selected_team["name"] if team else "All Teams"
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('teams.html',teams=teams,requests=requests,show_teams=True,crumbname=crumbname,filtered=filtered,selected_team=selected_team)

#add new team
@app.route('/teams/add_team')
def add_new_team():
    userslist=mongo.db.userslist.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('addNewTeam.html',userslist=userslist,requests=requests,show_teams=True,crumbname="Add New Team")

@app.route('/teams/insert_team', methods=["POST"])
def insert_team():
    req= request.form.to_dict()
    users=[]
    managers=[]
    for item in req:
        if item.startswith('manager'):
            managers.append({'email':req[item],'approver':True})
        elif item.startswith('user') and req.get('checkuser_'+item[-1],False) == 'on' :
            users.append({'email':req[item],'approver':True,'role':req['role_'+item[-1]]})
        elif item.startswith('user') and req.get('checkuser_'+item[-1],False)==False :
            users.append({'email':req[item],'role':req['role_'+item[-1]]})
        
    mongo.db.team.insert_one({'name':req['team_name'],'users':users,'managers':managers})
    return redirect(url_for('teams'))

@app.route('/teams/edit_team', methods=["POST"])

def edit_team():
    team_id=request.form.get('team')
    all_teams=mongo.db.team.find()
    team=mongo.db.team.find_one({'_id':ObjectId(team_id)})
    userslist=mongo.db.userslist.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('editTeam.html',team=team, teams=all_teams, userslist=userslist,requests=requests,show_teams=True,crumbname='Edit "'+team["name"]+'" Team')

@app.route('/teams/update_team/',methods=["POST"])
def update_team():
    req=request.form.to_dict()
    team_id=req.get("team_id")
    team_name=req.get("team_name")
    users=[]
    managers=[]
    for item in req:

        if item.startswith('manager'):
            managers.append({'email':req[item],'approver':True})
        elif item.startswith('user') and req.get('checkuser_'+item[-1],False) == 'on' :
            users.append({'email':req[item],'approver':True,'role':req['role_'+item[-1]]})
        elif item.startswith('user') and req.get('checkuser_'+item[-1],False)==False :
            users.append({'email':req[item],'role':req['role_'+item[-1]]})
            
        else:
            continue  
    mongo.db.team.update_one({'_id':ObjectId(team_id)},{'$set':{'name':team_name,'users':users,'managers':managers}})
    return redirect(url_for('teams'))

@app.route('/teams/delete_entry/<scope>',methods=["GET","POST"])
def delete_entry(scope):
    if request.method == 'POST':
        _bin=mongo.db.bin.find_one()
        _bin_id=_bin["_id"]
        email=request.form.get('user_email')
        entry_id=request.form.get('entry_id')
        if scope == "team":
            entry_id=request.form.get('entry_id')
            selected_item_array=[]
            selected_item =mongo.db.team.find_one({'_id':ObjectId(entry_id)})
            selected_item_array.append(selected_item)
            mongo.db.bin.update_one({'_id':ObjectId(_bin_id)},{'$push':{'teams':selected_item_array}},False)
            mongo.db.team.remove({'_id':ObjectId(entry_id)})
            items_in_userslist = mongo.db.userslist.find({'team':selected_item["name"]})
            if items_in_userslist:
                for user in items_in_userslist:
                    if user['team']==selected_item['name']:
                        item_id=user['_id']
                        mongo.db.userslist.remove({'_id':ObjectId(item_id)})
            return redirect(url_for('teams'))  
        elif scope=="user":
            selected_item_array=[]
            item_in_userslist_array=[]
            selected_item = mongo.db.team.find_one({'_id':ObjectId(entry_id),'users.email':email})
            selected_item_array.append(selected_item)
            for i in selected_item["users"]:
                if i['email']==email:
                    mongo.db.bin.update_one({'_id':ObjectId(_bin_id)},{'$push':{'team_memebers.users':i}})
                    mongo.db.team.update_one({'users.email':email},{'$pull':{'users':i}})

            item_in_userslist = mongo.db.userslist.find_one({'email':email})
            if item_in_userslist != None:
                item_id=item_in_userslist["_id"]
                item_in_userslist_array.append(item_in_userslist)
                mongo.db.bin.update_one({'_id':ObjectId(_bin_id)},{'$push':{'team_memebers.requests':item_in_userslist_array}})
                mongo.db.userslist.remove({'_id':ObjectId(item_id)})
            return redirect(url_for('teams')) 
        elif scope=="manager":
            selected_item_array=[]
            item_in_userslist_array=[]
            selected_item = mongo.db.team.find_one({'_id':ObjectId(entry_id),'managers.email':email})
            selected_item_array.append(selected_item)
            for i in selected_item["managers"]:
                if i['email']==email:
                    mongo.db.bin.update_one({'_id':ObjectId(_bin_id)},{'$push':{'team_memebers.managers':i}})
                    mongo.db.team.update_one({'managers.email':email},{'$pull':{'managers':i}})
            return redirect(url_for('teams'))   

@app.route('/bin/<data_requested>')   
def get_bin(data_requested):
    try:
        deleted_items=mongo.db.bin.find()
    except:
        error="Something is wrong. Contsct your Administrator"
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    leave_requests=[]
    team_members=[]
    teams=[]
    if deleted_items:
        if data_requested=="team_members":
            for item in deleted_items:
                for user in item["team_members"]["users"]:
                    team_members.append(user)
                for manager in item["team_members"]["managers"]:
                    team_members.append(manager)
            keys=list(set().union(*team_members))
            keys.sort(reverse=True)
            return render_template('bin.html',items=team_members, bin=True, crumbname="Bin/Users",requests=requests,data="users",keys=keys)
        elif data_requested == "requests":              
            for item in deleted_items:
                for cat in item["team_members"]["requests"]:
                    leave_requests.append(cat)
            keys=list(set().union(*leave_requests))
            keys.sort(reverse=True)
            return render_template('bin.html',items=leave_requests, bin=True, crumbname="Bin/Requests",requests=requests,data="requests",keys=keys)
        elif data_requested == "teams":
            keys=[]
            for item in deleted_items:
                for cat in item["teams"]:
                    teams.append(cat)
            keys=["team name","users","managers"]
            return render_template('bin.html',items=teams, bin=True, crumbname="Bin/Teams",requests=requests,data="teams",keys=keys)
    else:
        return render_template('error.html',error=error)
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)