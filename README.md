# Leave Request Manager

Leave Request Manager is the answer to a specific need: To keep track of all requests made by employees and be able to approve or reject them.

Leave request manager comes with a Dashboard which you can filter by month or clicking on a specific day and thanks to our awesome menu 

You will be able to filter by All your requests, the ones awaiting for approval already approved or even rejected for a better visual experience. 

With a "team" structure where to add new members and "new leave request" area that allows to open requests on behalf of your team.

Finally a "bin" section allows to transfer items rather than deleting them creating a repository, hence you do not lose your team data!


## UX
 
UX is focused on helping supervisors handling their team's leave requests. 

As a supervisor, I want to know which requests have been logged this month via a dashboard.   
As a supervisor, I want to change how the dashboard data is filtered.   
As a supervisor, I want to see all requests in effect in a specific day.   
As a supervisor, I want to see all requests (not filtered).   
As a supervisor, I want to see all not approved requests.   
As a supervisor, I want to see all approved requests.   
As a supervisor, I want to see all rejected requests.   
As a supervisor, I want to be able to review existing teams.   
As a supervisor, I want to be able to add new teams.   
As a supervisor, I want to be able to edit existing teams. adding new members or deleting users or the team itself   
As a supervisor, I want to be able to add a request on behalf of others.   
As a supervisor, I want to be able to approve, reject or cancel requests.   
As a supervisor, I want an overview of what has been deleted ("bin").    
As a supervisor, I want to be able to permanently delete what was moved to the "bin".   

Leave manager request mock can be found in local folder `project-mocks`
Database diagram can be found in local folder [database-schema]()

## Features

1) side navigation bar for easy navigation to major pages in the web app
    -including "Leave request" area "Teams" area "Bin" area and a section to add a leave request.
2) every page "includes" a "controller", navigation bar devided in cards. each card will filter the section accordingly to its name: 
    -in "leave request" section the card "all request" loads the page with all requests.
    -in Teams add new team will load a page showing a Form to create a new team 
3) All Requests, approved requests, to be approved and rejected will show a data table including a cell with an info icon.            clicking the info icon Users will be able to see extra info such as resquestor comments and three buttons, such as Cancel,         Reject, Approve. User can approve or reject from here

4) To cancel a leave request means to change its boolean (deleted) to true. the request itself will be automatically filtered by       every page  
5) to delete an user or a team means to transfer its data to the Bin section. 
6) Add or Edit team have a description part and a limit quota of 30 users max 
7) All "teams" sections have a data table with a book icon as last cell, clicking this last cell will allow user to book a leave       request on behalf of the selected user row.
8) an error page exists in case most common errors are detected, for a good UX experience
9) a under developying page exists for features not yet finished and under developying
 
### Existing Features

- Feature 1: Dashboard - 
    > refer to `Dashboard.html`, `app.py`

             Allows users to have an overview of all requests related to current month, is including a calendar.
- Feature 2: Calendar- 
    > refer to `calendarview.html`, `myCalendar.py`, `app.py`;

             Allows users to review requests logged for a specific month-year or if selected day-month-year  
- Feature 3: Navigation bar "Leave requests"-   
    > refer to `controller.html`, `app.py`;

            Allows users to easy filter the data depending on approval status: "All Requests", "To be Approved", "Approved", "Rejected"  
- Feature 4: Navigation bar "Manage Teams"-   
    > refer to `controller.html`, `app.py`;

            Allows users to easily select options related to Team management: "All Teams", "Select team","add new team", "Edit Teams"
- Feature 5: Navigation bar "Bin":
    > refer to `controller.html`, `app.py`;

             Allows users to review deleted Teams or Users.    
- Feature 6: Side navigation bar: 
    > refer to `base.html`;      

             Allows users to reach all the most important features faster by clicking the related Icon/name. 
- Feature 7: Side navigation bar "Add new leave request"- 
    > refer to `leaveRequest.html`;

             Allows users to add a request on behalf of a user belonging to the selected team  
