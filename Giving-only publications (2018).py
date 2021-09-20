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

# Read in data - CHANGE PATHWAY
SubSecAvgDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecAvgDon.csv")
SubSecAvgNumDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecAvgNumDon.csv")
SubSecDonRates_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-SubSecDonRates.csv")
DonRates_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-DonRate.csv")
AvgTotDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-AvgTotDon.csv")
AvgNumCauses_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-AvgNumCauses.csv")
AvgTotNumDon_2018 = pd.read_csv("~/PycharmProjects/statscan_data_portal_1/Tables copy/2018-AvgTotNumDon.csv")
data = [SubSecAvgDon_2018, SubSecDonRates_2018, DonRates_2018, AvgTotDon_2018]
data_num = [SubSecAvgNumDon_2018, AvgNumCauses_2018, AvgTotNumDon_2018]

# Format as percentage
DonRates_2018['Estimate'] = DonRates_2018['Estimate']*100
DonRates_2018['CI Upper'] = DonRates_2018['CI Upper']*100

# # Add annotation, suppress estimates/CI bounds where necessary
values = ["Use with caution", "Estimate supressed", ""]
i = 0
while i < len(data):
    conditions = [data[i]["Marker"] == "*",
                  data[i]["Marker"] == "...",
                pd.isnull(data[i]["Marker"])]
    data[i]["Annotation"] = np.select(conditions, values)

    data[i]["Estimate"] = np.where(data[i]["Marker"]=="...", 0, data[i]["Estimate"])
    data[i]["CI Upper"] = np.where(data[i]["Marker"]=="...", 0, data[i]["CI Upper"])

    data[i]['Estimate'] = data[i]['Estimate'].round(0)
    data[i]["CI Upper"] = data[i]["CI Upper"].round(0)
    i = i + 1

i = 0
while i < len(data_num):
    conditions = [data_num[i]["Marker"] == "*",
                  data_num[i]["Marker"] == "...",
                  pd.isnull(data_num[i]["Marker"])]
    data_num[i]["Annotation"] = np.select(conditions, values)

    data_num[i]["Estimate"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["Estimate"])
    data_num[i]["CI Upper"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["CI Upper"])

    data_num[i]['Estimate'] = data_num[i]['Estimate'].round(2)
    data_num[i]["CI Upper"] = data_num[i]["CI Upper"].round(2)
    i = i + 1

# # Extract info from data for selection menus
region_names = SubSecAvgDon_2018['Region'].unique()
demo_names = SubSecAvgDon_2018['Group'].unique()
# Remove "All"
demo_names = np.delete(demo_names, 0)

# General app layout/set up
app.layout = html.Div([
    # TOP ROWS
    html.Center([
        # Page title
        html.H1('Giving-only publications')]),
    html.Center([
        html.Center(["Select a region of focus:",
            # Left dropdown (regions)
            dcc.Dropdown(
                # Object id (used to reference object within callbacks)
                id='region-selection',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in region_names],
                # Default value, shows up at top of dropdown list
                value='ON',
                style={'verticalAlgin': 'middle'}
            ),
        ],
        style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div(
        dcc.Markdown('''
        ## Who donates and how much do they give?
        
        ### Overall likelihood of donating and levels of support
        
        ### Demographic patterns of donating
        
        ### Breadth and focus of support
        
        Canadians with higher household incomes were
        more likely to donate and more likely to give
        larger annual donations than those with lower
        household incomes.
        Eighty-six percent of Canadians with household
        incomes of $100,000 or more were donors, as
        were 87% of those with household incomes
        between $80,000 and $99,999. As household
        income decreased, so did the percentage of those
        making donations.
        Those with household incomes of $100,000 or
        more made the largest average annual donation —
        $529, down from $608 in 1997. Average annual
        donations decreased steadily as household
        incomes decreased.
        
        '''), style={'width': '50%', 'height': 1200, 'marginTop': 20, 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='graph-1', style={'marginTop': 50}),
        dcc.Graph(id='graph-2', style={'marginTop': 50}),
        dcc.Graph(id='graph-3', style={'marginTop': 50}),
        html.Div([
            "Choose demographic feature to display below: ",
            dcc.Dropdown(id='graph-4-demos',
                         options=[{'label': i, 'value': i} for i in demo_names],
                         value="Age group")
            ], style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
        dcc.Graph(id='graph-4')
        ],
        style={'width': '40%', 'display': 'inline-block', 'height': 1200, "marginTop": 20}),
    # html.Div([
    #     # Graph object, with ID for use with below function implementation
    #     dcc.Graph(id='middle-graph')
    # ],
    #     style={'width': '49%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20}),
    # html.Div([
    #     # Graph object, with ID for use with below function implementation
    #     dcc.Graph(id='right-graph')
    # ],
    #     style={'width': '49%', 'display': 'inline-block', 'padding': '0 100', "marginTop": 20})

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

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False)
    # fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #                    xref='paper', yref='paper', showarrow=False, align='left',
    #                    text=title)
    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

def don_rate_avg_don(dff1, dff2, name1, name2, title):

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

    # Add CA comparison
    # fig.add_trace(df[(df['Group']=='All') and (df['Region']=='CA')],
    #              x='Estimate',
    #              y='Attribute',
    #              orientation='h',
    #              marker_color="#FBC02D")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False, showticklabels=False)
    # fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #                    xref='paper', yref='paper', showarrow=False, align='left',
    #                    text=title)
    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

def num_don_num_causes(dff1, dff2, name1, name2, title):

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

    # Add CA comparison
    # fig.add_trace(df[(df['Group']=='All') and (df['Region']=='CA')],
    #              x='Estimate',
    #              y='Attribute',
    #              orientation='h',
    #              marker_color="#FBC02D")

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False, showticklabels=False)
    # fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #                    xref='paper', yref='paper', showarrow=False, align='left',
    #                    text=title)
    fig.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig

# Interaction: left graph
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('graph-1', 'figure'),
    [
    # ...according to input from top (page level) and left (graph level) drop downs
    # These represent the selections from each of the drop down menus, and are inputted into the following function as arguments in order of their appearance below
     dash.dependencies.Input('region-selection', 'value'),
     # dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     ])
def update_graph(region):

    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by age group", region)
    # Uses above function
    return don_rate_avg_don(dff1, dff2, name1, name2, title)



# Interaction: middle graph
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('graph-2', 'figure'),
    [
        # ...according to input from top (page level) and left (graph level) drop downs
        dash.dependencies.Input('region-selection', 'value'),
        # dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    ])
def update_graph(region):

    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by education", region)
    # Uses above function
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

# Interaction: right graph
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('graph-3', 'figure'),
    [
        # ...according to input from top (page level) and left (graph level) drop downs
        dash.dependencies.Input('region-selection', 'value'),
        # dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    ])
def update_graph(region):

    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by personal income", region)
    # Uses above function
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    # Changes left graph...
    dash.dependencies.Output('graph-4', 'figure'),
    [
        # ...according to input from top (page level) and left (graph level) drop downs
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
    # Uses above function
    return num_don_num_causes(dff1, dff2, name1, name2, title)



if __name__ == '__main__':
    app.run_server(debug=True)
