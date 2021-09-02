import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read in data - CHANGE PATHWAY
SubSecAvgDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecAvgDon.csv")
conditions = [SubSecAvgDon_2018["Marker"] == "*",
              SubSecAvgDon_2018["Marker"] == "...",
              pd.isnull(SubSecAvgDon_2018["Marker"])]
values = ["Use with caution", "Estimate supressed", ""]
SubSecAvgDon_2018["Annotation"] = np.select(conditions, values)
SubSecAvgDon_2018["Estimate"] = np.where(SubSecAvgDon_2018["Marker"]=="...", 0, SubSecAvgDon_2018["Estimate"])
SubSecAvgDon_2018["CI Upper"] = np.where(SubSecAvgDon_2018["Marker"]=="...", 0, SubSecAvgDon_2018["CI Upper"])

# Extract info from data for selection menus
available_demographics = SubSecAvgDon_2018['Group'].unique()
region_names = SubSecAvgDon_2018['Region'].unique()
sector_names = SubSecAvgDon_2018['QuestionText'].unique()

# General app layout/set up
app.layout = html.Div([
    # TOP/PAGE LEVEL
    html.Div([
        # Page title
        html.H1('Average Donation Per Sub-Sector'),
        # Page level filter (dropdown menu); shows up just under title vertically
        html.Div([
            dcc.Dropdown(
                # Object id (used to reference object within interface backend/code)
                id='region-selection',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in region_names],
                # Default value, shows up at top of dropdown list
                value='ON'
            ),
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                # Object id (used to reference object within interface backend/code)
                id='sector-selection',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in sector_names],
                # Default value, shows up at top of dropdown list
                value='Arts & culture'
            ),
        ],
            style={'width': '49%', 'display': 'inline-block'}),
    ]),
    # SECOND ROW (graph level)
    html.Div([
        # Left dropdown menu
        html.Div([
            dcc.Dropdown(
                # Object id (used to reference object within interface backend/code)
                id='crossfilter-xaxis-column',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in available_demographics],
                # Default value, shows up at top of dropdown list
                value='Age group'
            ),
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        # Right dropdown menu
        html.Div([
            dcc.Dropdown(
                # Object id (used to reference object within interface backend/code)
                id='crossfilter-yaxis-column',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in available_demographics],
                # Default value, shows up at top of dropdown list
                value='Age group'
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'padding': '10px 5px'
    }),
    # Left graph
    html.Div([
        # ID for use with below function implementation
        dcc.Graph(id='left-time-series',)
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    # Right graph
    html.Div([
        # ID for use with below function implementation
        dcc.Graph(id='right-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),


])

# Function: create bar graph
def create_bar_graph(dff, title):

    # Scatter plot - data frame, x label, y label
    fig = px.bar(dff,
                 x='Estimate',
                 y='Attribute',
                 orientation="h",
                 # error_x=dict(value=dff["CI Upper"] - dff["Estimate"], color="grey"),
                 # hovertext = ...
                 # name = ...
                 )

    # Add CA comparison
    # fig.add_trace(SubSecAvgDon_2018[(SubSecAvgDon_2018['Group']=='All') and (SubSecAvgDon_2018['Region']=='CA')],
    #              x='Estimate',
    #              y='Attribute',
    #              orientation='h',
    #              marker_color="#FBC02D")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False)
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

# Interaction?
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('left-time-series', 'figure'),
    [
    # ...according to input from top (page level) and left (graph level) drop downs
     dash.dependencies.Input('region-selection', 'value'),
     dash.dependencies.Input('sector-selection', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     ])
# TODO: How does this get activated???
def update_y_timeseries(region, sector, xaxis_column_name):
    dff = SubSecAvgDon_2018[SubSecAvgDon_2018['Region'] == region]
    dff = dff[dff['QuestionText'] == sector]
    dff = dff[dff['Group'] == xaxis_column_name]
    title = '<b>{}</b><br>{}, {}'.format(sector, xaxis_column_name, region)
    # Uses above function
    return create_bar_graph(dff, title)


@app.callback(
    # Changes left graph...
    dash.dependencies.Output('right-time-series', 'figure'),
    [
    # ...according to input from top (page level) and left (graph level) drop downs
    dash.dependencies.Input('region-selection', 'value'),
    dash.dependencies.Input('sector-selection', 'value'),
    dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     ])
# TODO: How does this get activated???
def update_x_timeseries(region, sector, yaxis_column_name):
    dff = SubSecAvgDon_2018[SubSecAvgDon_2018['Region'] == region]
    dff = dff[dff['QuestionText'] == sector]
    dff = dff[dff['Group'] == yaxis_column_name]
    # Uses above function
    return create_bar_graph(dff, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)
