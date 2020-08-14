from datetime import date

today = date.today()
string_date = str(today)
formatted_date = string_date.replace("-", "")
month_day = formatted_date[4:]
#print("Today's date:", formatted_date)
print(month_day)