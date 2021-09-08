import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read in data - CHANGE PATHWAY
SubSecAvgDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecAvgDon.csv")
SubSecAvgNumDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecAvgNumDon.csv")
SubSecAvgDon_2013 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2013-SubSecAvgDon.csv")
SubSecAvgNumDon_2013 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2013-SubSecAvgNumDon.csv")

# Combine all data into one long dataframe
# TODO: Need to update for multiple dataframes
df = SubSecAvgDon_2018.append(SubSecAvgNumDon_2018)
df = df.append(SubSecAvgDon_2013)
df = df.append(SubSecAvgNumDon_2013)

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
available_demographics = df['Group'].unique()
region_names = df['Region'].unique()
sector_names = df['QuestionText'].unique()
dataset_names = df['QuestionGroup'].unique()
years = df['Year'].unique()

# General app layout/set up
app.layout = html.Div([
    # TOP ROWS
    html.Div([
        # Page title
        html.H1('Sub-Sectoral Giving Patterns')]),
    html.Center([
        html.Center([
            dcc.Dropdown(
                id='year-selection',
                options=[{'label': i, 'value': i} for i in years],
                value=2018
            )])
    ], style={'width': '49%', 'display': 'inline-block'}),
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
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            # Right drop down (sector)
            dcc.Dropdown(
                # Object id (used to reference object within callbacks)
                id='sector-selection',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in sector_names],
                # Default value, shows up at top of dropdown list
                value='Health'
            ),
        ],
            style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            # Right drop down (sector)
            dcc.Dropdown(
                # Object id (used to reference object within callbacks)
                id='crossfilter-xaxis-column',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in available_demographics],
                # Default value, shows up at top of dropdown list
                value='Age group'
            ),
        ],
            style={'width': '33%', 'display': 'inline-block'}),
    ]),

    # Second row: graph-specific dropdowns
    html.Div([
        html.Div(dcc.Dropdown(
            # Object id (used to reference object within callbacks)
            id='left-dataset-selection',
            # Dropdown menu options
            options=[{'label': i, 'value': i} for i in dataset_names],
            # Default value, shows up at top of dropdown list
            value='Average donation by subsector'
        ), style={'width': '49%', 'display': 'inline-block'}
        ),
        html.Div(dcc.Dropdown(
            # Object id (used to reference object within callbacks)
            id='right-dataset-selection',
            # Dropdown menu options
            options=[{'label': i, 'value': i} for i in dataset_names],
            # Default value, shows up at top of dropdown list
            value='Average number of donation by subsector'
        ), style={'width': '49%', 'display': 'inline-block'})
    ], style={"marginTop": 40}
    ),

    # Third row: graphs
    html.Div([
        # Graph object, with ID for use with below function implementation
        dcc.Graph(id='left-graph')
    ],
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20}),
    html.Div([
        # Graph object, with ID for use with below function implementation
        dcc.Graph(id='right-graph')
    ],
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20} )

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

# Interaction
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('left-graph', 'figure'),
    [
    # ...according to input from top (page level) and left (graph level) drop downs
    # These represent the selections from each of the drop down menus, and are inputted into the following function as arguments in order of their appearance below
     dash.dependencies.Input('year-selection', 'value'),
     dash.dependencies.Input('region-selection', 'value'),
     dash.dependencies.Input('sector-selection', 'value'),
     dash.dependencies.Input('left-dataset-selection', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     ])
def update_graph(year, region, sector, dataset, xaxis_column_name):
    dff = df[df['Region'] == region]
    dff = dff[dff['Year'] == year]
    dff = dff[dff['QuestionText'] == sector]
    dff = dff[dff['QuestionGroup'] == dataset]
    dff = dff[dff['Group'] == xaxis_column_name]

    CA_dff = df_CA[df_CA['QuestionText'] == sector]
    CA_dff = CA_dff[CA_dff['Year'] == year]
    CA_dff = CA_dff[CA_dff['QuestionGroup'] == dataset]
    CA_dff = CA_dff[CA_dff['Group'] == xaxis_column_name]

    CAnoQC_dff = df_CAnoQC[df_CAnoQC['QuestionText'] == sector]
    CAnoQC_dff = CAnoQC_dff[CAnoQC_dff['Year'] == year]
    CAnoQC_dff = CAnoQC_dff[CAnoQC_dff['QuestionGroup'] == dataset]
    CAnoQC_dff = CAnoQC_dff[CAnoQC_dff['Group'] == xaxis_column_name]

    title = '<b>{}</b>: {}, {}'.format(sector, xaxis_column_name, region)
    # Uses above function
    return create_bar_graph(dff, CA_dff, CAnoQC_dff, title, region)



# Interaction
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('right-graph', 'figure'),
    [
        # ...according to input from top (page level) and left (graph level) drop downs
        dash.dependencies.Input('year-selection', 'value'),
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('sector-selection', 'value'),
        dash.dependencies.Input('right-dataset-selection', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    ])
def update_graph(year, region, sector, dataset, xaxis_column_name):
    dff = df[df['Region'] == region]
    dff = dff[dff['Year'] == year]
    dff = dff[dff['QuestionText'] == sector]
    dff = dff[dff['QuestionGroup'] == dataset]
    dff = dff[dff['Group'] == xaxis_column_name]

    CA_dff = df_CA[df_CA['QuestionText'] == sector]
    CA_dff = CA_dff[CA_dff['Year'] == year]
    CA_dff = CA_dff[CA_dff['QuestionGroup'] == dataset]
    CA_dff = CA_dff[CA_dff['Group'] == xaxis_column_name]

    CAnoQC_dff = df_CAnoQC[df_CAnoQC['QuestionText'] == sector]
    CAnoQC_dff = CAnoQC_dff[CAnoQC_dff['Year'] == year]
    CAnoQC_dff = CAnoQC_dff[CAnoQC_dff['QuestionGroup'] == dataset]
    CAnoQC_dff = CAnoQC_dff[CAnoQC_dff['Group'] == xaxis_column_name]

    title = '<b>{}</b>: {}, {}'.format(sector, xaxis_column_name, region)
    # Uses above function
    return create_bar_graph(dff, CA_dff, CAnoQC_dff, title, region)



if __name__ == '__main__':
    app.run_server(debug=True)
