import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import textwrap

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

TopVolsMotivations_2018 = pd.read_csv("../Tables/2018-TopVolunteersMotivationsForVolunteering.csv")
TopVolsBarriers_2018 = pd.read_csv("../Tables/2018-TopVolsBarriersToVolunteering.csv")
TopVolsPercTotHours_2018 = pd.read_csv("../Tables/2018-TopVolsPercTotHours.csv")
TopVolsPercTotVols_2018 = pd.read_csv("../Tables/2018-TopVolsPercTotVols.csv")
TopVolsVolRates_2018 = pd.read_csv("../Tables/2018-TopVolsVolRates.csv")
TopVolsDemoLikelihoods = pd.read_csv("../Tables/2018-TopVolsDemoLikelihoods.csv")

TopVolsMotivations_2018['Estimate'] = TopVolsMotivations_2018['Estimate'] * 100
TopVolsMotivations_2018['CI Upper'] = TopVolsMotivations_2018['CI Upper'] * 100
TopVolsBarriers_2018['Estimate'] = TopVolsBarriers_2018['Estimate'] * 100
TopVolsBarriers_2018['CI Upper'] = TopVolsBarriers_2018['CI Upper'] * 100
TopVolsPercTotHours_2018['Estimate'] = TopVolsPercTotHours_2018['Estimate'] * 100
TopVolsPercTotHours_2018['CI Upper'] = TopVolsPercTotHours_2018['CI Upper'] * 100
TopVolsPercTotVols_2018['Estimate'] = TopVolsPercTotVols_2018['Estimate'] * 100
TopVolsPercTotVols_2018['CI Upper'] = TopVolsPercTotVols_2018['CI Upper'] * 100
TopVolsVolRates_2018['Estimate'] = TopVolsVolRates_2018['Estimate'] * 100
TopVolsVolRates_2018['CI Upper'] = TopVolsVolRates_2018['CI Upper'] * 100
TopVolsDemoLikelihoods['Estimate'] = TopVolsDemoLikelihoods['Estimate'] * 100
TopVolsDemoLikelihoods['CI Upper'] = TopVolsDemoLikelihoods['CI Upper'] * 100

data = [TopVolsMotivations_2018, TopVolsBarriers_2018, TopVolsPercTotHours_2018, TopVolsPercTotVols_2018, TopVolsVolRates_2018, TopVolsDemoLikelihoods]

for i in range(len(data)):
    data[i]["Estimate"] = np.where(data[i]["Marker"] == "...", 0, data[i]["Estimate"])
    data[i]["CI Upper"] = np.where(data[i]["Marker"] == "...", 0, data[i]["CI Upper"])

    data[i]["Group"] = np.where(data[i]["Attribute"] == "Unable to determine", "", data[i]["Group"])
    data[i]["Group"] = np.where(data[i]["Attribute"] == "Unknown", "", data[i]["Group"])

    data[i]["Attribute"] = data[i]["Attribute"].str.wrap(15)
    data[i]["Attribute"] = data[i]["Attribute"].replace({'\n': '<br>'}, regex=True)
    data[i]["Attribute"] = np.where(data[i]["Attribute"] == "Regular<br>volunteer", "Regular volunteer", data[i]["Attribute"])

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

demo_names = TopVolsDemoLikelihoods["Group"].unique()

app.layout = html.Div([
    html.Div([
        html.H1('Understanding Top Volunteers')]),
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
        dcc.Graph(id='TopVolsTotalHours', style={'marginTop': 50}),
        html.Div([
            "Choose demographic feature to display below: ",
            dcc.Dropdown(id='demo-selection',
                         options=[{'label': i, 'value': i} for i in demo_names],
                         value="Age group")
        ], style={'marginTop': 50, 'width': '100%', 'verticalAlign': 'middle'}),
        dcc.Graph(id='TopVolsDemographics', style={'marginTop': 50}),
        dcc.Graph(id='TopVolsSubSecSupport', style={'marginTop': 50}),
        dcc.Graph(id='TopVolsMotivations', style={'marginTop': 50}),
        dcc.Graph(id='TopVolsBarriers', style={'marginTop': 50})
    ],
        style={'width': '50%', 'display': 'inline-block', "marginTop": 20}),
])


