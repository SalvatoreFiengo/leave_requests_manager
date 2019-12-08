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

Leave manager request mock here-> (local folder)
Database diagram here -> (local folder)

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
- Feature 1 - allows users X to achieve Y, by having them fill out Z
- ...

For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement
- Another feature idea

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.


## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X
