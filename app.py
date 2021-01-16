import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from parse import *
import plotly.express as px

app = dash.Dash()

PROVINCE = "ON"
DATES = get_weekly()
STATS = "cases"

json_data = get_request(PROVINCE, DATES, STATS)
df = get_cases_from_data(json_data)

fig = px.line(df, x="date", y="cases")

app.layout = html.Div([
    html.Div([
        html.H2('COVID-19 Data Visualization of Canada'),

    ], className="banner"),

    html.Img(
        src=app.get_asset_url('virus-logo.png'), className="resize",),

    html.Div([
        html.H4('Fill in the boxes below:'),
    ], className="about"),

    dcc.Dropdown(
        id='province-dropdown',
        className='dropdowns',
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
        value="ON"
    ),
    dcc.Dropdown(
        id='time-dropdown',
        className='dropdowns',
        options=[
            {'label': 'Past Week', 'value': 'weekly'},
            {'label': 'Past Month', 'value': 'monthly'},
            {'label': 'Past Year', 'value': 'yearly'}
        ],
        placeholder="Select a timeframe:",
        value="weekly"
    ), dcc.Dropdown(
        id='stats-dropdown',
        className='dropdowns',
        options=[
            {'label': 'Cases', 'value': 'cases'},
            {'label': 'Deaths', 'value': 'mortality'}
        ],
        placeholder="Select a statistic:",
        value="cases"
    ),
    html.Div(id='dd-province-output-container',
             className='info-display'),
    html.Div(id='dd-time-output-container',
             className='info-display'),
    html.Div(id='dd-stats-output-container',
             className='info-display'),
    dcc.Graph(
        id='mapbox',
        figure=fig
    )

])


@ app.callback(
    Output('dd-province-output-container', 'children'),
    [Input('province-dropdown', 'value')])
def update_province_output(value):
    return f"Province selected: {value}"


@ app.callback(
    Output('dd-time-output-container', 'children'),
    [Input('time-dropdown', 'value')])
def update_time_output(value):
    return f"Timeframe selected: {value}"


@ app.callback(
    Output('mapbox', 'figure'),
    Input('province-dropdown', 'value'),
    Input('time-dropdown', 'value'),
    Input('stats-dropdown', 'value')
)
def update_graph(prov_val, time_val, stats_val):
    PROVINCE = prov_val
    DATES = calculate_date(time_val)
    STATS = stats_val
    json_data = get_request(PROVINCE, DATES, STATS)
    if STATS == 'cases':
        df = get_cases_from_data(json_data)
        fig = px.line(df, x="date", y="cases")
    elif STATS == 'mortality':
        df = get_deaths_from_data(json_data)
        fig = px.line(df, x="date_death_report", y="deaths")
    fig.update_layout(
        autosize=False,
        width=1000,
        height=500,
    )
    return fig


@app.callback(
    Output('dd-stats-output-container', 'children'),
    [Input('stats-dropdown', 'value')])
def update_stats_output(value):
    return f"Statistic selected: {value}"


if __name__ == "__main__":
    app.run_server(debug=True)
