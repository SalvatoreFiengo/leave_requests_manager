import datetime
import calendar

myCal = calendar.TextCalendar()


def get_calendar_by_year_month(year, month):
    """returns a calendar given year and month"""
    days = []
    for day in myCal.itermonthdates(year, month):
        days.append(day)
    return days


def last_day_of_month(year, month):
    """returns last day of the month given year and month"""
    return calendar.monthrange(year, month)[1]


def get_month_long_name(month):
    """for better readability returns month name (long)"""
    return calendar.month_name[month]


def year_month_flow(year, month):
    """function to get the correct response when clicking next previous on calendar feature"""
    if month > 12:
        month = 1
        year = year+1
        return (year, month)
    elif month < 1:
        month = 12
        year = year-1
        return (year, month)
    else:
        return (year, month)
