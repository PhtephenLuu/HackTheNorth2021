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
    dates['today'] = today.strftime('%Y-%m-%d')
    dates['yesterday'] = yesterday.strftime('%Y-%m-%d')
    return dates

def get_monthly():
    dates = {}
    today = datetime.now()
    yesterday = datetime.now() - relativedelta(months=1)
    dates['today'] = today.strftime('%Y-%m-%d')
    dates['yesterday'] = yesterday.strftime('%Y-%m-%d')
    return dates

def get_yearly():
    dates = {}
    today = datetime.now()
    yesterday = datetime.now() - relativedelta(years=1)
    dates['today'] = today.strftime('%Y-%m-%d')
    dates['yesterday'] = yesterday.strftime('%Y-%m-%d')
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
    URL = f"https://api.opencovid.ca/timeseries?stat={stats}&loc={province}&before={second_date}&after={first_date}&legacy=true"
    # DD - MM - YYYY
    response = requests.get(URL)
    json_data = json.loads(response.text)
    return json_data

def get_all_info(province="MB", dates=get_weekly(), stats=['cases']):
    '''returns dataframe with ALL info'''
    stat_dict = {}
    for stat in stats:
        stat_dict[stat] = get_request(province, dates, stat).get('data')

    '''
    cases_info = get_request(province, dates, "cases")
    deaths_info = get_request(province, dates, "mortality")
    recovered_info = get_request(province, dates, "recovered")
    testing_info = get_request(province, dates, "testing")
    active_info = get_request(province, dates, "active")
    '''

    result = {}
    result['Date'] = []
    result['Statistic'] = []
    result['Count'] = []

    # starting iterating through dictionaries
    if 'cases' in stat_dict and stat_dict['cases'] is not None:
        cases_inner = stat_dict['cases']['cases']
        print("cases_inner", cases_inner)
        for each in cases_inner:
            print(each)
            current_date = each['date_report']
            current_cases = abs(each['cases'])
            result['Date'].append(current_date)
            result['Statistic'].append('cases')
            result['Count'].append(current_cases)
    else:
        current_date = 'N/A'
        current_cases = 0
        result['Date'].append(current_date)
        result['Statistic'].append('N/A')
        result['Count'].append(current_deaths)


    if 'mortality' in stat_dict and stat_dict['mortality'] is not None:
        print(stat_dict)
        deaths_inner = stat_dict['mortality']
        print(deaths_inner)
        for each in deaths_inner:
            current_date = each['date_death_report']
            current_deaths = abs(each['deaths'])
            result['Date'].append(current_date)
            result['Statistic'].append('deaths')
            result['Count'].append(current_deaths)
    else:
        current_date = 'N/A'
        current_deaths = 0
        result['Date'].append(current_date)
        result['Statistic'].append('N/A')
        result['Count'].append(current_deaths)

    if 'recovered' in stat_dict and stat_dict['recovered'] is not None:
        recovered_inner = stat_dict['data'].get("recovered")
        for each in recovered_inner:
            current_date = each['date_recovered']
            current_recovered = abs(each['recovered'])
            result['Date'].append(current_date)
            result['Statistic'].append('recovered')
            result['Count'].append(current_recovered)
    else:
        current_date = 'N/A'
        current_recovered = 0
        result['Date'].append(current_date)
        result['Statistic'].append('N/A')
        result['Count'].append(current_recovered)

    if 'testing' in stat_dict and stat_dict['testing'] is not None:
        testing_inner = stat_dict['data'].get("testing")
        for each in testing_inner:
            current_date = each['date_testing']
            current_testing = abs(each['testing'])
            if current_testing > 150000: #handles Alberta testing anomaly
                current_testing /= 10
            result['Date'].append(current_date)
            result['Statistic'].append('testing')
            result['Count'].append(current_testing)
    else:
        current_date = 'N/A'
        current_testing = 0
        result['Date'].append(current_date)
        result['Statistic'].append('N/A')
        result['Count'].append(current_deaths)

    if 'active' in stat_dict and stat_dict['active'] is not None:
        active_inner = stat_dict['data'].get("active")
        for each in active_inner:
            current_date = each['date_active']
            current_active = abs(each['active_cases'])
            result['Date'].append(current_date)
            result['Statistic'].append('active_cases')
            result['Count'].append(current_active)     
    else:
        current_date = 'N/A'
        current_active = 0
        result['Date'].append(current_date)
        result['Statistic'].append('N/A')
        result['Count'].append(current_active)
   
    return result


def get_all_cumulative_info(province="MB", dates=get_weekly(), stats=['cases']):
    '''returns dataframe with ALL info'''
    stat_dict = {}
    for stat in stats:
        stat_dict[stat] = get_request(province, dates, stat).get('data')

    # {topic: [cases -> active], 'count: [total_cases -> total_active]}
    # {cases: total_cases, deaths: total_deaths, .....}
    
    result = {}
    result['Statistic'] = stats
    result['Count'] = [0] * len(stats)

    if 'cases' in stat_dict:
        inner_cases = stat_dict['cases']['cases']
        for each in inner_cases:
            result['Count'][stats.index('cases')] += int(each['cases'])
    
    if 'mortality' in stat_dict and stat_dict['mortality'] is not None:
        inner_deaths = stat_dict['data']['mortality']
        for each in inner_deaths:
            result['Count'][stats.index('mortality')] += int(each['deaths'])
    else:
        result['Count'][stats.index('mortality')] = 0

    if 'recovered' in stat_dict and stat_dict['recovered'] is not None:
        inner_recovered = stat_dict['data']['recovered']
        for each in inner_recovered:
            result['Count'][stats.index('recovered')] += int(each['recovered'])
    else:
        result['Count'][stats.index('recovered')] = 0


    if 'testing' in stat_dict and stat_dict['testing'] is not None:
        inner_testing = stat_dict['data']['testing']
        for each in inner_testing:
            result['Count'][stats.index('testing')] += int(each['testing'])
    else:
        result['Count'][stats.index('testing')] = 0

    if 'active' in stat_dict and stat_dict['active'] is not None:
        inner_active = stat_dict['data']['active']
        for each in inner_active:
            result['Count'][stats.index('active')] += int(each['active_cases'])
    else:
        result['Count'][stats.index('active')] = 0

    return result


# {date:[1,2,3], cases=[30,40,50]}

# {date=[1,2,3], topics=["cases", "cases", mortality, recovered, testing, active", ..., "active", ""], count=[30,40, 100]}


def get_cases_from_data(json_data):
    '''ONLY CAN BE USED IF STATS = "cases" '''
    result = {}
    inner = json_data["data"]["cases"]

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
    inner = json_data["data"]["cumulative_cases"]
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
    inner = json_data["data"]["mortality"]
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

def get_prov_name(province):
    prov = {
        "AB": "Alberta",
        "BC": "British Columbia",
        "MB": "Manitoba",
        "NB": "New Brunswick",
        "NL": "Newfoundland and Labrador",
        "NT": "Northwest Territories",
        "NS": "Nova Scotia",
        "NU": "Nunavut",
        "ON": "Ontario",
        "PE": "Prince Edward Island",
        "QC": "Quebec",
        "SK": "Saskatchewan",
        "YT": "Yukon",
    }

    if province in prov:
        return prov[province]
    return

def main():
    #result = prompt()
    province = 'ON'#result['province'] # ex: ON
    time_view = 'weekly' #result['time_view'] # ex: Weekly
    stats = 'cases' #result['stats'] # ex: cases

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