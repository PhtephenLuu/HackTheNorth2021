import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from parse import get_request, get_cases_from_data
import plotly.express as px
import pandas as pd

app = dash.Dash()

json_data = get_request("ON", {'today': '16-01-2021', 'yesterday': '01-07-2020'}, "cases")
df = get_cases_from_data(json_data)

fig = px.line(df, x="date", y="cases")

app.layout = html.Div([
    dcc.Dropdown(
        id='province-dropdown',
        options=[
            {'label': 'Alberta', 'value': 'AB'},
            {'label': 'British Columbia', 'value': 'BC'},
            {'label': 'Manitoba', 'value': 'MB'},
            {'label': 'New Brunswick', 'value': 'NB'},
            {'label': 'Northwest Territories', 'value': 'NT'},
            {'label': 'Nova Scotia', 'value': 'NS'},
            {'label': 'Newfoundland and Labrador', 'value': 'NL'},
            {'label': 'Nunavut', 'value': 'NU'},
            {'label': 'Ontario', 'value': 'ON'},
            {'label': 'Prince Edward Island', 'value': 'PE'},
            {'label': 'Quebec City', 'value': 'QC'},
            {'label': 'Saskatchewan', 'value': 'SK'},
            {'label': 'Yukon', 'value': 'YT'}
        ],
        placeholder="Select a province:",
    ),
    dcc.Dropdown(
        id='time-dropdown',
        options=[
            {'label': 'Weekly', 'value': 'weekly'},
            {'label': 'Monthly', 'value': 'monthly'},
            {'label': 'Yearly', 'value': 'yearly'}
        ],
        placeholder="Select a timeframe:",
    ),dcc.Dropdown(
        id='stats-dropdown',
        options=[
            {'label': 'Cases', 'value': 'cases'},
            {'label': 'Deaths', 'value': 'mortality'}
        ],
        placeholder="Select a statistic:",
    ),
    html.Div(id='dd-province-output-container'),
    html.Div(id='dd-time-output-container'),
    html.Div(id='dd-stats-output-container'),
    dcc.Graph(
                id='mapbox',
                figure=fig
        )
])

@app.callback(
    Output('dd-province-output-container', 'children'),
    [Input('province-dropdown', 'value')])
def update_province_output(value):
    return f"Province selected: {value}"

@app.callback(
    Output('dd-time-output-container', 'children'),
    [Input('time-dropdown', 'value')])
def update_time_output(value):
    return f"Timeframe selected: {value}"

@app.callback(
    Output('dd-stats-output-container', 'children'),
    [Input('stats-dropdown', 'value')])
def update_stats_output(value):
    return f"Statistic selected: {value}"


if __name__ == "__main__":
    app.run_server(debug=True)
