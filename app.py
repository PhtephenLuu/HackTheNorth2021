import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from parse import *
from whitenoise import Whitenoise
import plotly.express as px
import plotly.graph_objects as go

server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root=‘static/’)
app = dash.Dash()

PROVINCE = "ON"
DATES = get_weekly()
STATS = ["cases", "mortality", "recovered", "testing", "active"]

get_all_cumulative_info(PROVINCE, DATES)

# json_data = get_request(PROVINCE, DATES, STATS)
df = get_all_info(PROVINCE, DATES, STATS)
PROVINCE = get_prov_name(PROVINCE)
fig = px.line(df, x="date", y="count", color="topic",
              line_group="topic", title="Time-Series Data of {}".format(PROVINCE))


app.layout = html.Div([
    html.Div([
        html.H2('COVID-19 Data Visualization of Canada'),
    ], className="banner"),

    html.Div([
        html.H3('Case overview'),
        html.Img(
            src=app.get_asset_url('virus-graphic.png'), className="resize2",),
    ], className="info-box"),

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
            {'label': 'Quebec', 'value': 'QC'},
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
    ),
    html.Div([
        dcc.Checklist(
            id="checklist",
            options=[
                {"label": "Cases", "value": "cases"},
                {"label": "Deaths", "value": "mortality"},
                {"label": "Recovered", "value": "recovered"},
                {"label": "Testing", "value": "testing"},
                {"label": "Active", "value": "active"}
            ],
            value=["cases", "mortality", "recovered", "testing", "active"],
            labelStyle={'display': 'inline-block'}
        )], className="checklist-container"
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
    Input('checklist', 'value')
)
def update_graph(prov_val, time_val, stats):
    PROVINCE = prov_val
    DATES = calculate_date(time_val)
    stats.sort() # sorts list to maintain color
    df = get_all_info(PROVINCE, DATES, stats)
    PROVINCE = get_prov_name(PROVINCE)
    fig = px.line(df, x="date", y="count", color="topic",
                  line_group="topic", title="Time-Series Data of {}".format(PROVINCE))
    fig.update_layout(
        autosize=True,
        width=1000,
        height=500,
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
