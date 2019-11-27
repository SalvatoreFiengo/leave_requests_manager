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
@app.route('/dashboard/calendar/<year>/<month>/<day>')

def calendarview(year,month,day="1"):
    
    dayNames=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    year_month=myCalendar.year_month_flow(int(year),int(month))
    year=year_month[0]
    input_month=year_month[1] 
    input_day=int(day)
    input_date=datetime.datetime(year,input_month,input_day)
    month=input_date.strftime('%m')
    month_name=myCalendar.get_month_long_name(input_month)
    crumbname=month_name+"-"+str(year)
    days=myCalendar.get_calendar_by_year_month(year,input_month)
    last_day=myCalendar.last_day_of_month(year,input_month)
    today_date=datetime.datetime.now()
    selected_date= "" if day else input_date
    date_from=datetime.datetime(year,input_month,1,0,0,0) if day else input_date
    date_to=datetime.datetime(year,input_month,last_day,0,0,0) if day else input_date

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
            requests=requests
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
    crumbname=team if team else "All Teams"
    filtered=True if team else False
    teams=mongo.db.team.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('teams.html',teams=teams,requests=requests,show_teams=True,crumbname=crumbname,filtered=filtered)

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
        else:
            continue
        
    mongo.db.team.insert_one({'name':req['team_name'],'users':users,'managers':managers})
    return redirect(url_for('teams'))

@app.route('/teams/edit_team/<team_id>')

def edit_team(team_id):
    team=mongo.db.team.find_one({'_id':ObjectId(team_id)})
    userslist=mongo.db.userslist.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('editTeam.html',team=team, userslist=userslist,requests=requests,show_teams=True,crumbname='Edit "'+team["name"]+'" Team')

@app.route('/teams/update_team/<team_id>',methods=["POST"])
def update_team(team_id):
    req=request.form.to_dict()
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

@app.route('/teams/delete/<entry_id>/<scope>',methods=["POST"])
def delete_entry(entry_id,scope):
    email=request.form.get('user')
    _bin=mongo.db.bin.find_one()
    _bin_id=_bin["_id"]
    if scope == "team":
        selected_item_array=[]
        # items_in_userslist_array=[]
        selected_item =mongo.db.team.find_one({'_id':ObjectId(entry_id)})
        selected_item_array.append(selected_item)
        mongo.db.bin.update_one({'_id':ObjectId(_bin_id)},{'$set':{'teams':selected_item_array}},False)
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
        return redirect(url_for('update_team',team_id=entry_id)) 
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)