import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Reading in data from public urls
# DonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-DonRate.csv")
DonRates_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-DonRate.csv")
# AvgTotDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotDon.csv")
AvgTotDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-AvgTotDon.csv")
AvgNumCauses_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgNumCauses.csv")
FormsGiving_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-FormsGiving.csv")
TopCauseFocus_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-TopCauseFocus.csv")
PropTotDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-PercTotDonors.csv")
PropTotDonAmt_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-PercTotDonations.csv")

# Format donation rates as percentage
DonRates_2018['Estimate'] = DonRates_2018['Estimate']*100
DonRates_2018['CI Upper'] = DonRates_2018['CI Upper']*100
FormsGiving_2018['Estimate'] = FormsGiving_2018['Estimate']*100
FormsGiving_2018['CI Upper'] = FormsGiving_2018['CI Upper']*100
TopCauseFocus_2018['Estimate'] = TopCauseFocus_2018['Estimate']*100
TopCauseFocus_2018['CI Upper'] = TopCauseFocus_2018['CI Upper']*100
PropTotDon_2018['Estimate'] = PropTotDon_2018['Estimate']*100
PropTotDon_2018['CI Upper'] = PropTotDon_2018['CI Upper']*100
PropTotDonAmt_2018['Estimate'] = PropTotDonAmt_2018['Estimate']*100
PropTotDonAmt_2018['CI Upper'] = PropTotDonAmt_2018['CI Upper']*100

# Create list of dataframes for iterated cleaning
# "data" contains estimates that are dollar amounts or rates, "data_num" contains estimates that are numbers
data = [DonRates_2018, AvgTotDon_2018, FormsGiving_2018, TopCauseFocus_2018, PropTotDon_2018, PropTotDonAmt_2018]
data_num = [AvgNumCauses_2018]


# Add annotation, suppress estimates/CI bounds where necessary, round estimate values according to estimate type (as above)
# Annotation text
values = ["Use with caution", "Estimate suppressed", ""]

i = 0
while i < len(data):
    # Different marker values
    conditions = [data[i]["Marker"] == "*",
                  data[i]["Marker"] == "...",
                  pd.isnull(data[i]["Marker"])]
    # Assign annotation text according to marker values
    data[i]["Annotation"] = np.select(conditions, values)

    # Suppress Estimate and CI Upper where necessary (for visualizations and error bars)
    data[i]["Estimate"] = np.where(data[i]["Marker"]=="...", 0, data[i]["Estimate"])
    data[i]["CI Upper"] = np.where(data[i]["Marker"]=="...", 0, data[i]["CI Upper"])

    # Round rates and dollar amounts to zero decimal places
    data[i]['Estimate'] = data[i]['Estimate'].round(0)
    data[i]["CI Upper"] = data[i]["CI Upper"].round(0)
    i = i + 1

i = 0
while i < len(data_num):
    # Different marker values
    conditions = [data_num[i]["Marker"] == "*",
                  data_num[i]["Marker"] == "...",
                  pd.isnull(data_num[i]["Marker"])]
    # Assign annotation text according to marker values
    data_num[i]["Annotation"] = np.select(conditions, values)

    # Suppress Estimate and CI Upper where necessary (for visualizations and error bars)
    data_num[i]["Estimate"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["Estimate"])
    data_num[i]["CI Upper"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["CI Upper"])

    # Round number amounts to two decimal places
    data_num[i]['Estimate'] = data_num[i]['Estimate'].round(2)
    data_num[i]["CI Upper"] = data_num[i]["CI Upper"].round(2)
    i = i + 1

# Extract info from data for selection menus
region_names = np.array(['CA', 'CA (without QC)', 'AB', 'AT', 'BC', 'ON', 'PR', 'QC'], dtype=object)
demo_names = np.array(['Gender', 'Marital status', 'Labour force status', 'Frequency of religious attendance', 'Immigration status'], dtype=object)

fig1df1 = DonRates_2018[DonRates_2018['Group'] == "All"]
fig1df1 = fig1df1[fig1df1.Province.notnull()]

