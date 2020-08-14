from datetime import date

def get_current_monthday():
    today = date.today()
    string_date = str(today)
    formatted_date = string_date.replace("-", "")
    month_day = formatted_date[4:]
    string = "_"
    #string.append(month_day)
    string += month_day
    return string
