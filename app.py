import requests
import json
import dash
import pandas 

def reqProv(prov = "ON"):
    URL = f"https://api.opencovid.ca/summary?loc={prov}"
    response = requests.request("GET", URL)
    data = json.loads(response.text)
    print(response.text)
    print(data["summary"])

def reqTimeSeries(prov = "ON"):
    pass

def main():
    reqProv()

if __name__ == "__main__":
    main()