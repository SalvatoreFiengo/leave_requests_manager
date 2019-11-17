import datetime
import calendar

myCal=calendar.TextCalendar()


def get_calendar_by_year_month(year,month):
    days=[]
    for day in myCal.itermonthdates(year,month):
       days.append(day)
    return days
def last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]   
def get_month_long_name(month):
    return calendar.month_name[month]

