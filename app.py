import os
import datetime
import math
from static.python import myCalendar
from static.python import helper
from flask import Flask, render_template, \
    redirect, request, url_for, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "leave_request_manager"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/favicon.ico')
def favicon():
    """favicon from folder to root as per documentation:
        https://flask.palletsprojects.com/en/0.12.x/patterns/favicon/"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    """home redirected to dashboard"""
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """ dashboard overview - calendar plus holiday table filtered by month"""
    dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    current_date = datetime.datetime.now()
    year = int(current_date.strftime("%Y"))
    month = current_date.strftime("%m")
    input_month = int(month)
    month_name = myCalendar.get_month_long_name(input_month)
    current_day = current_date
    days = myCalendar.get_calendar_by_year_month(year, input_month)
    last_day = myCalendar.last_day_of_month(year, input_month)
    month_start = datetime.datetime(year, input_month, 1, 0, 0, 0)
    month_end = datetime.datetime(year, input_month, last_day, 0, 0, 0)
    crumbname = month_name + "-" + str(year)
    teams = mongo.db.team.find()
    teams_length = mongo.db.team.count_documents({})
    userslist = mongo.db.userslist.find()
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    return render_template(
        'leaveRequestTable.html',
        calendar=True,
        filtered=False,
        crumbname=crumbname,
        userslist=userslist,
        teams=teams,
        days=days,
        dayNames=dayNames,
        month_name=month_name,
        today=current_day,
        month=month,
        input_month=input_month,
        year=year,
        month_start=month_start,
        month_end=month_end,
        requests=requests,
        teams_count=teams_length
    )


@app.route('/dashboard/<status>', methods=["GET"])
def leave_requests_datatable(status):
    """dashboard leave requests menu (controller) to filter view with
    all requests/approved/to be apporved or rejected requests"""
    teams = mongo.db.team.find()
    userslist = mongo.db.userslist.find()
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    teams_lenght = mongo.db.team.count_documents({})
    if teams_lenght < 1:
        message = "No leave requests found"
        error = "no leave requests"
        return render_template('error.html',
                               error=error,
                               requests=helper.mock_requests,
                               crumbname=status,
                               message=message)

    if status == 'approved_requests':
        approved_status = True
        users = mongo.db.userslist.find(
            {'leave_request.approved': approved_status})

        return render_template('leaveRequestTable.html',
                               teams=teams,
                               userslist=users,
                               requests=requests,
                               crumbname=status,
                               approval="approved",
                               filtered=True,
                               calendar=False,
                               teams_count=teams_lenght)

    elif status == 'rejected_requests':
        rejected_status = True
        users = mongo.db.userslist.find(
            {'leave_request.rejected': rejected_status})
        return render_template('leaveRequestTable.html',
                               teams=teams,
                               userslist=users,
                               requests=requests,
                               crumbname=status,
                               approval="rejected",
                               filtered=True,
                               calendar=False,
                               teams_count=teams_lenght)

    elif status == 'to_be_approved':
        approved_status = False
        rejected_status = False
        users = mongo.db.userslist.find(
            {
                'leave_request.rejected': rejected_status,
                'leave_request.approved': approved_status
            })
        return render_template('leaveRequestTable.html',
                               teams=teams,
                               userslist=users,
                               requests=requests,
                               crumbname=status,
                               approval="to_be_approved",
                               filtered=True,
                               calendar=False,
                               teams_count=teams_lenght)

    elif status == 'all_requests':
        return render_template('leaveRequestTable.html',
                               teams=teams,
                               userslist=userslist,
                               requests=requests,
                               crumbname=status,
                               filtered=False,
                               teams_count=teams_lenght)
    else:
        return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=["POST"])
@app.route('/dashboard/<status>', methods=["POST"])
def get_approval(status='none'):
    """if requsts are selected to click on buttons approve/reject/cancel
    will update leave request accordingly // crud update"""
    req = request.form.to_dict()
    if not req:
        return render_template('error.html',
                               error=helper.error,
                               requests=helper.mock_requests,
                               crumbname=status)

    if req['approval']:
        mongo.db.userslist.update(
            {
                '_id': ObjectId(req['user_id']),
                'leave_request._leaveId': ObjectId(req['leave_id'])
            },
            {
                '$set':
                {
                    'leave_request.$.' + req["approval"]: True
                }
            },
            **{
                'upsert': False
            })

    if req["approval"] == 'approved':
        return redirect(url_for('leave_requests_datatable',
                                status=status))

    elif req["approval"] == 'rejected':
        return redirect(url_for('leave_requests_datatable',
                                status=status))

    else:
        return redirect(url_for('dashboard'))


