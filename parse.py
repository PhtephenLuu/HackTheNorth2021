from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import requests

def prompt():
    result = {}
    # options are ["AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"]
    province = input("Enter province code: ")
    result['province'] = province

    # options are Weekly, Monthly, Yearly
    time_view = input("Enter time series view: ")
    result['time_view'] = time_view

    # options are [cases, mortality]
    stats = input("Enter to view cases/deaths: ")
    result['stats'] = stats
    return result


def get_weekly():
    dates = {}
    today = datetime.now()
    yesterday = datetime.now() - relativedelta(weeks=1)
    dates['today'] = today.strftime('%d-%m-%Y')
    dates['yesterday'] = yesterday.strftime('%d-%m-%Y')
    return dates

def get_monthly():
    dates = {}
    today = datetime.now()
    last_month = datetime.now() - relativedelta(months=1)
    dates['today'] = today.strftime('%d-%m-%Y')
    dates['yesterday'] = last_month.strftime('%d-%m-%Y')
    return dates

def get_yearly():
    dates = {}
    today = datetime.now()
    yesterday = datetime.now() - relativedelta(years=1)
    dates['today'] = today.strftime('%d-%m-%Y')
    dates['yesterday'] = yesterday.strftime('%d-%m-%Y')
    return dates

def calculate_date(user_choice):
    if user_choice.lower() == "weekly":
        date = get_weekly()
    elif user_choice.lower() == "monthly":
        date = get_monthly()
    elif user_choice.lower() == "yearly":
        date = get_yearly()
    else:
        raise Exception
    return date

def get_request(province, dates, stats):
    #dates = calculate_date()
    print(dates)
    first_date = dates['yesterday']
    second_date = dates['today']
    URL = f"https://api.opencovid.ca/timeseries?stat={stats}&loc={province}&before={second_date}&after={first_date}"
    # DD - MM - YYYY
    response = requests.request("GET", URL)
    json_data = json.loads(response.text)

    with open(f"sample_outputs/{province}_{first_date}to{second_date}_{stats}.json", "w") as f:
        json.dump(json_data, f, indent=4)
    return json_data


def main():
    result = prompt()
    province = result['province'] # ex: ON
    time_view = result['time_view'] # ex: Weekly
    stats = result['stats'] # ex: cases

    dates = calculate_date(time_view) # returns dictionary with today/yesterday as keys

    results = get_request(province, dates, stats)
    print(results)
    try:
        print(results["Summary"])
        print("Success")
    except:
        print("ERROR!")
    
if __name__ == '__main__':
    main()