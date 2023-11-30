from datetime import datetime, timedelta

def path_csv(date, file_path):
    return f"{file_path}{str(date).split(' ')[0]}.csv"

def get_timestamp(date_str):
    date, hour = date_str.split('T')
    date_list = map(int, date.split('-'))
    hour_list = map(int, hour.split('.')[0].split(':'))

    return datetime(*date_list, *hour_list).timestamp()

def get_dates_in_intervals(start_date, end_date, interval_minutes=5):
    current_date = start_date
    date_list = []

    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(minutes=interval_minutes)

    return date_list

def to_tmsp(date):
    return int(date.timestamp() * 1000)

def dates_to_tmsps(start_date, end_date):
    dates_int5 = get_dates_in_intervals(start_date, end_date)

    tmsps = []
    for i in range(len(dates_int5)):
        if i == len(dates_int5)-1: break
        tmsps.append((to_tmsp(dates_int5[i]), to_tmsp(dates_int5[i+1])))

    return tmsps