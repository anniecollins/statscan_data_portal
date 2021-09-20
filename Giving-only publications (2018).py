import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read in data - CHANGE PATHWAY
SubSecAvgDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecAvgDon.csv")
SubSecAvgNumDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecAvgNumDon.csv")
SubSecDonRates_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecDonRates.csv")
DonRates_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-DonRate.csv")
AvgTotDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-AvgTotDon.csv")
AvgNumCauses_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-AvgNumCauses.csv")


# Combine all data into one long dataframe
# TODO: Need to update for multiple dataframes
df = pd.concat([SubSecAvgDon_2018, SubSecAvgNumDon_2018, SubSecDonRates_2018], ignore_index=True)

# Add annotation, suppress estimates/CI bounds where necessary
conditions = [df["Marker"] == "*",
              df["Marker"] == "...",
              pd.isnull(df["Marker"])]
values = ["Use with caution", "Estimate supressed", ""]
df["Annotation"] = np.select(conditions, values)
df["Estimate"] = np.where(df["Marker"]=="...", 0, df["Estimate"])
df["CI Upper"] = np.where(df["Marker"]=="...", 0, df["CI Upper"])


# Filter out non-demographic data
df = df[df["Group"] != "All"]

# Save versions with just Canada-level estimates
df_CA = df[df["Region"] == "CA"]
df_CAnoQC = df[df["Region"] == "CA (without QC)"]

# Save original version without Canada-level estimates
df = df[(df["Region"] != "CA") & (df["Region"] != "CA (without QC)")]

# Extract info from data for selection menus
region_names = df['Region'].unique()

# General app layout/set up
app.layout = html.Div([
    # TOP ROWS
    html.Div([
        # Page title
        html.H1('Giving-only publications')]),
    html.Div([
        dcc.Markdown('''
        Select a region of focus:
        '''
        )
    ]),
    html.Div([
        html.Div([
            # Left dropdown (regions)
            dcc.Dropdown(
                # Object id (used to reference object within callbacks)
                id='region-selection',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in region_names],
                # Default value, shows up at top of dropdown list
                value='ON'
            ),
        ],
        style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div([
        dcc.Markdown('''
        ## Who donates and how much do they give?
        
        ### Overall likelihood of donating and levels of support
        
        > INSERT TEXT
        ''')
    ], style={'marginTop': 20}
    ),
    html.Div(
        dcc.Markdown('''
        ### Demographic patterns of donating
        
        > INSERT TEXT
        '''), style={'width': '40%', 'height': 200, 'marginTop': 20}),
    # html.Div([
    #     # Graph object, with ID for use with below function implementation
    #     dcc.Graph(id='left-graph')
    # ],
    #     style={'width': '33%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20}),
    html.Div([
        dcc.Graph(id='left-graph')
        ],
        style={'width': '33%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20}),
    html.Div([
        # Graph object, with ID for use with below function implementation
        dcc.Graph(id='middle-graph')
    ],
        style={'width': '33%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20}),
    html.Div([
        # Graph object, with ID for use with below function implementation
        dcc.Graph(id='right-graph')
    ],
        style={'width': '33%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20})

])

# Function: create bar graph
def create_bar_graph(dff, CA_dff, CAnoQC_dff, title, region):

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

    # Add CA comparison
    # fig.add_trace(df[(df['Group']=='All') and (df['Region']=='CA')],
    #              x='Estimate',
    #              y='Attribute',
    #              orientation='h',
    #              marker_color="#FBC02D")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False)
    # fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #                    xref='paper', yref='paper', showarrow=False, align='left',
    #                    text=title)
    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

# Interaction: left graph
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('left-graph', 'figure'),
    [
    # ...according to input from top (page level) and left (graph level) drop downs
    # These represent the selections from each of the drop down menus, and are inputted into the following function as arguments in order of their appearance below
     dash.dependencies.Input('region-selection', 'value'),
     # dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     ])
def update_graph(region):
    # Specifically for age
    df = DonRates_2018
    df_CA = DonRates_2018[DonRates_2018["Region"] == "CA"]
    df_CAnoQC = DonRates_2018[DonRates_2018["Region"] == "CA (without QC)"]

    dff = df[df['Region'] == region]
    dff = dff[dff['Group'] == "Age group"]

    CA_dff = df_CA[df_CA['Group'] == "Age group"]

    CAnoQC_dff = df_CAnoQC[df_CAnoQC['Group'] == "Age group"]

    title = '{}, {}'.format("Donation rate by age", region)
    # Uses above function
    return create_bar_graph(dff, CA_dff, CAnoQC_dff, title, region)



# Interaction: middle graph
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('middle-graph', 'figure'),
    [
        # ...according to input from top (page level) and left (graph level) drop downs
        dash.dependencies.Input('region-selection', 'value'),
        # dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    ])
def update_graph(region):
    # Specifically for gender
    df = DonRates_2018
    df_CA = DonRates_2018[DonRates_2018["Region"] == "CA"]
    df_CAnoQC = DonRates_2018[DonRates_2018["Region"] == "CA (without QC)"]

    dff = df[df['Region'] == region]
    dff = dff[dff['Group'] == "Personal income category"]

    CA_dff = df_CA[df_CA['Group'] == "Personal income category"]

    CAnoQC_dff = df_CAnoQC[df_CAnoQC['Group'] == "Personal income category"]

    title = '{}, {}'.format("Donation rate by personal income", region)
    # Uses above function
    return create_bar_graph(dff, CA_dff, CAnoQC_dff, title, region)

# Interaction: right graph
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('right-graph', 'figure'),
    [
        # ...according to input from top (page level) and left (graph level) drop downs
        dash.dependencies.Input('region-selection', 'value'),
        # dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    ])
def update_graph(region):
    # Specifically for gender
    df = DonRates_2018
    df_CA = DonRates_2018[DonRates_2018["Region"] == "CA"]
    df_CAnoQC = DonRates_2018[DonRates_2018["Region"] == "CA (without QC)"]

    dff = df[df['Region'] == region]
    dff = dff[dff['Group'] == "Education"]

    CA_dff = df_CA[df_CA['Group'] == "Education"]

    CAnoQC_dff = df_CAnoQC[df_CAnoQC['Group'] == "Education"]

    title = '{}, {}'.format("Donation rate by education", region)
    # Uses above function
    return create_bar_graph(dff, CA_dff, CAnoQC_dff, title, region)



if __name__ == '__main__':
    app.run_server(debug=True)
