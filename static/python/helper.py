# mock used in error.html in which there is no need to retrieve the actual data
mock_requests={
    "approved":0,
    "rejected":0,
    "to_be_approved":0,
    "all_requests":0
    }
# default error for error.html
error="Something is wrong. Contact your Administrator </br> Error: <strong class='text-danger'>Wrong Collection Name or missing data</strong></br>"

# function to get the number of requests and fill badges in dashboard controller
def get_items_number_by_status(collection):
    results={}
    all_results=0
    approved=0
    rejected=0
    to_be_approved=0
    for item in collection.find():
        if item["leave_request"]:
          for request in item["leave_request"]:
            if request["deleted"]== False:
                all_results=all_results+1
                if request["approved"] == True:
                    approved=approved+1
                elif request["rejected"] == True:
                    rejected=rejected+1
                elif request["approved"]==False and request["rejected"]==False:
                    to_be_approved=to_be_approved+1
    results={
        "approved":approved,
        "rejected":rejected,
        "to_be_approved":to_be_approved,
        "all_requests":all_results
    }
    return results 

            