fig1df2 = AvgTotDon_2018[AvgTotDon_2018['Group'] == "All"]
fig1df2 = fig1df2[fig1df2.Province.notnull()]


fig1 = go.Figure()

fig1.add_trace(go.Bar(x=fig1df1['Province'],
                      y=fig1df1['Estimate'],
                      error_y=dict(type="data", array=fig1df1["CI Upper"]-fig1df1["Estimate"]),
                      hovertext=fig1df1['Annotation'],
                      marker=dict(color="#7BAFD4"),
                      text=fig1df1.Estimate.map(str)+"%",
                      textposition='inside',
                      insidetextanchor='start',
                      name="Donor rate",
                      yaxis='y2',
                      offsetgroup=2
                      ),
               )

fig1.add_trace(go.Bar(x=fig1df2['Province'],
                      y=fig1df2['Estimate'],
                      error_y=dict(type="data", array=fig1df2["CI Upper"]-fig1df2["Estimate"]), # need to vectorize subtraction
                      hovertext =fig1df2['Annotation'],
                      marker=dict(color="#c8102e"),
                      text="$"+fig1df2.Estimate.map(str),
                      textposition='inside',
                      insidetextanchor='start',
                      name="Average donation amount",
                      offsetgroup=1
                      ),
               )

y2 = go.layout.YAxis(overlaying='y', side='right')

fig1.update_layout(title={'text': "Donation rate & average donation amount by province",
                          'y': 0.99},
                   margin=dict(l=20, r=20, t=100, b=20),
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   barmode="group",
                   yaxis2=y2,
                   legend={'orientation': 'h', 'yanchor': "bottom", 'xanchor': 'left'}
                   )
fig1.update_traces(error_x_color="#757575")

# Aesthetics for fig
fig1.update_yaxes(showgrid=False, showticklabels=False)

fig1.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

