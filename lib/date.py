from datetime import *

def get_date():
    today = date.today()
    string_date = str(today)
    return string_date

def get_current_monthday():
    today = date.today()
    string_date = str(today)
    formatted_date = string_date.replace("-", "")
    month_day = formatted_date[4:]
    string = "_"
    string += month_day
    return string
    
def get_yesterday_monthday():
    today = date.today()
    yesterday = today - timedelta(days=1)
    string_date = str(yesterday)
    formatted_date = string_date.replace("-", "")
    month_day = formatted_date[4:]
    string = "_"
    string += month_day
    return string

def get_variable_monthday(*args):
    today = date.today()
    variable = today - timedelta(days=args[0])
    string_date = str(variable)
    formatted_date = string_date.replace("-", "")
    month_day = formatted_date[4:]
    string = "_"
    string += month_day
    return string