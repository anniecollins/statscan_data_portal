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

# Read in data - CHANGE DIRECTORIES AS NEEDED
# SubSecAvgDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-SubSecAvgDon.csv")
# SubSecAvgNumDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-SubSecAvgNumDon.csv")
# SubSecDonRates_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-SubSecDonRates.csv")
# DonRates_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-DonRate.csv")
# AvgTotDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-AvgTotDon.csv")
# AvgNumCauses_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-AvgNumCauses.csv")
# AvgTotNumDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables/2018-AvgTotNumDon.csv")

# Reading in data from public urls
SubSecAvgDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-SubSecAvgDon.csv")
SubSecAvgNumDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-SubSecAvgNumDon.csv")
SubSecDonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-SubSecDonRates.csv")
DonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-DonRate.csv")
AvgTotDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotDon.csv")
AvgNumCauses_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgNumCauses.csv")
AvgTotNumDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotNumDon.csv")

# Format donation rates as percentage
DonRates_2018['Estimate'] = DonRates_2018['Estimate']*100
DonRates_2018['CI Upper'] = DonRates_2018['CI Upper']*100

# Create list of dataframes for iterated cleaning
# "data" contains estimates that are dollar amounts or rates, "data_num" contains estimates that are numbers
data = [SubSecAvgDon_2018, SubSecDonRates_2018, DonRates_2018, AvgTotDon_2018]
data_num = [SubSecAvgNumDon_2018, AvgNumCauses_2018, AvgTotNumDon_2018]


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
region_names = SubSecAvgDon_2018['Region'].unique()
demo_names = SubSecAvgDon_2018['Group'].unique()
# Remove "All" from demographic names (will cause visualization to not show if not removed since demographic group "All" has no values under "Attribute", which is the column used for x-axis values in the graohs)
demo_names = np.delete(demo_names, 0)

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
    # Left main body element - Text
    html.Div(
        # Dave's text here
        dcc.Markdown('''        
        ## Overall likelihood of donating and levels of support
        
        ## Demographic patterns of donating
        
        ## Breadth and focus of support
        
        '''),
        # TODO: Might need to customize dimensions once text is in place
        style={'width': '50%', 'height': 800, 'marginTop': 20, 'display': 'inline-block'}),

    html.Div([
        # Graph components!
        dcc.Graph(id='graph-1', style={'marginTop': 50}),
        dcc.Graph(id='graph-2', style={'marginTop': 50}),
        dcc.Graph(id='graph-3', style={'marginTop': 50}),
        # Dropdown menu, linked "graph-4"
        html.Div([
            "Choose demographic feature to display below: ",
            dcc.Dropdown(id='graph-4-demos',
                         options=[{'label': i, 'value': i} for i in demo_names],
                         value="Age group")
            ], style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
        dcc.Graph(id='graph-4')
        ],
        style={'width': '40%', 'display': 'inline-block', 'height': 800, "marginTop": 20}),

])

# Functions to produce Plot.ly graphs
def create_bar_graph(dff, CA_dff, CAnoQC_dff, title, region):
    '''
    Produces a horizontal single bar graph displaying estimates from the inputted region. Options to toggle on and off bars to compare with Canada-wide and Canada-wide-excluding-Quebec estimates.

    dff, CA_dff, and CAnoQC_dff must be filtered for the correct region-demographic combination before create_bar_graph() is called (in this file, this step is done within update_graph() after the relevant callback).

    X-axis: Estimate
    Y-axis: Demographic trait (ie. age groups, income categories, genders, etc.).

    :param dff: Region-specific dataframe
    :param CA_dff: Canada-only dataframe
    :param CAnoQC_dff: Canada (without QC)-only dataframe
    :param title: Graph title (str)
    :param region: Name of region (str)
    :return: Plot.ly graph object
    '''

    # Scatter plot - data frame, x label, y label
    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff['Estimate'],
                        y=dff['Attribute'],
                        orientation="h",
                        error_x=dict(type="data", array=dff["CI Upper"]-dff["Estimate"]), # need to vectorize subtraction
                        # hover_data =['Annotation'],
                        marker=dict(color="#FDD835"),
                        name = region
                        )
                  )

    fig.add_trace(go.Bar(x=CA_dff['Estimate'],
                         y=CA_dff['Attribute'],
                         orientation="h",
                         error_x=dict(type="data", array=CA_dff["CI Upper"]-CA_dff["Estimate"]), # need to vectorize subtraction
                         # hover_data=['Annotation'],
                         marker=dict(color="#FBC02D"),
                         name="Canada",
                         visible=False
                         )
                  )

    fig.add_trace(go.Bar(x=CAnoQC_dff['Estimate'],
                         y=CAnoQC_dff['Attribute'],
                         orientation="h",
                         error_x=dict(type="data", array=CAnoQC_dff["CI Upper"]-CAnoQC_dff["Estimate"]), # need to vectorize subtraction
                         # hover_data=['Annotation'],
                         marker=dict(color="#F9A825"),
                         name="Canada (without Quebec)",
                         visible=False
                         )
                  )

    fig.update_xaxes(showticklabels=False)
    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin=dict(l=20, r=20, t=100, b=20),
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      barmode="group",
                      updatemenus=[
                          dict(
                              type="buttons",
                              xanchor="left",
                              x=1,
                              y=0.75,
                              #yanchor="top",
                              buttons=[
                                  dict(label="Reset",
                                       method="update",
                                       args=[{"visible": [True, False, False]}]),
                                  dict(label="Canada",
                                       method="update",
                                       args=[{"visible": [True, True, False]}]),
                                  dict(label="Canada (without Quebec)",
                                       method="update",
                                       args=[{"visible": [True, False, True]}])
    ])]
                      )
    fig.update_traces(error_x_color="#757575")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False)

    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

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

    TODO: this could be made more generic, or kept specific but with fewer arguments. Not sure about best way forward yet.
    '''

    # Scatter plot - data frame, x label, y label
    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff2['Estimate'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"]), # need to vectorize subtraction
                         hovertext =dff2['Annotation'],
                         marker=dict(color="#81D4F4"),
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
                         marker=dict(color="#FDD835"),
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

def num_don_num_causes(dff1, dff2, name1, name2, title):
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
                         marker=dict(color="#FFA000"),
                         text=dff2['Estimate'],
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
                         marker=dict(color="#FFC107"),
                         text=dff1['Estimate'],
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

# Interaction: graph-1, with region-selection
@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('graph-1', 'figure'),
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



# Interaction: graph-2, with region-selection
@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('graph-2', 'figure'),
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
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by education", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

# Interaction: graph-3, with region-selection
@app.callback(
    # Output: change to graph-3
    dash.dependencies.Output('graph-3', 'figure'),
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

    # Donation rate data, filtered for selected region and demographic group (personal income category)
    # Corresponding name assigned
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (personal income category)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by personal income", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

# Interaction: graph-4, with region-selection and graph-4-demos
@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('graph-4', 'figure'),
    [
        # Inputs: selected region from region-selection and selected demographic group from graph-4-demos (dropdown menu)
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('graph-4-demos', 'value')
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
    dff1 = AvgTotNumDon_2018[AvgTotNumDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == demo]
    name1 = "Average number of annual donations"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == demo]
    name2 = "Average number of causes supported"

    # Format title according to dropdown input
    title = '{} \n by {}, {}'.format("Average number of causes supported and average number of donations annually", demo, region)

    # Uses external function with dataframes, names, and title set up above
    return num_don_num_causes(dff1, dff2, name1, name2, title)



if __name__ == '__main__':
    app.run_server(debug=True)
