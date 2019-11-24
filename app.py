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
    calendar_filter=mongo.db.userslist.find(
                {
                "leave_request.from":
                    {"$gte":date_from},
                "leave_request.to":
                    {"$lte":date_to},
                "leave_request.approved":True
                })
    userslist=mongo.db.userslist.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)
    print(requests)
    return render_template(
            'leaveRequestTable.html',
            userslist=userslist,
            days=days,
            users=calendar_filter,
            showTable=True,
            dayNames=dayNames,
            month_name=month_name,
            today=current_day,
            month=month,
            input_month=input_month,
            year=year,
            requests=requests
            )

# dashboard leave requests menu 
@app.route('/dashboard/<status>',methods=["GET","POST"])

def leave_requests_datatable(status):

    userslist = mongo.db.userslist.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)

    if status == 'approved_requests':
        approved_status=True
        users=mongo.db.userslist.find({'leave_request.approved': approved_status})
        return render_template('leaveRequestTable.html',userslist=users,requests=requests,crumbname=status)
    
    elif status == 'rejected_requests':
        rejected_status=True
        users=mongo.db.userslist.find({'leave_request.rejected': rejected_status})
        return render_template('leaveRequestTable.html',userslist=users,requests=requests,crumbname=status)
    
    elif status == 'to_be_approved':
        approved_status=False
        rejected_status=False
        users = mongo.db.userslist.find({'leave_request.rejected': rejected_status,'leave_request.approved': approved_status})
        return render_template('leaveRequestTable.html',userslist=users,requests=requests,crumbname=status)
    
    elif status == 'all_requests':
        return render_template('leaveRequestTable.html',userslist=userslist,requests=requests,crumbname=status)

# click on buttons approve/reject/delete will update leave request accordingly
@app.route('/dashboard/<status>/<user_id>/<leave_id>/<approval>', methods=["POST"])

def get_approval(status,user_id,leave_id,approval):
    mongo.db.userslist.update(
        {'_id':ObjectId(user_id),'leave_request._leaveId':ObjectId(leave_id)},
        {'$set':{'leave_request.$.'+approval : True}},**{'upsert':False})
    if approval=='approved':
        return redirect(url_for('leave_requests_datatable',status=status))    
    elif approval=='rejected':
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
                    {"$lte":date_to},
                "leave_request.approved":True
                })
    userslist=mongo.db.userslist.find()
    requests=helper.get_items_number_by_status(mongo.db.userslist)

    return render_template(
            'leaveRequestTable.html',
            userslist=userslist,
            days=days,
            users=calendar_filter,
            crumbname=crumbname,
            showTable=True,
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
    print(_leaveId)
    print(req)
    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)