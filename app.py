import os
import datetime
import myCalendar

from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import env


app = Flask(__name__)


app.config["MONGO_DBNAME"]="leave_request_manager"
app.config["MONGO_URI"]=os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')

def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')

def dashboard():
    dayNames=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

    current_date= datetime.datetime.now()
    year=int(current_date.strftime("%Y"))
    month=int(current_date.strftime("%m"))
    month_name=myCalendar.get_month_long_name(month)
    current_day=current_date
    days=myCalendar.get_calendar_by_year_month(year,month)
    last_day=myCalendar.last_day_of_month(year,month)
    
    date_from=datetime.datetime(year,month,1,0,0,0)
    date_to=datetime.datetime(year,month,last_day,0,0,0) 
    calendar_filter=mongo.db.userslist.find(
                {
                "leave_request.from":
                    {"$gte":date_from},
                "leave_request.to":
                    {"$lte":date_to},
                "leave_request.approved":True
                })
    userslist=mongo.db.userslist.find()

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
            year=year
            )

@app.route('/dashboard/<status>', methods=['POST'])

def leave_requests_datatable(status):

    userslist = mongo.db.userslist.find()
    showTable = True
    
    if status == 'approved_requests':
        approved_status=True
        users=mongo.db.userslist.find({'leave_request.approved': approved_status})
        return render_template('leaveRequestTable.html',userslist=userslist,users=users,showTable=showTable,crumbname=status)
    
    elif status == 'rejected_requests':
        rejected_status=True
        users=mongo.db.userslist.find({'leave_request.rejected': rejected_status})
        return render_template('leaveRequestTable.html',userslist=userslist,users=users,showTable=showTable,crumbname=status)
    
    elif status == 'to_be_approved':
        approved_status=False
        rejected_status=False
        users = mongo.db.userslist.find({'leave_request.rejected': rejected_status,'leave_request.approved': approved_status})
        return render_template('leaveRequestTable.html',userslist=userslist,users=users,showTable=showTable,crumbname=status)
    
    elif status == 'all_requests':
        return render_template('leaveRequestTable.html',userslist=userslist,crumbname=status)
    else:

        return render_template('leaveRequestTable.html',userslist=userslist,users=users,crumbname=status)

@app.route('/leave_request')

def leave_request():
    userslist = mongo.db.userslist.find()
    return render_template('leaveRequest.html',userslist=userslist,crumbname="New Leave Request")

@app.route('/insert_leave_request',methods=['POST'])

def insert_leave_request():
    req = request.form.to_dict()
    print(req)
    return redirect(url_for('dashboard'))

@app.route('/dashboard/calendar/<year>/<month>/<day>')

def calendarview(year,month,day="1"):
    dayNames=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    year=int(year)
    month=int(month)
    input_day=int(day)
    input_date=datetime.datetime(year,month,input_day)
    month_name=myCalendar.get_month_long_name(month)
    status=str(year)+"-"+str(month)
    days=myCalendar.get_calendar_by_year_month(year,month)
    last_day=myCalendar.last_day_of_month(year,month)
    today_date=datetime.datetime.now()
    selected_date= "" if day else input_date
    date_from=datetime.datetime(year,month,1,0,0,0) if day else input_date
    date_to=datetime.datetime(year,month,last_day,0,0,0) if day else input_date

    calendar_filter=mongo.db.userslist.find(
                {
                "leave_request.from":
                    {"$gte":date_from},
                "leave_request.to":
                    {"$lte":date_to},
                "leave_request.approved":True
                })
    userslist=mongo.db.userslist.find()

    return render_template(
            'leaveRequestTable.html',
            userslist=userslist,
            days=days,
            users=calendar_filter,
            crumbname=status,
            showTable=True,
            dayNames=dayNames,
            year=year,
            month=month,
            month_name=month_name,
            selected_date=selected_date,
            today=today_date
            )

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)