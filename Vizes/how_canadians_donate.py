import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import textwrap


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# DonMethAvgDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-DonMethAvgDon.csv")
DonMethAvgDon_2018 = pd.read_csv("Tables/2018-DonMethAvgDon.csv")
# DonMethDonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-DonMethDonRates.csv")
DonMethDonRates_2018 = pd.read_csv("Tables/2018-DonMethDonRates.csv")

DonMethDonRates_2018['Estimate'] = DonMethDonRates_2018['Estimate']*100
DonMethDonRates_2018['CI Upper'] = DonMethDonRates_2018['CI Upper']*100

data = [DonMethAvgDon_2018, DonMethDonRates_2018]

for i in range(len(data)):
    data[i]["Estimate"] = np.where(data[i]["Marker"]=="...", 0, data[i]["Estimate"])
    data[i]["CI Upper"] = np.where(data[i]["Marker"]=="...", 0, data[i]["CI Upper"])


    data[i]["Group"] = np.where(data[i]["Attribute"]=="Unable to determine", "", data[i]["Group"])
    data[i]["Group"] = np.where(data[i]["Attribute"]=="Unknown", "", data[i]["Group"])

    data[i]["Attribute"] = data[i]["Attribute"].str.wrap(15)
    data[i]["Attribute"] = data[i]["Attribute"].replace({'\n': '<br>'}, regex=True)

    data[i]['Estimate'] = data[i]['Estimate'].round(0).astype(int)
    data[i]["CI Upper"] = data[i]["CI Upper"].round(0).astype(int)
    data[i]['cv'] = data[i]['cv'].round(2)

region_values = np.array(['CA', 'BC', 'AB', 'PR', 'ON', 'QC', 'AT'], dtype=object)
region_names = np.array(['Canada',
                         'British Columbia',
                         'Alberta',
                         'Prairie Provinces (SK, MB)',
                         'Ontario',
                         'Quebec',
                         'Atlantic Provinces (NB, NS, PE, NL)'], dtype=str)

method_names = DonMethAvgDon_2018["QuestionText"].unique()

