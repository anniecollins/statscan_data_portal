import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import textwrap


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

TopDonorsMotivations_2018 = pd.read_csv("../Tables/2018-TopDonorsMotivationsForGiving.csv")
TopDonorsBarriers_2018 = pd.read_csv("../Tables/2018-TopDonorsBarriersToGiving.csv")
TopDonorsPercTotDonations_2018 = pd.read_csv("../Tables/2018-TopDonorsPercTotDonations.csv")
TopDonorsPercTotDonors_2018 = pd.read_csv("../Tables/2018-TopDonorsPercTotDonors.csv")
TopDonorsDonRates_2018 = pd.read_csv("../Tables/2018-TopDonorsDonRates.csv")
TopDonorsDemoLikelihoods = pd.read_csv("../Tables/2018-TopDonorsDemoLikelihoods.csv")

TopDonorsMotivations_2018['Estimate'] = TopDonorsMotivations_2018['Estimate']*100
TopDonorsMotivations_2018['CI Upper'] = TopDonorsMotivations_2018['CI Upper']*100
TopDonorsBarriers_2018['Estimate'] = TopDonorsBarriers_2018['Estimate']*100
TopDonorsBarriers_2018['CI Upper'] = TopDonorsBarriers_2018['CI Upper']*100
TopDonorsPercTotDonations_2018['Estimate'] = TopDonorsPercTotDonations_2018['Estimate']*100
TopDonorsPercTotDonations_2018['CI Upper'] = TopDonorsPercTotDonations_2018['CI Upper']*100
TopDonorsPercTotDonors_2018['Estimate'] = TopDonorsPercTotDonors_2018['Estimate']*100
TopDonorsPercTotDonors_2018['CI Upper'] = TopDonorsPercTotDonors_2018['CI Upper']*100
TopDonorsDonRates_2018['Estimate'] = TopDonorsDonRates_2018['Estimate']*100
TopDonorsDonRates_2018['CI Upper'] = TopDonorsDonRates_2018['CI Upper']*100
TopDonorsDemoLikelihoods['Estimate'] = TopDonorsDemoLikelihoods['Estimate']*100
TopDonorsDemoLikelihoods['CI Upper'] = TopDonorsDemoLikelihoods['CI Upper']*100

data = [TopDonorsMotivations_2018, TopDonorsBarriers_2018, TopDonorsPercTotDonations_2018, TopDonorsPercTotDonors_2018, TopDonorsDonRates_2018, TopDonorsDemoLikelihoods]

for i in range(len(data)):
    data[i]["Estimate"] = np.where(data[i]["Marker"]=="...", 0, data[i]["Estimate"])
    data[i]["CI Upper"] = np.where(data[i]["Marker"]=="...", 0, data[i]["CI Upper"])

    data[i]["Group"] = np.where(data[i]["Attribute"]=="Unable to determine", "", data[i]["Group"])
    data[i]["Group"] = np.where(data[i]["Attribute"]=="Unknown", "", data[i]["Group"])

    data[i]["Attribute"] = data[i]["Attribute"].str.wrap(15)
    data[i]["Attribute"] = data[i]["Attribute"].replace({'\n': '<br>'}, regex=True)

    data[i]["QuestionText"] = data[i]["QuestionText"].str.wrap(20)
    data[i]["QuestionText"] = data[i]["QuestionText"].replace({'\n': '<br>'}, regex=True)

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

demo_names = TopDonorsDemoLikelihoods["Group"].unique()

app.layout = html.Div([
    html.Div([
        html.H1('Understanding Top Donors')]),
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
        dcc.Graph(id='TopDonorsTotalDonations', style={'marginTop': 50}),
        html.Div([
            "Choose demographic feature to display below: ",
            dcc.Dropdown(id='demo-selection',
                         options=[{'label': i, 'value': i} for i in demo_names],
                         value="Personal income category")
        ], style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
        dcc.Graph(id='TopDonorsDemographics', style={'marginTop': 50}),
        dcc.Graph(id='TopDonorsSubSecSupport', style={'marginTop': 50}),
        dcc.Graph(id='TopDonorsMotivations', style={'marginTop': 50}),
        dcc.Graph(id='TopDonorsBarriers', style={'marginTop': 50})
    ],
        style={'width': '50%', 'display': 'inline-block', "marginTop": 20}),
])