@app.route('/dashboard/calendar/<year>/<month>')
@app.route('/dashboard/calendar/<year>/<month>/<day>')
def calendarview(year, month, day=""):
    """route to calendar passing date,
    leave requests table results filtered accordingly to selected month"""
    dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    year_month = myCalendar.year_month_flow(int(year), int(month))
    year = year_month[0]
    input_month = year_month[1]
    input_day = int(day) if day else 1
    input_date = datetime.datetime(year, input_month, input_day, 0, 0, 0)
    month = input_date.strftime('%m')
    month_name = myCalendar.get_month_long_name(input_month)
    days = myCalendar.get_calendar_by_year_month(year, input_month)
    last_day = myCalendar.last_day_of_month(year, input_month)
    selected_date = input_date if day else ""
    today_date = selected_date if day else datetime.datetime.now()
    crumbname = selected_date.strftime(
        '%d-%m-%y') if day else month_name + "-" + str(year)
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    teams = mongo.db.team.find()
    month_start = input_date if day else datetime.datetime(
        year, input_month, 1, 0, 0, 0)
    month_end = input_date if day else datetime.datetime(
        year, input_month, last_day, 0, 0, 0)
    dates = mongo.db.userslist.find()
    teams_lenght = mongo.db.team.count_documents({})

    return render_template(
        'leaveRequestTable.html',
        userslist=dates,
        teams=teams,
        calendar=True,
        days=days,
        crumbname=crumbname,
        dayNames=dayNames,
        year=year,
        month=month,
        input_month=input_month,
        month_start=month_start,
        month_end=month_end,
        month_name=month_name,
        selected_date=selected_date,
        today=today_date,
        requests=requests,
        bin=False,
        teams_count=teams_lenght
    )


@app.route('/leave_request/<team_id>')
@app.route('/leave_request/<team_id>/<user_email>')
def leave_request(team_id="", user_email=""):
    """ route to form to submit a leave request"""
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    all_teams = mongo.db.team.find()
    teams_lenght = mongo.db.team.count_documents({})
    if teams_lenght < 1:
        return render_template('error.html',
                               error=helper.error,
                               requests=helper.mock_requests,
                               crumbname="New Leave Request")
    if team_id:
        team = mongo.db.team.find({'_id': ObjectId(team_id)})
        return render_template('leaveRequest.html',
                               user=user_email,
                               teams=all_teams,
                               selected_team=team,
                               requests=requests,
                               crumbname="New Leave Request",
                               teams_count=teams_lenght)


@app.route('/insert_leave_request', methods=['POST'])
def insert_leave_request():
    """ form to submit leave requests - crud create """
    req = request.form.to_dict()
    _leaveId = ObjectId()
    if not req:
        return render_template('error.html',
                               error=helper.error,
                               requests=helper.mock_requests)
    
    date_from = datetime.datetime.strptime(req['from'], "%d-%m-%Y")
    date_to = datetime.datetime.strptime(req['to'], "%d-%m-%Y")
    user_team_data = mongo.db.team.find_one(
        {'users': {'$elemMatch': {'userId': ObjectId(req['user_id'])}}})    
    user_data = []
    for user in user_team_data['users']:
        if str(user['userId']) == str(req['user_id']):
            user_data = user      
    mongo.db.userslist.update(
        {'_id': ObjectId(user_data['userId'])},
        {'$set': {
            'email': user_data['email'].lower(),
            'name': user_data['name'].lower(),
            'surname': user_data['surname'].lower(),
            'role': user_data['role'].lower(),
            'team': user_team_data["name"].lower()},
            '$push': {
            'leave_request':
                {'reason': req['reason'].lower(),
                    'from': date_from,
                    'to': date_to,
                    'approved': False,
                    'rejected': False,
                    'deleted': False,
                    'comments': req['comments'],
                    '_leaveId': ObjectId(_leaveId)}
        }
        }, upsert=True)
    return redirect(url_for('dashboard'))