- Feature 8: "leave requests" Data Table - 
    > refer to `leaveRequestTable.html`,`app.py`;

             Allows users to review requests' comments and approve/reject or cancel the request by clicking on info icon
             This functionality is available for all type of requests but allows for approvals only if requests have not been
             approved/rejected/deleted yet otherwise allows for comments and request's status review. 
- Feature 9: "Teams" Data Table - 
    > refer to `teams`,`app.py`;

             Allows users to review Teams' structure and add a leave requst on behalf of the related user in that team via the
             "book" icon
- Feature 10: Clean the "bin": 
    > refer to `bin.html`,`app.py`;

              Allows users to permanently delete a user and its requests or a whole team and their requests from
              the bin
- Feature 11: Breadcrumb: 

    > refer to `breadcrumb.html`, `app.py`;

              Allows users to easily go back to previous page and keep track of where they are
- Feature 12: error page:
    > refer to `error.html`, `app.py`;

             Allows users to catch most common errors or alerts with a friendly UI
- Feature 13: In developying page:
    > refer to `developying.html`, `app.py`;

            Allows user to get an alert message if the page they are surfing is in developying/ not yet deployed

### Features Left to Implement
- Feature 14: Recover deleted entries:
    > refer to `controller.html`, `app.py`

            In the bin section users will be allowed to recover what previously deleted
- Feature 15: Recover cancelled leave requests:
    > refer to `leaveRequestTable.html`, `app.py`

            Option to recover or modify cancelled requests and consequently new approval flow
- Feature 16: Not supervisor app filter:
    
            Using OS app will recognize user and filter pages accordingly
            If users are not supervisors will be allowed to "leave requests" section and to add a new leave request only   

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.

