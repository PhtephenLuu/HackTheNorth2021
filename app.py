import dash
import dash_core_components as dcc
import dash_html_components as html

import json
import requests

app = dash.Dash()

app.layout = html.Div(
    html.H1(children="Hello world")
)

'''
def get_request(province):
    PROVINCES = ["AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"]
    URL = f"https://api.opencovid.ca/summary?loc={province}"
    response = requests.request("GET", URL)
    json_data = json.loads(response.text)
    return json_data

def main():
    print(type(get_request("ON")))

'''
if __name__ == "__main__":
    app.run_server(debug=True)