@app.route('/teams', methods=["GET", "POST"])
def teams():
    """teams view and filter by team name via 'controller select team'"""
    req = request.form.to_dict()
    team = req["team"] if req else ""
    filtered = True if team else False
    teams = mongo.db.team.find()
    selected_team = mongo.db.team.find_one(
        {'_id': ObjectId(team)}) if team else ""
    crumbname = selected_team["name"] if team else "All Teams"
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    teams_lenght = mongo.db.team.count_documents({})
    if teams_lenght < 1:
        message = "No 'Teams' data retrieved"
        error = "no teams"
        return render_template('error.html',
                               error=error,
                               requests=helper.mock_requests,
                               show_teams=True,
                               message=message,
                               crumbname=crumbname)
    return render_template('teams.html',
                           teams=teams,
                           requests=requests,
                           show_teams=True,
                           crumbname=crumbname,
                           filtered=filtered,
                           selected_team=selected_team,
                           teams_count=teams_lenght)


@app.route('/teams/add_team')
def add_new_team():
    """renders add new team"""
    teams = mongo.db.team.find()
    teams_lenght = mongo.db.team.count_documents({})
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('addNewTeam.html',
                           teams=teams,
                           requests=requests,
                           show_teams=True,
                           crumbname="Add New Team",
                           teams_count=teams_lenght)


@app.route('/teams/insert_team', methods=["POST"])
def insert_team():
    """insert team (add team) - crud create """
    req = request.form.to_dict()
    if not req:
        return render_template('error.html',
                               error=helper.error,
                               requests=helper.mock_requests,
                               show_teams=True,
                               crumbname="Add New Team")
    users = helper.get_users_by_req(req)

    mongo.db.team.insert_one({'name': req['team_name'], 'users': users})
    return redirect(url_for('teams'))


@app.route('/teams/edit_team', methods=["POST"])
def edit_team():
    """renders edit team"""
    team_id = request.form.get('team')
    all_teams = mongo.db.team.find()
    team = mongo.db.team.find_one({'_id': ObjectId(team_id)})
    userslist = mongo.db.userslist.find()
    teams_lenght = mongo.db.team.count_documents({})
    if teams_lenght < 1 or not team_id or not team:
        return render_template('error.html',
                               error=helper.error,
                               requests=helper.mock_requests,
                               teams=all_teams,
                               crumbname="Edit Team")
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    return render_template('editTeam.html',
                           team=team,
                           teams=all_teams,
                           userslist=userslist,
                           requests=requests,
                           show_teams=True,
                           crumbname='Edit "' + team["name"] + '" Team',
                           teams_count=teams_lenght)


@app.route('/teams/update_team/', methods=["POST"])
def update_team():
    """update team via edit team - crud update"""
    req = request.form.to_dict()
    team_id = req.get("team-entry-id")
    team_name = req.get("team-name")
    if not req or not team_id or not team_name:
        return render_template('error.html',
                               error=helper.error,
                               requests=helper.mock_requests,
                               crumbname="Edit Team")

    users = helper.get_users_by_req(req)

    mongo.db.team.update_one({'_id': ObjectId(team_id)},
                             {'$set':
                              {'name': team_name, 'users': users}
                              })
    return redirect(url_for('teams'))


@app.route('/teams/delete_entry/<scope>', methods=["GET", "POST"])
def delete_entry(scope):
    """delete team via edit team based on scope: user or team
        // crud update and remove"""
    if request.method == 'POST':
        try:
            _bin = mongo.db.bin.find_one()
            _bin_id = _bin["_id"]
            email = request.form.get('user_email')
            entry_id = request.form.get('entry_id')
        except:
            return render_template('error.html',
                                   error=helper.error,
                                   requests=helper.mock_requests,
                                   show_teams=True,
                                   crumbname="Edit Team")
        if not entry_id or not _bin_id:
            return render_template('error.html',
                                   error=helper.error,
                                   requests=helper.mock_requests,
                                   show_teams=True,
                                   crumbname="Edit Team")
        else:
            deleted_time = datetime.datetime.now()
            if scope == "team":
                selected_item = mongo.db.team.find_one(
                    {'_id': ObjectId(entry_id)})
                edited_selected_item = selected_item.copy()
                edited_selected_item["deleted_time"] = deleted_time
                mongo.db.bin.update_one({'_id': ObjectId(_bin_id)},
                                        {'$push':
                                         {'teams': edited_selected_item}
                                         }, True)
                mongo.db.team.remove({'_id': ObjectId(entry_id)})
                items_in_userslist = mongo.db.userslist.find(
                    {'team': selected_item["name"]})
                if items_in_userslist:
                    for user in items_in_userslist:
                        if user['team'] == selected_item['name']:
                            item_id = user['_id']
                            mongo.db.userslist.remove(
                                {'_id': ObjectId(item_id)})
                return redirect(url_for('teams'))
            elif scope == "user":
                user_team = mongo.db.team.find_one({'_id': ObjectId(entry_id)})
                for user in user_team["users"]:
                    if user["email"] == email.lower():
                        edited_user = user.copy()
                        edited_user["deleted_time"] = deleted_time
                        mongo.db.bin.update_one(
                            {'_id': ObjectId(_bin_id)},
                            {'$push':
                                {'users': {
                                    "user": edited_user,
                                    '_teamId': ObjectId(entry_id),
                                    'team_name': user_team["name"]
                                }}})
                        mongo.db.team.update_one(
                            {'_id': ObjectId(entry_id)},
                            {'$pull':
                                {'users': user}})
                        mongo.db.userslist.remove({'email': email.lower()})
                return redirect(url_for('teams'))