app.layout = html.Div([
    html.Div([
        html.H1('How do Canadians donate?')]),
    html.Div([
        html.Div(["Select a region of focus:",
                  dcc.Dropdown(
                      id='region-selection',
                      options=[{'label': region_names[i], 'value': region_values[i]} for i in range(len(region_values))],
                      value='CA',
                      style={'verticalAlgin': 'middle'}
                  ),
                  ],
                 style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div([
        html.Div(["Select a method of focus:",
                  dcc.Dropdown(
                      id='method-selection',
                      options=[{'label': i, 'value': i} for i in method_names],
                      value='At work',
                      style={'verticalAlgin': 'middle'}
                  ),
                  ],
                 style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div([
        dcc.Graph(id='DonMethDonRateAvgDonAmt-Method', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-Gndr', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-Age', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-Educ', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-Inc', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-Relig', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-MarStat', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-Labour', style={'marginTop': 50}),
        dcc.Graph(id='DonMethDonRateAvgDonAmt-ImmStat', style={'marginTop': 50})
    ],
        style={'width': '50%', 'display': 'inline-block', "marginTop": 20}),
])

def don_rate_avg_don_by_meth(dff1, dff2, name1, name2, title):
    dff1['Text'] = np.select([dff1["Marker"] == "*", dff1["Marker"] == "...", pd.isnull(dff1["Marker"])],
                             [dff1.Estimate.map(str)+"%"+"*", "...", dff1.Estimate.map(str)+"%"])
    dff1['HoverText'] = np.select([dff1["Marker"] == "*",
                                   dff1["Marker"] == "...",
                                   pd.isnull(dff1["Marker"])],
                                  ["Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%"])
    dff2['Text'] = np.select([dff2["Marker"] == "*", dff2["Marker"] == "...", pd.isnull(dff2["Marker"])],
                             ["$"+dff2.Estimate.map(str)+"*", "...", "$"+dff2.Estimate.map(str)])
    dff2['HoverText'] = np.select([dff2["Marker"] == "*",
                                   dff2["Marker"] == "...",
                                   pd.isnull(dff2["Marker"])],
                                  ["Estimate: $"+dff2.Estimate.map(str)+" ± $"+(dff2["CI Upper"] - dff2["Estimate"]).map(str)+"<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: $"+dff2.Estimate.map(str)+" ± $"+(dff2["CI Upper"] - dff2["Estimate"]).map(str)])
    dff1 = dff1[(dff1.Attribute != "Unknown")]
    dff1 = dff1[(dff1.Attribute != "Unable to<br>determine")]
    dff2 = dff2[(dff2.Attribute != "Unknown")]
    dff2 = dff2[(dff2.Attribute != "Unable to<br>determine")]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff1['CI Upper'],
                         y=dff1['QuestionText'],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         text=None,
                         hoverinfo="skip",
                         textposition='outside',
                         showlegend=False,
                         cliponaxis=False,
                         xaxis='x2',
                         offsetgroup=2
                         ),
                  )
    fig.add_trace(go.Bar(x=dff2['CI Upper'],
                         y=dff2['QuestionText'],
                         orientation="h",
                         error_x=None, # need to vectorize subtraction
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         text=None,
                         hoverinfo="skip",
                         textposition='outside',
                         showlegend=False,
                         cliponaxis=False,
                         xaxis='x1',
                         offsetgroup=1
                         ),
                  )

    fig.add_trace(go.Bar(x=dff1['Estimate'],
                         y=dff1['QuestionText'],
                         orientation="h",
                         error_x=None,
                         hovertext=dff1['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         hoverinfo="text",
                         marker=dict(color="#c8102e"),
                         text=dff1['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         insidetextanchor=None,
                         name=name1,
                         xaxis='x2',
                         offsetgroup=2
                         ),
                  )
    fig.add_trace(go.Bar(x=dff2['Estimate'],
                         y=dff2['QuestionText'],
                         orientation="h",
                         error_x=None, # need to vectorize subtraction
                         hovertext =dff2['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         marker=dict(color="#7BAFD4"),
                         text=dff2['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         insidetextanchor= None,
                         name=name2,
                         xaxis='x1',
                         offsetgroup=1
                         ),
                  )

    x2 = go.layout.XAxis(overlaying='x',
                         side='bottom',
                         autorange = False,
                         range = [0, 1.25*max(dff1["CI Upper"])])
    x1 = go.layout.XAxis(overlaying='x',
                         side='top',
                         autorange = False,
                         range = [0, 1.25*max(dff2["CI Upper"])])

    fig.update_layout(title={'text': title,
                             'y': 0.95},
                      margin={'l': 30, 'b': 30, 'r': 10, 't': 30},
                      height=600,
                      bargroupgap=0.05,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      barmode="group",
                      xaxis1=x1,
                      xaxis2=x2,
                      legend={'orientation': 'h', 'yanchor': "bottom"},
                      updatemenus=[
                          dict(
                              type = "buttons",
                              xanchor='right',
                              x = 1.2,
                              y = 0.5,
                              buttons=list([
                                  dict(
                                      args=[{"error_x": [None, None, None, None],
                                             "text": [None, None, dff1['Text'], dff2['Text']]}],
                                      label="Reset",
                                      method="restyle"
                                  ),
                                  dict(
                                      args=[{"error_x": [None, None, dict(type="data", array=dff1["CI Upper"]-dff1["Estimate"], color="#424242", thickness=1.5), dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"], color="#424242", thickness=1.5)],
                                             "text": [dff1['Text'], dff2['Text'], None, None]}],
                                      label="Confidence Intervals",
                                      method="restyle"
                                  )
                              ]),
                          ),
                      ]
                      )
    fig.update_xaxes(showgrid=False,
                     showticklabels=False,
                     autorange = False,
                     )
    fig.update_yaxes(autorange="reversed",
                     ticklabelposition="outside top",
                     tickfont=dict(size=12),
                     categoryorder='array',
                     categoryarray=dff1.sort_values(by="Estimate", ascending=False)["QuestionText"])

    markers = pd.concat([dff1["Marker"], dff2["Marker"]])
    if markers.isin(["*"]).any() and markers.isin(["..."]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.31, x=1.2, align="left", showarrow=False),
                                       dict(text="*<i>Use with caution<br>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.08, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    elif markers.isin(["*"]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.31, x=1.2, align="left", showarrow=False),
                                       dict(text="*<i>Use with caution</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.08, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    elif markers.isin(["..."]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.31, x=1.2, align="left", showarrow=False),
                                       dict(text="<i>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.08, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    else:
        fig.update_layout(margin={'l': 30, 'b': 30, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.32, x=1.2, align="left", showarrow=False)])

    return fig


def don_rate_avg_don(dff1, dff2, name1, name2, title):
    dff1['Text'] = np.select([dff1["Marker"] == "*", dff1["Marker"] == "...", pd.isnull(dff1["Marker"])],
                             [dff1.Estimate.map(str)+"%"+"*", "...", dff1.Estimate.map(str)+"%"])
    dff1['HoverText'] = np.select([dff1["Marker"] == "*",
                                   dff1["Marker"] == "...",
                                   pd.isnull(dff1["Marker"])],
                                  ["Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%"])
    dff2['Text'] = np.select([dff2["Marker"] == "*", dff2["Marker"] == "...", pd.isnull(dff2["Marker"])],
                             ["$"+dff2.Estimate.map(str)+"*", "...", "$"+dff2.Estimate.map(str)])
    dff2['HoverText'] = np.select([dff2["Marker"] == "*",
                                   dff2["Marker"] == "...",
                                   pd.isnull(dff2["Marker"])],
                                  ["Estimate: $"+dff2.Estimate.map(str)+" ± $"+(dff2["CI Upper"] - dff2["Estimate"]).map(str)+"<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: $"+dff2.Estimate.map(str)+" ± $"+(dff2["CI Upper"] - dff2["Estimate"]).map(str)])
    dff1 = dff1[(dff1.Attribute != "Unknown") & (dff1.Attribute != "Unable to determine")]
    dff2 = dff2[(dff2.Attribute != "Unknown") & (dff2.Attribute != "Unable to determine")]

    # Scatter plot - data frame, x label, y label
    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff1['CI Upper'],
                         y=dff1['Attribute'],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         text=None,
                         hoverinfo="skip",
                         textposition='outside',
                         showlegend=False,
                         cliponaxis=False,
                         xaxis='x2',
                         offsetgroup=2
                         ),
                  )
    fig.add_trace(go.Bar(x=dff2['CI Upper'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=None, # need to vectorize subtraction
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         text=None,
                         hoverinfo="skip",
                         textposition='outside',
                         showlegend=False,
                         cliponaxis=False,
                         xaxis='x1',
                         offsetgroup=1
                         ),
                  )

    fig.add_trace(go.Bar(x=dff1['Estimate'],
                         y=dff1['Attribute'],
                         orientation="h",
                         error_x=None,
                         hovertext=dff1['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         hoverinfo="text",
                         marker=dict(color="#c8102e"),
                         text=dff1['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         insidetextanchor=None,
                         name=name1,
                         xaxis='x2',
                         offsetgroup=2
                         ),
                  )
    fig.add_trace(go.Bar(x=dff2['Estimate'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=None, # need to vectorize subtraction
                         hovertext =dff2['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         marker=dict(color="#7BAFD4"),
                         text=dff2['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         insidetextanchor= None,
                         name=name2,
                         xaxis='x1',
                         offsetgroup=1
                         ),
                  )

    x2 = go.layout.XAxis(overlaying='x',
                         side='bottom',
                         autorange = False,
                         range = [0, 1.25*max(dff1["CI Upper"])])
    x1 = go.layout.XAxis(overlaying='x',
                         side='top',
                         autorange = False,
                         range = [0, 1.25*max(dff2["CI Upper"])])

    fig.update_layout(title={'text': title,
                             'y': 0.95},
                      margin={'l': 30, 'b': 30, 'r': 10, 't': 30},
                      height=400,
                      bargroupgap=0.05,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      barmode="group",
                      xaxis1=x1,
                      xaxis2=x2,
                      legend={'orientation': 'h', 'yanchor': "bottom"},
                      updatemenus=[
                          dict(
                              type = "buttons",
                              xanchor='right',
                              x = 1.2,
                              y = 0.5,
                              buttons=list([
                                  dict(
                                      args=[{"error_x": [None, None, None, None],
                                             "text": [None, None, dff1['Text'], dff2['Text']]}],
                                      label="Reset",
                                      method="restyle"
                                  ),
                                  dict(
                                      args=[{"error_x": [None, None, dict(type="data", array=dff1["CI Upper"]-dff1["Estimate"], color="#424242", thickness=1.5), dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"], color="#424242", thickness=1.5)],
                                             "text": [dff1['Text'], dff2['Text'], None, None]}],
                                      label="Confidence Intervals",
                                      method="restyle"
                                  )
                              ]),
                          ),
                      ]
                      )
    fig.update_xaxes(showgrid=False,
                     showticklabels=False,
                     autorange = False,
                     )
    fig.update_yaxes(autorange="reversed",
                     ticklabelposition="outside top",
                     tickfont=dict(size=12))

    markers = pd.concat([dff1["Marker"], dff2["Marker"]])
    if markers.isin(["*"]).any() and markers.isin(["..."]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.2, align="left", showarrow=False),
                                       dict(text="*<i>Use with caution<br>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    elif markers.isin(["*"]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.2, align="left", showarrow=False),
                                       dict(text="*<i>Use with caution</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    elif markers.isin(["..."]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.2, align="left", showarrow=False),
                                       dict(text="<i>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    else:
        fig.update_layout(margin={'l': 30, 'b': 30, 'r': 10, 't': 40},
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.22, x=1.2, align="left", showarrow=False)])

    return fig

@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-Method', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])

def update_graph(region):

    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "All"]
    name1 = "% donating"

    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "All"]
    name2 = "Average amount"

    title = '{}, {}'.format("Donation rate & average donation amount by method", region)

    return don_rate_avg_don_by_meth(dff1, dff2, name1, name2, title)

@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-Age', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):

    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by age group", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-Gndr', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):
    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by gender", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('DonMethDonRateAvgDonAmt-MarStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):
    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by marital status", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-Educ', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):
    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by education", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)


@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-Labour', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):
    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by employment status", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-Relig', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):
    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by religious attendance", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-Inc', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):
    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by income", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(

    dash.dependencies.Output('DonMethDonRateAvgDonAmt-ImmStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('method-selection', 'value')
    ])
def update_graph(region, method):
    dff1 = DonMethDonRates_2018[DonMethDonRates_2018['Region'] == region]
    dff1 = dff1[dff1['QuestionText'] == method]
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "% donating"


    dff2 = DonMethAvgDon_2018[DonMethAvgDon_2018['Region'] == region]
    dff2 = dff2[dff2['QuestionText'] == method]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Average amount"


    title = '{}, {}'.format("Donation rate & average donation amount per method by immigration status", region)


    return don_rate_avg_don(dff1, dff2, name1, name2, title)

if __name__ == '__main__':
    app.run_server(debug=True)