- [Bootstrap 4](https://getbootstrap.com/docs/4.4/getting-started/introduction/)
    - The project uses **Bootstrap 4** and a modified **Bootstrap template** to simplify its cascade stylesheet
    - refer to template's `README.MD` for further information, its `LICENSE` is also included 

- [Atlas Mongo DB](https://www.mongodb.com/cloud/atlas)
    - to serve as Database Host 

- [Python 3](https://www.python.org/download/releases/3.0/)
    - with [pymongo](https://api.mongodb.com/python/current/) to serve as back-end and connect with [Mongo DB](https://www.mongodb.com/) and perfor data manipulation on database query results.

## Testing

1. dashboard (landing page):
    1. click on calendar to select next or previous month and verify no error has thrown even without data from DB  
    2. click on calendar date, verify table is filtered to show results only for specific date selected no error if no data from db
    3. click on header badge(bell) shows number of "to be approved requests" even if no data from db 
    4. click on "check request waiting for approval" in badge(bell) dropdown redirect to new requests - to error.html if no data      from db
    5. all links in navs and sidebar redirect to their sections correctly
    6. in particular sidebar "add a request" link allows to select user and redirects to "leave request from" and filters data by     user selected with no errors. if no user has been added link won't be shown in sidebar
    7. data table in dashboard shows no data if no data from db. if data click on info icon to show leave request info correctly
    8. click on info's buttons to approve reject or cancel leave requests expected to redirect to correct sections and change         approval status in DB: no errors
    9. controllers badges show correct number of requests by type

2. "All requests" section:
    1. click on "All request" "view details" redirects to its section if data from DB or error.html page with custom information 
    2. Data table expected to show data from DB not filtered. no errors
3. "new requests" section: 
    1. click on "new requests" "view details" redirects to its section if data from DB or error.html page with custom information
    2. Data table expected to show data from DB filtered by not "rejected" not "approved" and not "deleted". no errors
4. "approved requests" section: 
    1. click on "approved requests" "view details" redirects to its section if data from DB or error.html page with custom            information
    2. Data table expected to show data from DB filtered by "approved" requests from db. no errors
5. "rejected requests" section: 
    1. click on "rejected requests" "view details" redirects to its section if data from DB or error.html page with custom            information
    2. Data table expected to show data from DB filtered by "rejected" requests from db. no errors

6. "All teams" section:
    1. click on "All teams" "view details" redirects to its section if data from DB or error.html page with custom information 
    2. Data table expected to show data from DB not filtered. no errors
7. "selected team" section: 
    1. click on "selected team" "view details" opens a modal correctly with list of teams if no data from DB shows alert correctly
    2. click on team from modal filters data in teams data table
    3. Data table expected to show data from DB filtered by team selected. no errors
8. "add a new team" section: 
    1. click on "add new team" "view details" redirects to its section
    2. try to submit an empty or partially empty form and verify that an error message about the next required field appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that successfuly redirects to "teams" page to show data added.
9. "edit team" section:
    1. click on "edit team" "view details" opens a modal correctly with list of teams if no data from DB shows alert correctly 
    2. click on team from modal redirects to form to edit team
    3. try to submit an empty or partially empty form and verify that an error message about the next required field appears
    4. Try to submit the form with an invalid email address and verify that a relevant error message appears
    5. Try to submit the form with all inputs valid and verify that successfuly redirects to "teams" page to show data edited
10. "bin" section:
    1. Go to "Bin" section
    2. Verify "Bin" shows "Deleted users""View Details" by default and with no data shows custom error.html correctly
    3. click on "Deleted Teams""View Details" and verify it shows bin filtered by deleted teams or custom error.html correctly if     no data in db
    4. click on "Empty bin""View Details" and verify modal with warning is rendered
    5. click on "Confirm" in "Empty bin" modal and verify custom error.html is rendered correctly
    6. click on "Recover Deleted Entries" and verify developing.html is rendered correctly

Leave request manager is a responsive app, but under 1032px width user will need to scroll right/left to see all tables content  
Same behaviour on Edge and Chrome, on IE it is visible a flickering when changing template, routing to another template  

IE calendar grid not supported, it could be fixed by adding a class for every day displayed that holds day placement in the grid  
as autoplacement is not yet working in IE
In IE footer does not behave correctly as well as delete teams in edit team and bin section, to be addressed 
Added an alert in case user loads app from IE

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.
Deployment in github:
1. Created new repository in [github](https://github.com/)
2. In VS Code set Master branch with 'git init' command
3. added initial content with 'git init'
4. git commit -m 'initial commit' to commit initial push
5. git remote add origin example.com:my_project.git
6. git push -u origin master
7. going forward created .gitignore to ignore env.py file (MONGO URI containing password)

Deployment on Heroku:
1. Created new app in [Heroku](https://dashboard.heroku.com/apps)
2. downloaded Heroku cli
3. launched Heroku login
4. removed env.py file
5. command git add . to stage changes 
6. command git commit -m "initial commit" to commit changes 
7. git push heroku master
8. click on created app and go to "Settings"
9. Set "Config Vars": IP, MONGO_URI, PORT. Mongo uri so can avoid to share secret key
10. write concern 'w=majority' was trowing errors in Heroku only, write concern 'w=1' fixed it.

to run the app locally:
1. be sure env.py is in 'static/python' folder
2. run app.py from terminal / vscode 'run' icon 

## Credits
Thanks to [CSS tricks](https://css-tricks.com/) as always very nice website when stuck on a CSS issue   
    especially for the tips on how to use [CSS grids](https://css-tricks.com/snippets/css/complete-guide-grid/)
Thanks to [StackOverflow](https://stackoverflow.com/questions/21825157/internet-explorer-11-detection) and in particular to             'EpokK' and his Post on how to detect IE with JQuery
Thanks to [free icons library](https://icon-library.net/) where i found the image used for the favicon 
    image native name: Booking Icon Png #311896; image can be found in images forlder: favicon-32x32.png  

