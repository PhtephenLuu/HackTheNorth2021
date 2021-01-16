from datetime import datetime, timedelta
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
    today = datetime.now()
    yesterday = datetime.now() - timedelta(7)
    return (today.strftime('%d-%m-%Y'), yesterday.strftime('%d-%m-%Y'))

def get_monthly():
    today = datetime.now()
    yesterday = datetime.now() - timedelta(30)
    return (today.strftime('%d-%m-%Y'), yesterday.strftime('%d-%m-%Y'))

def get_yearly():
    today = datetime.now()
    yesterday = datetime.now() - timedelta(365)
    return (today.strftime('%d-%m-%Y'), yesterday.strftime('%d-%m-%Y'))

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
    URL = f"https://api.opencovid.ca/timeseries?stat={stats}&loc={province}&before={dates[0]}&after={dates[1]}"
    # DD - MM - YYYY
    response = requests.request("GET", URL)
    json_data = json.loads(response.text)

    n = 4
    with open(f"sample_outputs/output{n}_{province}_{dates[0]}to{dates[1]}_{stats}.json", "w") as f:
        json.dump(json_data, f, indent=4)
    return json_data


def main():
    result = prompt()
    province = result['province'] # ex: ON
    time_view = result['time_view'] # ex: Weekly
    stats = result['stats'] # ex: cases

    dates = calculate_date(time_view)

    get_request(province, dates, stats)
    print("Success")

if __name__ == '__main__':
    main()