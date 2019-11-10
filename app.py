import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)


app.config["MONGO_DBNAME"]="leave_request_manager"
app.config["MONGO_URI"]=os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')

def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')

def dashboard():
    userslist = mongo.db.userslist.find()
    leave_requests = mongo.db.leave_requests.find()
    return render_template('controller.html',userslist=userslist,requests=leave_requests)

@app.route('/dashboard/<status>', methods=['POST'])

def leave_requests_datatable(status):
    userslist = mongo.db.userslist.find()
    leave_requests = mongo.db.leave_requests.find()
    showTable = True
    if status == 'approved_requests':
        approved_status=True
        users=mongo.db.userslist.find({'leave_request.approved': approved_status})
        return render_template('controller.html',userslist=userslist,requests=leave_requests,users=users,showTable=showTable)
    elif status == 'rejected_requests':
        rejected_status=True
        users=mongo.db.userslist.find({'leave_request.rejected': rejected_status})
        return render_template('controller.html',userslist=userslist,requests=leave_requests,users=users,showTable=showTable)
    elif status == 'to_be_approved':
        approved_status=False
        rejected_status=False
        users = mongo.db.userslist.find({'leave_request.rejected': rejected_status,'leave_request.approved': approved_status})
        return render_template('controller.html',userslist=userslist,requests=leave_requests,users=users,showTable=showTable)
    elif status == 'all_requests':
        
        return render_template('controller.html',userslist=userslist,requests=leave_requests)

@app.route('/leave_request')

def leave_request():
    return render_template('leaveRequest.html')

@app.route('/insert_leave_request',methods=['POST'])

def insert_leave_request():
    req = request.form.to_dict()
    print(req)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)