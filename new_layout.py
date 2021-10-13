import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

from data_utils import process_data, get_data
from graph_utils import don_rate_avg_don, num_don_num_causes

###################### App setup ######################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

###################### Data processing ######################

SubSecAvgDon_2018, SubSecDonRates_2018, DonRates_2018, AvgTotDon_2018,SubSecAvgNumDon_2018, AvgNumCauses_2018, AvgTotNumDon_2018 = get_data()

data = [SubSecAvgDon_2018, SubSecDonRates_2018, DonRates_2018, AvgTotDon_2018] 
data_num = [SubSecAvgNumDon_2018, AvgNumCauses_2018, AvgTotNumDon_2018] 

# TODO: Move this to data_utils
process_data(data)
process_data(data_num)

# Extract info from data for selection menus
region_names = SubSecAvgDon_2018['Region'].unique()
demo_names = SubSecAvgDon_2018['Group'].unique()

# Remove "All" from demographic names (will cause visualization to not show if not removed since demographic group "All" has no values under "Attribute", which is the column used for x-axis values in the graohs)
demo_names = np.delete(demo_names, 0)

###################### App layout ######################

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More blogs", header=True),
                    dbc.DropdownMenuItem("Blog 1", href="#"),
                    dbc.DropdownMenuItem("Blog 2", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="StatsCan Data Portal",
        brand_href="#",
        color="#c7102e",
        dark=True,
    ),
    html.Header([
        html.Div(className='overlay'),
        dbc.Container(
            dbc.Row(
                html.Div(
                    html.Div([
                        html.H1('Who Donates and How Much Do They Give?'),
                        html.Span(
                            'Author and date',
                            className='meta'
                        )
                        ],
                        className='post-heading'
                    ),
                    className='col-md-10 col-lg-8 mx-auto position-relative'
                )
            )
        ),
    ], 
        # className='masthead'       
        className="bg-secondary text-white text-center py-4",
    ),
   dbc.Container(
       dbc.Row([
            html.Div(
                [
                    "Select a region of focus:",
                    dcc.Dropdown(
                        # Object id (used to reference object within callbacks)
                        id='region-selection',
                        # Dropdown menu options (region_names is nparray defined above
                        options=[{'label': i, 'value': i} for i in region_names],
                        # Default value, shows up at top of dropdown list and automatically filters graphs upon loading
                        value='ON',
                        style={'verticalAlign': 'middle'}
                        ),
                    html.Br(),   
                ], 
                className='col-md-10 col-lg-8 mx-auto mt-4'
            ),
            # Overall likelihood of donating and levels of support
            html.Div(
                [
                    html.H4('Overall likelihood of donating and levels of support'),
                    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Ut venenatis tellus in metus vulputate. Id ornare arcu odio ut sem. Lacus luctus accumsan tortor posuere. Amet mattis vulputate enim nulla aliquet.  "),
                    html.Br(), 
                    dcc.Graph(id='graph-1')
                ], className='col-md-10 col-lg-8 mx-auto'
            ),
            # Demographic patterns of donating
            html.Div(
                [
                    html.H4('Demographic patterns of donating'),
                    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Ut venenatis tellus in metus vulputate. Id ornare arcu odio ut sem. Lacus luctus accumsan tortor posuere. Amet mattis vulputate enim nulla aliquet.  "),
                    html.Br(),
                    dcc.Graph(id='graph-2')
                ], className='col-md-10 col-lg-8 mx-auto'
            ),
            # Breadth and focus of support
            html.Div(
                [
                    html.H4('Breadth and focus of support'),
                    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Ut venenatis tellus in metus vulputate. Id ornare arcu odio ut sem. Lacus luctus accumsan tortor posuere. Amet mattis vulputate enim nulla aliquet.  "),
                    html.Br(),
                    dcc.Graph(id='graph-3')
                ], className='col-md-10 col-lg-8 mx-auto'
            ),
            # Example with multiple controls
            html.Div(
                [
                    html.H4('Example with multiple controls'),
                    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Ut venenatis tellus in metus vulputate. Id ornare arcu odio ut sem. Lacus luctus accumsan tortor posuere. Amet mattis vulputate enim nulla aliquet.  "),
                    "Choose demographic feature to display below: ",
                    dcc.Dropdown(id='graph-4-demos',
                                options=[{'label': i, 'value': i} for i in demo_names],
                                value="Age group")
                    , #style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
                    html.Br(),
                    dcc.Graph(id='graph-4')
                ], className='col-md-10 col-lg-8 mx-auto'
            ),
        ]),     
   ),
   html.Footer(
       dbc.Container(
           dbc.Row(
               html.Div(
                   html.P('Copyright © Imagine Canada 2021',className="text-center"),
                   className='col-md-10 col-lg-8 mx-auto mt-5'
               ),
           )
       )
   )
])

###################### Callbacks ######################

# Interaction: graph-1, with region-selection
@app.callback(
    dash.dependencies.Output('graph-1', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
     ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by age group", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

# Interaction: graph-2, with region-selection
@app.callback(
    dash.dependencies.Output('graph-2', 'figure'),
    [dash.dependencies.Input('region-selection', 'value')])

def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by education", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

# Interaction: graph-3, with region-selection
@app.callback(
    dash.dependencies.Output('graph-3', 'figure'),
    [dash.dependencies.Input('region-selection', 'value')])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by personal income", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

# Interaction: graph-4, with region-selection and graph-4-demos
@app.callback(
    dash.dependencies.Output('graph-4', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('graph-4-demos', 'value')
    ])
def update_graph(region, demo):
    dff1 = AvgTotNumDon_2018[AvgTotNumDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == demo]
    name1 = "Average number of annual donations"

    dff2 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == demo]
    name2 = "Average number of causes supported"

    title = '{} \n by {}, {}'.format("Average number of causes supported and average number of donations annually", demo, region)

    return num_don_num_causes(dff1, dff2, name1, name2, title)



if __name__ == "__main__":
    app.run_server(debug=True)