@app.route('/bin/<data_requested>')
def get_bin(data_requested):
    """renders bin filtering deleted data from
    'bin' in DB by data requested: team_members or teams"""
    deleted_items = mongo.db.bin.find()
    requests = helper.get_items_number_by_status(mongo.db.userslist)
    teams = mongo.db.team.find()
    teams_lenght = mongo.db.team.count_documents({})
    bin_length = mongo.db.bin.count_documents({})
    if bin_length < 1:
        message = 'no item in the bin!'
        error = 'nothing has been moved here yet,'
        crumbname = 'Bin / Users' if data_requested == 'team_members' else 'Bin / Teams'
        return render_template('error.html',
                               error=error,
                               requests=helper.mock_requests,
                               message=message,
                               bin=True,
                               crumbname=crumbname)
    else:
        team_members = []
        deleted_teams = []
        if data_requested == "team_members":
            for deleted in deleted_items:
                try:
                    deleted["teams"]
                except:
                    try:
                        deleted["users"]
                    except:
                        message = 'no user in the bin!'
                        error = 'nothing has been moved here yet,'
                        return render_template('error.html',
                                               error=error,
                                               requests=helper.mock_requests,
                                               crumbname="Bin / Users",
                                               message=message,
                                               bin=True)
                if 'users' in deleted:
                    for user in deleted["users"]:
                        team_members.append(user)
                if 'teams' in deleted:
                    for team in deleted["teams"]:
                        if 'users' in team:
                            for team_user in team["users"]:
                                edited_user = team_user
                                edited_user["deleted_time"] = team["deleted_time"]
                                new_user_dict = {
                                    'user': edited_user,
                                    'team_name': team["name"],
                                    '_teamId': team["_id"],
                                    'team_deleted': True
                                }
                                team_members.append(new_user_dict)
            keys = ["email", "role", "approver", "team", "reason", "date"]
            return render_template('bin.html',
                                   items=team_members,
                                   teams=teams,
                                   bin=True,
                                   crumbname="Bin / Users",
                                   requests=requests,
                                   data="users",
                                   keys=keys,
                                   teams_count=teams_lenght)
        elif data_requested == "teams" and deleted_items:
            for deleted in deleted_items:
                try:
                    deleted["teams"]
                except:
                    message = 'no teams in the bin!'
                    error = 'nothing has been moved here yet,'
                    return render_template('error.html',
                                           error=error,
                                           requests=helper.mock_requests,
                                           crumbname="Bin / Teams",
                                           message=message,
                                           bin=True)
                for team in deleted["teams"]:
                    deleted_teams.append(team)
            keys = ["team name", "users", "date"]
            return render_template('bin.html',
                                   items=deleted_teams,
                                   teams=teams,
                                   bin=True,
                                   crumbname="Bin / Teams",
                                   requests=requests,
                                   data="teams",
                                   keys=keys,
                                   teams_count=teams_lenght)


@app.route('/bin/deleted')
def clean_bin():
    """permanently deletes entries - crud delete"""
    mongo.db.bin.remove()
    mongo.db.bin.insert({'_id': ObjectId()})
    return redirect(url_for('get_bin', data_requested="teams"))


@app.route('/developying')
def developying():
    """renders developying page for features not yet developed"""
    return render_template('developying.html',
                           requests=helper.mock_requests)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=False)
