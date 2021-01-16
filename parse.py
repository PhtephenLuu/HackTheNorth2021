from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd



def prompt():
    result = {}
    # options are ["AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"]
    province = input("Enter province code: ")
    result['province'] = province

    # options are Weekly, Monthly, Yearly
    time_view = input("Enter time series view: ").lower()
    result['time_view'] = time_view

    # options are [cases, mortality, recovered, testing, active]
    stats = input("Enter statistic to view: ").lower()
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
    yesterday = datetime.now() - relativedelta(months=1)
    dates['today'] = today.strftime('%d-%m-%Y')
    dates['yesterday'] = yesterday.strftime('%d-%m-%Y')
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

def get_request(province="MB", dates=get_weekly(), stats="cases"):
    first_date = dates['yesterday']
    second_date = dates['today']
    URL = f"https://api.opencovid.ca/timeseries?stat={stats}&loc={province}&before={second_date}&after={first_date}"
    # DD - MM - YYYY
    response = requests.request("GET", URL)
    json_data = json.loads(response.text)
    return json_data

def get_all_info(province="MB", dates=get_weekly()):
    '''returns dataframe with ALL info'''
    cases_info = get_request(province, dates, "cases")
    deaths_info = get_request(province, dates, "mortality")
    recovered_info = get_request(province, dates, "recovered")
    testing_info = get_request(province, dates, "testing")
    active_info = get_request(province, dates, "active")
    
    result = {}
    result['date'] = []
    result['topic'] = []
    result['count'] = []

    # starting iterating through dictionaries
    cases_inner = cases_info.get("cases")
    for each in cases_inner:
        current_date = each['date_report']
        current_cases = each['cases']
        result['date'].append(current_date)
        result['topic'].append('cases')
        result['count'].append(current_cases)

    deaths_inner = deaths_info.get("mortality")
    for each in deaths_inner:
        current_date = each['date_death_report']
        current_deaths = each['deaths']
        result['date'].append(current_date)
        result['topic'].append('deaths')
        result['count'].append(current_deaths)

    recovered_inner = recovered_info.get("recovered")
    for each in recovered_inner:
        current_date = each['date_recovered']
        current_deaths = each['recovered']
        result['date'].append(current_date)
        result['topic'].append('recovered')
        result['count'].append(current_deaths)

    testing_inner = testing_info.get("testing")
    for each in testing_inner:
        current_date = each['date_testing']
        current_deaths = each['testing']
        result['date'].append(current_date)
        result['topic'].append('testing')
        result['count'].append(current_deaths)

    active_inner = active_info.get("active")
    for each in active_inner:
        current_date = each['date_active']
        current_deaths = each['active_cases']
        result['date'].append(current_date)
        result['topic'].append('active_cases')
        result['count'].append(current_deaths)     
    
    return result

# {date:[1,2,3], cases=[30,40,50]}

# {date=[1,2,3], topics=["cases", "cases", mortality, recovered, testing, active", ..., "active", ""], count=[30,40, 100]}


def get_cases_from_data(json_data):
    '''ONLY CAN BE USED IF STATS = "cases" '''
    result = {}
    inner = json_data.get("cases")
    for each in inner:
        current_date = each['date_report']
        current_cases = each['cases']
        current_cuml_cases = each['cumulative_cases']
        if 'date' not in result:
            result['date'] = [current_date]
        else:
            result['date'].append(current_date)
        if 'cases' not in result:
            result['cases'] = [current_cases]
        else:
            result['cases'].append(current_cases)
    return result

def get_cumul_cases_from_data(json_data):
    '''ONLY CAN BE USED IF STATS = "cases" '''
    result = {}
    inner = json_data.get("cumulative_cases")
    for each in inner:
        current_date = each['date_report']
        current_cases = each['cumulative_cases']
        if 'date' not in result:
            result['date'] = [current_date]
        else:
            result['date'].append(current_date)
        if 'cumulative_cases' not in result:
            result['cumulative_cases'] = [current_cases]
        else:
            result['cumulative_cases'].append(current_cases)
    return result

def get_deaths_from_data(json_data):
    '''ONLY CAN BE USED IF STATS = "mortality" '''
    result = {}
    inner = json_data.get("mortality")
    for each in inner:
        current_date = each['date_death_report']
        current_cases = each['deaths']
        if 'date_death_report' not in result:
            result['date_death_report'] = [current_date]
        else:
            result['date_death_report'].append(current_date)
        if 'deaths' not in result:
            result['deaths'] = [current_cases]
        else:
            result['deaths'].append(current_cases)
    return result
"""
def get_cumul_deaths_from_data(json_data):
    '''ONLY CAN BE USED IF STATS = "mortality" '''
    result = {}
    inner = json_data.get("mortality")
    for each in inner:
        current_date = each['date_death_report']
        current_cases = each['cumulative_deaths']
        if 'date_death_report' not in result:
            result['date_death_report'] = [current_date]
        else:
            result['date_death_report'].append(current_date)
        if 'cumulative_deaths' not in result:
            result['cumulative_deaths'] = [current_cases]
        else:
            result['cumulative_deaths'].append(current_cases)
    return result
"""
def main():
    result = prompt()
    province = result['province'] # ex: ON
    time_view = result['time_view'] # ex: Weekly
    stats = result['stats'] # ex: cases

    dates = calculate_date(time_view) # returns dictionary with today/yesterday as keys

    json_data = get_request(province, dates, stats)
    
    if stats == "cases":
        dict_data = get_cases_from_data(json_data)
        df = pd.DataFrame(dict_data.items(), columns=["date", "cases"])
        print(df)
    elif stats == "mortality":
        dict_data = get_deaths_from_data(json_data)
        df = pd.DataFrame(dict_data.items(), columns=["date", "deaths"])
        print(df)

    print("Success")

if __name__ == '__main__':
    main()