### General app layout/set up ###
app.layout = html.Div([
    # Top row element (centred)
    html.Div([
        # Text element (title)
        html.H1('Who donates and how much do they give?')]),
    # Second row element (centred)
    html.Div([
        # Wrapper to contain text and dropdown menu (centred)
        html.Div(["Select a region of focus:",
                  # Region selection
                  dcc.Dropdown(
                      # Object id (used to reference object within callbacks)
                      id='region-selection',
                      # Dropdown menu options (region_names is nparray defined above
                      options=[{'label': i, 'value': i} for i in region_names],
                      # Default value, shows up at top of dropdown list and automatically filters graphs upon loading
                      value='ON',
                      style={'verticalAlgin': 'middle'}
                  ),
                  ],
                 style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div([
        # Graph components!
        dcc.Graph(id='FormsGiving', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-prv', figure=fig1, style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Age', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Educ', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Inc', style={'marginTop': 50}),
        html.Div([
            "Choose demographic feature to display below: ",
            dcc.Dropdown(id='DonRateAvgDonAmt-selection',
                         options=[{'label': i, 'value': i} for i in demo_names],
                         value="Gender")
        ], style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
        dcc.Graph(id='DonRateAvgDonAmt-other', style={'marginTop': 15}),
        dcc.Graph(id='PercDon-Age', style={'marginTop': 100}),
        dcc.Graph(id='PercDon-Educ', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-Inc', style={'marginTop': 50}),
        html.Div([
            "Choose demographic feature to display below: ",
            dcc.Dropdown(id='PercDon-selection',
                         options=[{'label': i, 'value': i} for i in demo_names],
                         value="Gender")
        ], style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
        dcc.Graph(id='PercDon-other', style={'marginTop': 15}),
        dcc.Graph(id='PrimCauseNumCause-Age', style={'marginTop': 100}),
        dcc.Graph(id='PrimCauseNumCause-Educ', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-Inc', style={'marginTop': 50}),
        html.Div([
            "Choose demographic feature to display below: ",
            dcc.Dropdown(id='PrimCauseNumCause-selection',
                         options=[{'label': i, 'value': i} for i in demo_names],
                         value="Gender")
        ], style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
        dcc.Graph(id='PrimCauseNumCause-other', style={'marginTop': 15})

    ],
        style={'width': '50%', 'display': 'inline-block', "marginTop": 20}),

])

def forms_of_giving(dff, title):
    fig = go.Figure()

    fig.add_trace(go.Bar(y=dff['Estimate'],
                         x=dff['QuestionText'],
                         error_y=dict(type="data", array=dff["CI Upper"]-dff["Estimate"]), # need to vectorize subtraction
                         # hover_data =['Annotation'],
                         marker=dict(color="#7BAFD4"),
                         hovertext=dff['Annotation'],
                         text=dff.Estimate.map(str)+"%",
                         textposition='inside',
                         insidetextanchor='start'
                         )
                  )
    fig.update_yaxes(categoryarray=np.array(["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC"]), categoryorder='array')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin=dict(l=20, r=20, t=100, b=20),
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      )
    fig.update_traces(error_y_color="#757575")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False)

    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

# Functions to produce Plot.ly graphs
def don_rate_avg_don(dff1, dff2, name1, name2, title):
    '''
    Produces a horizontal double bar graph with TWO DIFFERENT X-AXES displaying estimates from the inputted region, formatted specifically to compare donation rate (%) and donation amount ($) data.

    dff1 and dff2 must be filtered for the correct region-demographic combination before don_rate_avg_don() is called (in this file, this step is done within update_graph() after the relevant callback).

    X-axis 1: Estimate in $
    X-axis 2: Estimate in %
    Y-axis: Demographic trait (ie. age groups, income categories, genders, etc.).

    :param dff1: Donation amount dataframe (estimates in $)
    :param dff2: Donation rate dataframe (estimates in %)
    :param name1: Legend name for dff1
    :param name2: Legend name for dff2
    :param title: Graph title (str)
    :return: Plot.ly graph object
    '''

    # Scatter plot - data frame, x label, y label
    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff2['Estimate'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"]), # need to vectorize subtraction
                         hovertext =dff2['Annotation'],
                         marker=dict(color="#c8102e"),
                         text="$"+dff2.Estimate.map(str),
                         textposition='inside',
                         insidetextanchor='start',
                         name=name2,
                         offsetgroup=1
                         ),
                  )

    fig.add_trace(go.Bar(x=dff1['Estimate'],
                         y=dff1['Attribute'],
                         orientation="h",
                         error_x=dict(type="data", array=dff1["CI Upper"]-dff1["Estimate"]),
                         hovertext=dff1['Annotation'],
                         marker=dict(color="#7BAFD4"),
                         text=dff1.Estimate.map(str)+"%",
                         textposition='inside',
                         insidetextanchor='start',
                         name=name1,
                         xaxis='x2',
                         offsetgroup=2
                         ),
                  )

    x2 = go.layout.XAxis(overlaying='x', side='bottom')

    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin=dict(l=20, r=20, t=100, b=20),
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      barmode="group",
                      xaxis2=x2,
                      legend={'orientation': 'h', 'yanchor': "bottom", 'traceorder': 'reversed'}
                      )
    fig.update_traces(error_x_color="#757575")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False, showticklabels=False)

    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

def perc_don_perc_amt(dff1, dff2, name1, name2, title):
    '''
    Produces a horizontal double bar graph with ONE X-AXIS displaying estimates from the inputted region, formatted specifically to compare quantities (number of donations, causes, hours, etc.)
    currently specific to number of annual donations and number of causes support.

    dff1 and dff2 must be filtered for the correct region-demographic combination before num_don_num_causes() is called (in this file, this step is done within update_graph() after the relevant callback).

    X-axis: Estimate
    Y-axis: Demographic trait (ie. age groups, income categories, genders, etc.).

    :param dff1: Number of donations dataframe OR number of causes dataframe (interchangeable; no label formatting for units)
    :param dff2: Number of donations dataframe OR number of causes dataframe (interchangeable; no label formatting for units)
    :param name1: Legend name for dff1
    :param name2: Legend name for dff2
    :param title: Graph title (str)
    :return: Plot.ly graph object
    '''

    # Scatter plot - data frame, x label, y label
    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff2['Estimate'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"]), # need to vectorize subtraction
                         hovertext =dff2['Annotation'],
                         marker=dict(color="#c8102e"),
                         text=dff2.Estimate.map(str)+"%",
                         textposition='inside',
                         insidetextanchor='start',
                         name=name2,
                         offsetgroup=1
                         ),
                  )

    fig.add_trace(go.Bar(x=dff1['Estimate'],
                         y=dff1['Attribute'],
                         orientation="h",
                         error_x=dict(type="data", array=dff1["CI Upper"]-dff1["Estimate"]),
                         hovertext=dff1['Annotation'],
                         marker=dict(color="#7BAFD4"),
                         text=dff1.Estimate.map(str)+"%",
                         textposition='inside',
                         insidetextanchor='start',
                         name=name1,
                         offsetgroup=2
                         ),
                  )

    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin=dict(l=20, r=20, t=100, b=20),
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      barmode="group",
                      legend={'orientation': 'h', 'yanchor': "middle", 'traceorder': 'reversed'}
                      )
    fig.update_traces(error_x_color="#757575")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False, showticklabels=False)
    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