def dist_total_donations(dff1, dff2, name1, name2, title):
    dff1['Text'] = np.select([dff1["Marker"] == "*", dff1["Marker"] == "...", pd.isnull(dff1["Marker"])],
                             [dff1.Estimate.map(str) + "%" + "*", "...", dff1.Estimate.map(str) + "%"])
    dff1['HoverText'] = np.select([dff1["Marker"] == "*",
                                   dff1["Marker"] == "...",
                                   pd.isnull(dff1["Marker"])],
                                  ["Estimate: " + dff1.Estimate.map(str) + "% ± " + (dff1["CI Upper"] - dff1["Estimate"]).map(str) + "%<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: " + dff1.Estimate.map(str) + "% ± " + (dff1["CI Upper"] - dff1["Estimate"]).map(str) + "%"])

    dff2['Text'] = np.select([dff2["Marker"] == "*", dff2["Marker"] == "...", pd.isnull(dff2["Marker"])],
                             [dff2.Estimate.map(str) + "%" + "*", "...", dff2.Estimate.map(str) + "%"])
    dff2['HoverText'] = np.select([dff2["Marker"] == "*",
                                   dff2["Marker"] == "...",
                                   pd.isnull(dff2["Marker"])],
                                  ["Estimate: " + dff2.Estimate.map(str) + "% ± " + (dff2["CI Upper"] - dff2["Estimate"]).map(str) + "%<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: " + dff2.Estimate.map(str) + "% ± " + (dff2["CI Upper"] - dff2["Estimate"]).map(str) + "%"])
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
                         hovertext=dff2['HoverText'],
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
                              type="buttons",
                              xanchor='right',
                              x=1.4,
                              y=0.5,
                              buttons=list([
                                  dict(
                                      args=[{"error_y": [None, None, None, None],
                                             "text": [None, None, dff2['Text'], dff1['Text']],
                                             }],
                                      label="Reset",
                                      method="restyle"
                                  ),
                                  dict(
                                      args=[{"error_y": [None, None, dict(type="data", array=dff2["CI Upper"] - dff2["Estimate"], color="#424242", thickness=1.5), dict(type="data", array=dff1["CI Upper"] - dff1["Estimate"], color="#424242", thickness=1.5)],
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


def vertical_percentage_graph(dff, title, name1, name2):
    dff['Text'] = np.select([dff["Marker"] == "*", dff["Marker"] == "...", pd.isnull(dff["Marker"])],
                            [dff.Estimate.map(str) + "%" + "*", "...", dff.Estimate.map(str) + "%"])
    dff['HoverText'] = np.select([dff["Marker"] == "*",
                                  dff["Marker"] == "...",
                                  pd.isnull(dff["Marker"])],
                                 ["Estimate: " + dff.Estimate.map(str) + "% ± " + (dff["CI Upper"] - dff["Estimate"]).map(str) + "%<br><b>Use with caution</b>",
                                  "Estimate Suppressed",
                                  "Estimate: " + dff.Estimate.map(str) + "% ± " + (dff["CI Upper"] - dff["Estimate"]).map(str) + "%"])

    dff1 = dff[dff['Attribute'] == name1]

    dff2 = dff[dff['Attribute'] == name2]

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
                         hovertext=dff2['HoverText'],
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
                              type="buttons",
                              xanchor='right',
                              x=1.2,
                              y=0.5,
                              buttons=list([
                                  dict(
                                      args=[{"error_x": [None, None, None, None],
                                             "text": [None, None, dff1['Text'], dff2['Text']]}],
                                      label="Reset",
                                      method="restyle"
                                  ),
                                  dict(
                                      args=[{"error_x": [None, None, dict(type="data", array=dff1["CI Upper"] - dff1["Estimate"], color="#424242", thickness=1.5), dict(type="data", array=dff2["CI Upper"] - dff2["Estimate"], color="#424242", thickness=1.5)],
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
                     autorange=False,
                     range=[0, 1.25 * max(np.concatenate([dff1["CI Upper"], dff2["CI Upper"]]))])
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


def single_vertical_percentage_graph(dff, title, by="Attribute", sort=False):

    dff['Text'] = np.select([dff["Marker"] == "*", dff["Marker"] == "...", pd.isnull(dff["Marker"])],
                            [dff.Estimate.map(str) + "%" + "*", "...", dff.Estimate.map(str) + "%"])
    dff['HoverText'] = np.select([dff["Marker"] == "*",
                                  dff["Marker"] == "...",
                                  pd.isnull(dff["Marker"])],
                                 ["Estimate: " + dff.Estimate.map(str) + "% ± " + (dff["CI Upper"] - dff["Estimate"]).map(str) + "%<br><b>Use with caution</b>",
                                  "Estimate Suppressed",
                                  "Estimate: " + dff.Estimate.map(str) + "% ± " + (dff["CI Upper"] - dff["Estimate"]).map(str) + "%"])

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dff['CI Upper'],
                         y=dff[by],
                         orientation="h",
                         error_x=None,
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         showlegend=False,
                         hoverinfo="skip",
                         text=None,
                         name="",
                         textposition="outside",
                         cliponaxis=False,
                         offsetgroup=1
                         ),
                  )

    fig.add_trace(go.Bar(x=dff['Estimate'],
                         y=dff[by],
                         orientation="h",
                         error_x=None,
                         hovertext=dff['HoverText'],
                         hovertemplate="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         hoverinfo="text",
                         marker=dict(color="#c8102e"),
                         text=dff['Text'],
                         name="",
                         textposition='outside',
                         cliponaxis=False,
                         offsetgroup=1
                         ),
                  )

    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin={'l': 30, 'b': 30, 'r': 10, 't': 10},
                      height=600,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      showlegend=False,
                      updatemenus=[
                          dict(
                              type="buttons",
                              xanchor='right',
                              x=1.2,
                              y=0.5,
                              buttons=list([
                                  dict(
                                      args=[{"error_x": [None, None],
                                             "text": [None, dff['Text']]}],
                                      label="Reset",
                                      method="restyle"
                                  ),
                                  dict(
                                      args=[{"error_x": [None, dict(type="data", array=dff["CI Upper"] - dff["Estimate"], color="#424242", thickness=1.5)],
                                             "text": [dff['Text'], None]}],
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
                     range=[0, 1.25 * max(dff["CI Upper"])])
    fig.update_yaxes(autorange="reversed",
                     ticklabelposition="outside top",
                     tickfont=dict(size=9))

    if sort:
        fig.update_yaxes(categoryorder="total descending")

    markers = dff["Marker"]
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
    dash.dependencies.Output('TopVolsTotalHours', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff2 = TopVolsPercTotVols_2018[TopVolsPercTotVols_2018['Region'] == region]
    dff1 = TopVolsPercTotHours_2018[TopVolsPercTotHours_2018['Region'] == region]

    name2 = "% volunteers"
    name1 = "% volunteer hours"

    title = '{}, {}'.format("Distribution of total time by hours volunteered", region)
    return dist_total_donations(dff1, dff2, name1, name2, title)


@app.callback(
    dash.dependencies.Output('TopVolsDemographics', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
        dash.dependencies.Input('demo-selection', 'value')
    ])
def update_graph(region, demo):
    dff = TopVolsDemoLikelihoods[TopVolsDemoLikelihoods['Region'] == region]
    dff = dff[dff['Group'] == demo]

    title = '{}, {}'.format("Likelihood of being a top volunteer by demographic characteristic", region)
    return single_vertical_percentage_graph(dff, title)


@app.callback(
    dash.dependencies.Output('TopVolsSubSecSupport', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff = TopVolsVolRates_2018[TopVolsVolRates_2018['Region'] == region]
    name1 = "Top volunteer"
    name2 = "Regular volunteer"

    title = '{}, {}'.format("Levels of support by cause, top volunteers vs. regular volunteers", region)
    return vertical_percentage_graph(dff, title, name1, name2)


@app.callback(
    dash.dependencies.Output('TopVolsMotivations', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff = TopVolsMotivations_2018[TopVolsMotivations_2018['Region'] == region]
    name1 = "Top volunteer"
    name2 = "Regular volunteer"

    title = '{}, {}'.format("Motivations for volunteering, top volunteers vs. regular volunteers", region)
    return vertical_percentage_graph(dff, title, name1, name2)


@app.callback(
    dash.dependencies.Output('TopVolsBarriers', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff = TopVolsBarriers_2018[TopVolsBarriers_2018['Region'] == region]
    name1 = "Top volunteer"
    name2 = "Regular volunteer"

    title = '{}, {}'.format("Barriers to volunteering more, top volunteers vs. regular volunteers", region)
    return vertical_percentage_graph(dff, title, name1, name2)


if __name__ == '__main__':
    app.run_server(debug=True)
