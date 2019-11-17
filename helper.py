def get_items_number_by_status(collection):
    results={}
    all_results=0
    approved=0
    rejected=0
    to_be_approved=0
    for item in collection.find():
        if item["leave_request"][-1]["deleted"]== False:
            all_results=all_results+1
            if item["leave_request"][-1]["approved"] == True:
                approved=approved+1
            elif item["leave_request"][-1]["rejected"] == True:
                rejected=rejected+1
            elif item["leave_request"][-1]["approved"]==False and item["leave_request"][-1]["rejected"]==False:
                to_be_approved=to_be_approved+1
    results={
        "approved":approved,
        "rejected":rejected,
        "to_be_approved":to_be_approved,
        "all_requests":all_results
    }
    return results 

            