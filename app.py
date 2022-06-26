import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from parse import *
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash("__name__")
server = app.server

PROVINCE = "ON"
DATES = get_weekly()
STATS = ["cases", "mortality", "recovered", "testing", "active"]


# json_data = get_request(PROVINCE, DATES, STATS)
df = get_all_info(PROVINCE, DATES, STATS)
print(df)
TITLE_PROVINCE = get_prov_name(PROVINCE)
fig = px.line(df, x="Date", y="Count", color="Statistic",
              line_group="Statistic", title="Time-Series Data of {}".format(TITLE_PROVINCE))

df2 = get_all_cumulative_info(PROVINCE, DATES, STATS)
fig2 = px.bar(df2, x="Statistic", y="Count",
              title="Cumulative Data of {}".format(TITLE_PROVINCE))

app.layout = html.Div([
    html.Div([
        html.H2('COVID-19 Data Visualization of Canada'),
    ], className="banner"),

    html.Div([
        html.H3('Case Overview'),
        # html.Img(
        # src=app.get_asset_url('virus-graphic.png'), className="resize2",),
    ], className="info-header"),
    html.Div([
    ], className="info-box"),
    
    #html.Div([
        #html.H3('Multi-variable chart visualization',
                #className="graph-header"),
    #]),
    #html.Div([
        #html.H3('Multi-variable bar-graph visualization',
                #className="bar-header"),
    #]),
    
    html.Div([
        html.H3('Input Variables for Dynamic Output',
                className="input-header"),
    ]),
    
    #html.Div([
    #], className="bar-header-container"),
    #html.Div([
    #], className="graph-header-container"),
    
    html.Div([
    ], className="input-header-container"),
    # html.Img(
    # src=app.get_asset_url('virus-logo.png'), className="resize",),

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
    html.Div(
        id="graph-container",
        children=dcc.Graph(id="graph", figure=fig),
    ),
    html.Div(
        id="bar-container",
        children=dcc.Graph(id="graph2", figure=fig2),
    )
])


@ app.callback(
    Output('dd-province-output-container', 'children'),
    [Input('province-dropdown', 'value')])
def update_province_output(value):
    return f"Province Selected: {value}"


@ app.callback(
    Output('dd-time-output-container', 'children'),
    [Input('time-dropdown', 'value')])
def update_time_output(value):
    return f"Timeframe Selected: {value}"


@ app.callback(
    Output('graph', 'figure'),
    Input('province-dropdown', 'value'),
    Input('time-dropdown', 'value'),
    Input('checklist', 'value')
)
def update_graph(prov_val, time_val, stats):
    PROVINCE = prov_val
    DATES = calculate_date(time_val)
    stats.sort()  # sorts list to maintain color
    df = get_all_info(PROVINCE, DATES, stats)
    PROVINCE = get_prov_name(PROVINCE)
    fig = px.line(df, x="Date", y="Count", color="Statistic",
                  line_group="Statistic", title="Time-Series Data of {}".format(PROVINCE))
    fig.update_layout(
        autosize=True,
        margin=dict(
            pad=0,
        ),
        title={
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    return fig


@ app.callback(
    Output('graph2', 'figure'),
    Input('province-dropdown', 'value'),
    Input('time-dropdown', 'value'),
    Input('checklist', 'value')
)
def update_bars(prov_val, time_val, stats):
    PROVINCE = prov_val
    DATES = calculate_date(time_val)
    stats.sort()

    df2 = get_all_cumulative_info(PROVINCE, DATES, stats)
    PROVINCE = get_prov_name(PROVINCE)
    fig2 = px.bar(df2, x="Statistic", y="Count",
                  title="Cumulative Data of {}".format(PROVINCE))
    fig2.update_layout(
        height=780,
        title={
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    return fig2


if __name__ == "__main__":
    app.run_server(debug=True)