def prim_cause_num_cause(dff1, dff2, name1, name2, title):
    '''
   Produces a horizontal double bar graph with TWO DIFFERENT X-AXES displaying estimates from the inputted region, formatted specifically to compare donation rate (%) and donation amount ($) data.

   dff1 and dff2 must be filtered for the correct region-demographic combination before don_rate_avg_don() is called (in this file, this step is done within update_graph() after the relevant callback).

   X-axis 1: Estimate in $
   X-axis 2: Estimate in %
   Y-axis: Demographic trait (ie. age groups, income categories, genders, etc.).

   :param dff1: Donation amount dataframe (estimates in $)
   :param dff2: Donation rate dataframe (estimates in %)
   :param name1: Legend name for dff1
   :param name2: Legend name for dff2
   :param title: Graph title (str)
   :return: Plot.ly graph object
   '''

    # Scatter plot - data frame, x label, y label
    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff2['Estimate'],
                     y=dff2['Attribute'],
                     orientation="h",
                     error_x=dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"]), # need to vectorize subtraction
                     hovertext =dff2['Annotation'],
                     marker=dict(color="#c8102e"),
                     text=dff2["Estimate"],
                     textposition='inside',
                     insidetextanchor='start',
                     name=name2,
                     offsetgroup=1
                     ),
              )

    fig.add_trace(go.Bar(x=dff1['Estimate'],
                     y=dff1['Attribute'],
                     orientation="h",
                     error_x=dict(type="data", array=dff1["CI Upper"]-dff1["Estimate"]),
                     hovertext=dff1['Annotation'],
                     marker=dict(color="#7BAFD4"),
                     text=dff1.Estimate.map(str)+"%",
                     textposition='inside',
                     insidetextanchor='start',
                     name=name1,
                     xaxis='x2',
                     offsetgroup=2
                     ),
              )

    x2 = go.layout.XAxis(overlaying='x', side='bottom')

    fig.update_layout(title={'text': title,
                         'y': 0.99},
                  margin=dict(l=20, r=20, t=100, b=20),
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  barmode="group",
                  xaxis2=x2,
                  legend={'orientation': 'h', 'yanchor': "bottom", 'traceorder': 'reversed'}
                  )
    fig.update_traces(error_x_color="#757575")

