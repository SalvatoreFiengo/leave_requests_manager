import datetime
import calendar

myCal=calendar.TextCalendar()

# returns a calendar given year and month
def get_calendar_by_year_month(year,month):
    days=[]
    for day in myCal.itermonthdates(year,month):
       days.append(day)
    return days

#returns last day of the month given year and month
def last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1] 

#for better readability returns month name (long)
def get_month_long_name(month):
    return calendar.month_name[month]

#function to get the correct response when clicking next previous on calendar feature
def year_month_flow(year,month):
    if month>12:
        month=1
        year=year+1
        return (year,month)
    elif month<1:
        month=12
        year=year-1
        return (year,month)
    else:
        return (year,month)