def dist_total_donations(dff1, dff2, name1, name2, title):
    dff1['Text'] = np.select([dff1["Marker"] == "*", dff1["Marker"] == "...", pd.isnull(dff1["Marker"])],
                                [dff1.Estimate.map(str)+"%"+"*", "...", dff1.Estimate.map(str)+"%"])
    dff1['HoverText'] = np.select([dff1["Marker"] == "*",
                                      dff1["Marker"] == "...",
                                      pd.isnull(dff1["Marker"])],
                                     ["Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                      "Estimate Suppressed",
                                      "Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%"])

    dff2['Text'] = np.select([dff2["Marker"] == "*", dff2["Marker"] == "...", pd.isnull(dff2["Marker"])],
                             [dff2.Estimate.map(str)+"%"+"*", "...", dff2.Estimate.map(str)+"%"])
    dff2['HoverText'] = np.select([dff2["Marker"] == "*",
                                   dff2["Marker"] == "...",
                               pd.isnull(dff2["Marker"])],
                              ["Estimate: "+dff2.Estimate.map(str)+"% ± "+(dff2["CI Upper"] - dff2["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                               "Estimate Suppressed",
                               "Estimate: "+dff2.Estimate.map(str)+"% ± "+(dff2["CI Upper"] - dff2["Estimate"]).map(str)+"%"])
    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff2['Attribute'],
                          y=dff2['CI Upper'],
                          marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                          text=None,
                          textposition='outside',
                          showlegend=False,
                          hoverinfo="skip",
                          cliponaxis=False,
                          offsetgroup=1,
                          ),
                   )

    fig.add_trace(go.Bar(x=dff1['Attribute'],
                          y=dff1['CI Upper'],
                          marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                          text=None,
                          textposition='outside',
                          hoverinfo="skip",
                          showlegend=False,
                          name=name1,
                          offsetgroup=2,
                          ),
                   )

    fig.add_trace(go.Bar(x=dff2['Attribute'],
                          y=dff2['Estimate'],
                          error_y=None,
                          hovertext =dff2['HoverText'],
                          hovertemplate="%{hovertext}",
                          hoverlabel=dict(font=dict(color="white")),
                          hoverinfo="text",
                          marker=dict(color="#c8102e"),
                         text=dff2['Text'],
                          textposition='outside',
                          cliponaxis=False,
                          name=name2,
                          offsetgroup=1
                          ),
                   )

    fig.add_trace(go.Bar(x=dff1['Attribute'],
                          y=dff1['Estimate'],
                          error_y=None,
                          hovertext=dff1['HoverText'],
                          hovertemplate="%{hovertext}",
                          hoverlabel=dict(font=dict(color="white")),
                          hoverinfo="text",
                          marker=dict(color="#7BAFD4"),
                          text=dff1['Text'],
                          textposition='outside',
                          cliponaxis=False,
                          name=name1,
                          offsetgroup=2
                          ),
                   )

    fig.update_layout(title={'text': title,
                              'y': 0.99},
                       margin={'l': 30, 'b': 30, 'r': 10, 't': 10},
                       plot_bgcolor='rgba(0, 0, 0, 0)',
                       barmode="group",
                       bargroupgap=0.05,
                       legend={'orientation': 'h', 'yanchor': "bottom", 'xanchor': 'center', 'x': 0.5, 'y': -0.2},
                       height=400,
                       updatemenus=[
                           dict(
                               type = "buttons",
                               xanchor='right',
                               x = 1.4,
                               y = 0.5,
                               buttons=list([
                                   dict(
                                       args=[{"error_y": [None, None, None, None],
                                              "text": [None, None, dff2['Text'], dff1['Text']],
                                              }],
                                       label="Reset",
                                       method="restyle"
                                   ),
                                   dict(
                                       args=[{"error_y": [None, None, dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"], color="#424242", thickness=1.5), dict(type="data", array=dff1["CI Upper"]-dff1["Estimate"], color="#424242", thickness=1.5)],
                                              "text": [dff2['Text'], dff1['Text'], None, None],
                                              }],
                                       label="Confidence Intervals",
                                       method="restyle"
                                   )
                               ]),
                           ),
                       ])

    fig.update_xaxes(tickfont=dict(size=12))
    fig.update_yaxes(showgrid=False,
                      showticklabels=False)

    markers = pd.concat([dff1["Marker"], dff2["Marker"]])
    if markers.isin(["*"]).any() and markers.isin(["..."]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                           annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.4, align="left", showarrow=False),
                                        dict(text="*<i>Use with caution<br>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    elif markers.isin(["*"]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                           annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.4, align="left", showarrow=False),
                                        dict(text="*<i>Use with caution</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    elif markers.isin(["..."]).any():
        fig.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                           annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.4, align="left", showarrow=False),
                                        dict(text="<i>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
    else:
        fig.update_layout(margin={'l': 30, 'b': 30, 'r': 10, 't': 40},
                           annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.2, x=1.4, align="left", showarrow=False)])

    return fig

def vertical_percentage_graph(dff, title):
    dff['Text'] = np.select([dff["Marker"] == "*", dff["Marker"] == "...", pd.isnull(dff["Marker"])],
                             [dff.Estimate.map(str)+"%"+"*", "...", dff.Estimate.map(str)+"%"])
    dff['HoverText'] = np.select([dff["Marker"] == "*",
                                   dff["Marker"] == "...",
                                   pd.isnull(dff["Marker"])],
                                  ["Estimate: "+dff.Estimate.map(str)+"% ± "+(dff["CI Upper"] - dff["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: "+dff.Estimate.map(str)+"% ± "+(dff["CI Upper"] - dff["Estimate"]).map(str)+"%"])

    dff1 = dff[dff['Attribute'] == "Top donor"]
    name1 = "Top donors"

    dff2 = dff[dff['Attribute'] == "Regular donor"]
    name2 = "Regular donors"

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff1['CI Upper'],
                         y=dff1['QuestionText'],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         showlegend=False,
                         hoverinfo="skip",
                         text=None,
                         textposition="outside",
                         cliponaxis=False,
                         offsetgroup=2
                         ),
                  )

    fig.add_trace(go.Bar(x=dff2['CI Upper'],
                         y=dff2['QuestionText'],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         showlegend=False,
                         hoverinfo="skip",
                         text=None,
                         textposition="outside",
                         cliponaxis=False,
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
                         name=name1,
                         offsetgroup=2
                         ),
                  )

    fig.add_trace(go.Bar(x=dff2['Estimate'],
                         y=dff2['QuestionText'],
                         orientation="h",
                         error_x=None,
                         hovertext =dff2['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         hoverinfo="text",
                         marker=dict(color="#7BAFD4"),
                         text=dff2['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         name=name2,
                         offsetgroup=1
                         ),
                  )

    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin={'l': 30, 'b': 30, 'r': 10, 't': 10},
                      height=600,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      bargroupgap=0.05,
                      barmode="group",
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
                     range = [0, 1.25*max(np.concatenate([dff1["CI Upper"], dff2["CI Upper"]]))])
    fig.update_yaxes(autorange="reversed",
                     ticklabelposition="outside top",
                     tickfont=dict(size=9),
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
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.31, x=1.2, align="left", showarrow=False)])


    return fig

