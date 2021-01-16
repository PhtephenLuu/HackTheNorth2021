import requests
import dash
import pandas 

def reqProv(prov = "ON"):
    URL = f"https://api.opencovid.ca/summary?loc={prov}"
    response = requests.request("GET", URL)
    print(response.text)


def main():
    reqProv()

if __name__ == "__main__":
    main()