# Aesthetics for fig
    fig.update_xaxes(showgrid=False, showticklabels=False)

    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('FormsGiving', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    """
    Construct or update graph according to input from 'region-selection' dropdown menu.

    :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
    :return: Plot.ly graph object, produced by don_rate_avg_don().
    """
    # Donation rate data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff1 = FormsGiving_2018[FormsGiving_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "All"]

    # Format title according to dropdown input
    title = '{}, {}'.format("Forms of giving", region)

    # Uses external function with dataframes, names, and title set up above
    return forms_of_giving(dff1, title)


# Interaction: graph-1, with region-selection
@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('DonRateAvgDonAmt-Age', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    """
    Construct or update graph according to input from 'region-selection' dropdown menu.

    :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
    :return: Plot.ly graph object, produced by don_rate_avg_don().
    """
    # Donation rate data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by age group", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('DonRateAvgDonAmt-Educ', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    """
    Construct or update graph according to input from 'region-selection' dropdown menu.

    :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
    :return: Plot.ly graph object, produced by don_rate_avg_don().
    """
    # Donation rate data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by education", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('DonRateAvgDonAmt-Inc', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    """
    Construct or update graph according to input from 'region-selection' dropdown menu.

    :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
    :return: Plot.ly graph object, produced by don_rate_avg_don().
    """
    # Donation rate data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by income", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('DonRateAvgDonAmt-other', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('DonRateAvgDonAmt-selection', 'value')
    ])
def update_graph(region, demo):
    """
    Construct or update graph according to input from 'region-selection' dropdown menu.

    :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
    :return: Plot.ly graph object, produced by don_rate_avg_don().
    """
    # Donation rate data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == demo]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == demo]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{} by {}, {}'.format("Donor rate and average annual donation", demo, region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)


# Interaction: graph-2, with region-selection
@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('PercDon-Age', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value')
    ])

def update_graph(region):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    # Donation rate data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by age", region)

    # Uses external function with dataframes, names, and title set up above
    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('PercDon-Educ', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    # Donation rate data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by education", region)

    # Uses external function with dataframes, names, and title set up above
    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('PercDon-Inc', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    # Donation rate data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by income", region)

    # Uses external function with dataframes, names, and title set up above
    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('PercDon-other', 'figure'),
    [
        # Input: selected region from region-selection (dropdown menu)
        # In the case of multiple inputs listed here, they will enter as arguments into the function below in the order they are listed
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('PercDon-selection', 'value')
    ])
def update_graph(region, demo):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    # Donation rate data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == demo]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == demo]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{} by {}, {}'.format("Percentage of donors & total donation value", demo, region)

    # Uses external function with dataframes, names, and title set up above
    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('PrimCauseNumCause-Age', 'figure'),
    [
        # Inputs: selected region from region-selection and selected demographic group from graph-4-demos (dropdown menu)
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :param demo: Demographic group name (str). Automatically inherited from 'graph-4-demos' dcc.Dropdown() input via dash.dependencies.Input('graph-4-demos', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by age", region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('PrimCauseNumCause-Educ', 'figure'),
    [
        # Inputs: selected region from region-selection and selected demographic group from graph-4-demos (dropdown menu)
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :param demo: Demographic group name (str). Automatically inherited from 'graph-4-demos' dcc.Dropdown() input via dash.dependencies.Input('graph-4-demos', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by education", region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('PrimCauseNumCause-Inc', 'figure'),
    [
        # Inputs: selected region from region-selection and selected demographic group from graph-4-demos (dropdown menu)
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :param demo: Demographic group name (str). Automatically inherited from 'graph-4-demos' dcc.Dropdown() input via dash.dependencies.Input('graph-4-demos', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    # Average number of annual donations data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by income", region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('PrimCauseNumCause-other', 'figure'),
    [
        # Inputs: selected region from region-selection and selected demographic group from graph-4-demos (dropdown menu)
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('PrimCauseNumCause-selection', 'value')
    ])
def update_graph(region, demo):
    """
        Construct or update graph according to input from 'region-selection' dropdown menu.

        :param region: Region name (str). Automatically inherited from 'region-selection' dcc.Dropdown() input via dash.dependencies.Input('region-selection', 'value') above.
        :param demo: Demographic group name (str). Automatically inherited from 'graph-4-demos' dcc.Dropdown() input via dash.dependencies.Input('graph-4-demos', 'value') above.
        :return: Plot.ly graph object, produced by don_rate_avg_don().
    """

    # Average number of annual donations data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == demo]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == demo]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{} by {}, {}'.format("Focus on primary cause & average number of causes supported", demo, region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)




if __name__ == '__main__':
    app.run_server(debug=True)