def triple_vertical_percentage_graph(dff, title):
    dff['Text'] = np.select([dff["Marker"] == "*", dff["Marker"] == "...", pd.isnull(dff["Marker"])],
                            [dff.Estimate.map(str)+"%"+"*", "...", dff.Estimate.map(str)+"%"])
    dff['HoverText'] = np.select([dff["Marker"] == "*",
                                  dff["Marker"] == "...",
                                  pd.isnull(dff["Marker"])],
                                 ["Estimate: "+dff.Estimate.map(str)+"% ± "+(dff["CI Upper"] - dff["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                  "Estimate Suppressed",
                                  "Estimate: "+dff.Estimate.map(str)+"% ± "+(dff["CI Upper"] - dff["Estimate"]).map(str)+"%"])

    dff1 = dff[dff['QuestionText'] == "Top donors"]
    name1 = "Top donors"

    dff2 = dff[dff['QuestionText'] == "Top religious donors"]
    name2 = "Top religious donors"

    dff3 = dff[dff['QuestionText'] == "Top secular donors"]
    name3 = "Top secular donors"

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff1['CI Upper'],
                         y=dff1['Attribute'],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         showlegend=False,
                         hoverinfo="skip",
                         text=None,
                         textposition="outside",
                         cliponaxis=False,
                         offsetgroup=2
                         ),
                  )

    fig.add_trace(go.Bar(x=dff2['CI Upper'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         showlegend=False,
                         hoverinfo="skip",
                         text=None,
                         textposition="outside",
                         cliponaxis=False,
                         offsetgroup=1
                         ),
                  )

    fig.add_trace(go.Bar(x=dff3['CI Upper'],
                         y=dff3['Attribute'],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         showlegend=False,
                         hoverinfo="skip",
                         text=None,
                         textposition="outside",
                         cliponaxis=False,
                         offsetgroup=3
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
                         name=name1,
                         offsetgroup=2
                         ),
                  )

    fig.add_trace(go.Bar(x=dff2['Estimate'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=None,
                         hovertext =dff2['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         hoverinfo="text",
                         marker=dict(color="#7BAFD4"),
                         text=dff2['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         name=name2,
                         offsetgroup=1
                         ),
                  )

    fig.add_trace(go.Bar(x=dff3['Estimate'],
                         y=dff3['Attribute'],
                         orientation="h",
                         error_x=None,
                         hovertext=dff3['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         hoverinfo="text",
                         marker=dict(color="#50a684"),
                         text=dff3['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         name=name3,
                         offsetgroup=3
                         ),
                  )

    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin={'l': 30, 'b': 30, 'r': 10, 't': 10},
                      height=600,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      bargroupgap=0.05,
                      barmode="group",
                      legend={'orientation': 'h', 'yanchor': "bottom"},
                      updatemenus=[
                          dict(
                              type = "buttons",
                              xanchor='right',
                              x = 1.2,
                              y = 0.5,
                              buttons=list([
                                  dict(
                                      args=[{"error_x": [None, None, None, None, None, None],
                                             "text": [None, None, None, dff1['Text'], dff2['Text'], dff3['Text']]}],
                                      label="Reset",
                                      method="restyle"
                                  ),
                                  dict(
                                      args=[{"error_x": [None, None, None, dict(type="data", array=dff1["CI Upper"]-dff1["Estimate"], color="#424242", thickness=1.5),
                                                         dict(type="data", array=dff2["CI Upper"]-dff2["Estimate"], color="#424242", thickness=1.5),
                                                         dict(type="data", array=dff3["CI Upper"]-dff3["Estimate"], color="#424242", thickness=1.5)],
                                             "text": [dff1['Text'], dff2['Text'], dff3['Text'], None, None, None]}],
                                      label="Confidence Intervals",
                                      method="restyle"
                                  )
                              ]),
                          ),
                      ]
                      )

    fig.update_xaxes(showgrid=False,
                     showticklabels=False,
                     autorange=False,
                     range=[0, 1.25*max(np.concatenate([dff1["CI Upper"], dff2["CI Upper"], dff3["CI Upper"]]))])
    fig.update_yaxes(autorange="reversed",
                     ticklabelposition="outside top",
                     tickfont=dict(size=9))

    markers = pd.concat([dff1["Marker"], dff2["Marker"], dff3["Marker"]])
    if markers.isin(["*"]).any() and markers.isin(["..."]).any():
        fig.update_layout(margin={'l': 40, 'b': 75, 'r': 10, 't': 40},
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


@app.callback(
    dash.dependencies.Output('TopDonorsTotalDonations', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff2 = TopDonorsPercTotDonors_2018[TopDonorsPercTotDonors_2018['Region'] == region]
    dff1 = TopDonorsPercTotDonations_2018[TopDonorsPercTotDonations_2018['Region'] == region]

    name2 = "% donors"
    name1 = "% donation value"

    title = '{}, {}'.format("Distribution of total donations by amount donated", region)
    return dist_total_donations(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('TopDonorsDemographics', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('demo-selection', 'value')
    ])
def update_graph(region, demo):
    dff = TopDonorsDemoLikelihoods[TopDonorsDemoLikelihoods['Region'] == region]
    dff = dff[dff['Group'] == demo]

    title = '{}, {}'.format("Likelihood of being a top donor by demographic characteristic", region)
    return triple_vertical_percentage_graph(dff, title)

@app.callback(
    dash.dependencies.Output('TopDonorsSubSecSupport', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff = TopDonorsDonRates_2018[TopDonorsDonRates_2018['Region'] == region]

    title = '{}, {}'.format("Levels of support by cause, top donors vs. regular donors", region)
    return vertical_percentage_graph(dff, title)

@app.callback(
    dash.dependencies.Output('TopDonorsMotivations', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff = TopDonorsMotivations_2018[TopDonorsMotivations_2018['Region'] == region]

    title = '{}, {}'.format("Motivations for giving, top donors vs. regular donors", region)
    return vertical_percentage_graph(dff, title)

@app.callback(
    dash.dependencies.Output('TopDonorsBarriers', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff = TopDonorsBarriers_2018[TopDonorsBarriers_2018['Region'] == region]

    title = '{}, {}'.format("Barriers to giving more, top donors vs. regular donors", region)
    return vertical_percentage_graph(dff, title)


if __name__ == '__main__':
    app.run_server(debug=True)
