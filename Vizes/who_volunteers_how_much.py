import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import textwrap


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# VolRate_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-VolRate.csv")
VolRate_2018 = pd.read_csv("../Tables/2018-VolRate.csv")
# AvgTotHours_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotHours.csv")
AvgTotHours_2018 = pd.read_csv("../Tables/2018-AvgTotHours.csv")
FormsVolunteering_2018 = pd.read_csv("../Tables/2018-FormsVolunteering.csv")
PercTotVols_2018 = pd.read_csv("../Tables/2018-PercTotVolunteers.csv")
PercTotHours_2018 = pd.read_csv("../Tables/2018-PercTotHours.csv")

VolRate_2018['Estimate'] = VolRate_2018['Estimate']*100
VolRate_2018['CI Upper'] = VolRate_2018['CI Upper']*100
FormsVolunteering_2018['Estimate'] = FormsVolunteering_2018['Estimate']*100
FormsVolunteering_2018['CI Upper'] = FormsVolunteering_2018['CI Upper']*100
PercTotVols_2018['Estimate'] = PercTotVols_2018['Estimate']*100
PercTotVols_2018['CI Upper'] = PercTotVols_2018['CI Upper']*100
PercTotHours_2018['Estimate'] = PercTotHours_2018['Estimate']*100
PercTotHours_2018['CI Upper'] = PercTotHours_2018['CI Upper']*100

data = [VolRate_2018, AvgTotHours_2018, PercTotVols_2018, PercTotHours_2018, FormsVolunteering_2018]

for i in range(len(data)):
    data[i]["Estimate"] = np.where(data[i]["Marker"]=="...", 0, data[i]["Estimate"])
    data[i]["CI Upper"] = np.where(data[i]["Marker"]=="...", 0, data[i]["CI Upper"])

    data[i]["Region"] = np.select([data[i]["Province"] == "SK",
                                   data[i]["Province"] == "MB",
                                   data[i]["Province"] == "NB",
                                   data[i]["Province"] == "NS",
                                   data[i]["Province"] == "PE",
                                   data[i]["Province"] == "NL"],
                                  ["SK", "MB", "NB", "NS", "PE", "NL"], default=data[i]["Region"])

    data[i]["Group"] = np.where(data[i]["Attribute"]=="Unable to determine", "", data[i]["Group"])
    data[i]["Group"] = np.where(data[i]["Attribute"]=="Unknown", "", data[i]["Group"])

    data[i]["Attribute"] = data[i]["Attribute"].str.wrap(15)
    data[i]["Attribute"] = data[i]["Attribute"].replace({'\n': '<br>'}, regex=True)

    data[i]['Estimate'] = data[i]['Estimate'].round(0).astype(int)
    data[i]["CI Upper"] = data[i]["CI Upper"].round(0).astype(int)
    data[i]['cv'] = data[i]['cv'].round(2)

region_values = np.array(['CA', 'BC', 'AB', 'PR', 'SK', 'MB', 'ON', 'QC', 'AT', 'NB', 'NS', 'PE', 'NL'], dtype=object)
region_names = np.array(['Canada',
                         'British Columbia',
                         'Alberta',
                         'Prairie Provinces (SK, MB)',
                         'Saskatchewan',
                         'Manitoba',
                         'Ontario',
                         'Quebec',
                         'Atlantic Provinces (NB, NS, PE, NL)',
                         'New Brunswick',
                         'Nova Scotia',
                         'Prince Edward Island',
                         'Newfoundland and Labrador'], dtype=str)

fig1df1 = VolRate_2018[VolRate_2018['Group'] == "All"]
fig1df1 = fig1df1[fig1df1.Province.notnull()]

fig1df2 = AvgTotHours_2018[AvgTotHours_2018['Group'] == "All"]
fig1df2 = fig1df2[fig1df2.Province.notnull()]

fig1df1['Text'] = np.select([fig1df1["Marker"] == "*", fig1df1["Marker"] == "...", pd.isnull(fig1df1["Marker"])],
                            [fig1df1.Estimate.map(str)+"%"+"*", "...", fig1df1.Estimate.map(str)+"%"])
fig1df1['HoverText'] = np.select([fig1df1["Marker"] == "*",
                                  fig1df1["Marker"] == "...",
                                  pd.isnull(fig1df1["Marker"])],
                                 ["Estimate: "+fig1df1.Estimate.map(str)+"% ± "+(fig1df1["CI Upper"] - fig1df1["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                  "Estimate Suppressed",
                                  "Estimate: "+fig1df1.Estimate.map(str)+"% ± "+(fig1df1["CI Upper"] - fig1df1["Estimate"]).map(str)+"%"])

fig1df2['Text'] = np.select([fig1df2["Marker"] == "*", fig1df2["Marker"] == "...", pd.isnull(fig1df2["Marker"])],
                            ["$"+fig1df2.Estimate.map(str)+"*", "...", "$"+fig1df2.Estimate.map(str)])
fig1df2['HoverText'] = np.select([fig1df2["Marker"] == "*",
                                  fig1df2["Marker"] == "...",
                                  pd.isnull(fig1df2["Marker"])],
                                 ["Estimate: $"+fig1df2.Estimate.map(str)+" ± $"+(fig1df2["CI Upper"] - fig1df2["Estimate"]).map(str)+"<br><b>Use with caution</b>",
                                  "Estimate Suppressed",
                                  "Estimate: $"+fig1df2.Estimate.map(str)+" ± $"+(fig1df2["CI Upper"] - fig1df2["Estimate"]).map(str)])

fig1 = go.Figure()

fig1.add_trace(go.Bar(x=fig1df2['Province'],
                      y=fig1df2['CI Upper'],
                      marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                      text=None,
                      textposition='outside',
                      showlegend=False,
                      hoverinfo="skip",
                      cliponaxis=False,
                      offsetgroup=1,
                      ),
               )

fig1.add_trace(go.Bar(x=fig1df1['Province'],
                      y=fig1df1['CI Upper'],
                      marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                      text=None,
                      textposition='outside',
                      hoverinfo="skip",
                      showlegend=False,
                      name="Volunteer rate",
                      yaxis='y2',
                      offsetgroup=2,
                      ),
               )

fig1.add_trace(go.Bar(x=fig1df2['Province'],
                      y=fig1df2['Estimate'],
                      error_y=None, # need to vectorize subtraction
                      hovertext =fig1df2['HoverText'],
                      hovertemplate="%{hovertext}",
                      hoverlabel=dict(font=dict(color="white")),
                      hoverinfo="text",
                      marker=dict(color="#7BAFD4"),
                      text=fig1df2['Text'],
                      textposition='outside',
                      cliponaxis=False,
                      name="Average hours",
                      offsetgroup=1
                      ),
               )

fig1.add_trace(go.Bar(x=fig1df1['Province'],
                      y=fig1df1['Estimate'],
                      error_y=None,
                      hovertext=fig1df1['HoverText'],
                      hovertemplate="%{hovertext}",
                      hoverlabel=dict(font=dict(color="white")),
                      hoverinfo="text",
                      marker=dict(color="#c8102e"),
                      text=fig1df1['Text'],
                      textposition='outside',
                      cliponaxis=False,
                      name="Volunteer rate",
                      yaxis='y2',
                      offsetgroup=2
                      ),
               )

y1 = go.layout.YAxis(overlaying='y', side='left', range = [0, 1.25*max(fig1df2["CI Upper"])])
y2 = go.layout.YAxis(overlaying='y', side='right', range = [0, 1.25*max(fig1df1["CI Upper"])])

fig1.update_layout(title={'text': "Volunteer rate & average hours volunteered by province",
                          'y': 0.99},
                   margin={'l': 30, 'b': 30, 'r': 10, 't': 10},
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   barmode="group",
                   yaxis1=y1,
                   yaxis2=y2,
                   legend={'orientation': 'h', 'yanchor': "bottom", 'xanchor': 'center', 'x': 0.5, 'y': -0.15, 'traceorder': 'reversed'},
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
                                          "text": [None, None, fig1df2['Text'], fig1df1['Text']],
                                          }],
                                   label="Reset",
                                   method="restyle"
                               ),
                               dict(
                                   args=[{"error_y": [None, None, dict(type="data", array=fig1df2["CI Upper"]-fig1df2["Estimate"], color="#424242", thickness=1.5), dict(type="data", array=fig1df1["CI Upper"]-fig1df1["Estimate"], color="#424242", thickness=1.5)],
                                          "text": [fig1df2['Text'], fig1df1['Text'], None, None],
                                          }],
                                   label="Confidence Intervals",
                                   method="restyle"
                               )
                           ]),
                       ),
                   ])

# Aesthetics for fig
fig1.update_xaxes(autorange="reversed", tickfont=dict(size=12))
fig1.update_yaxes(showgrid=False,
                  showticklabels=False,
                  autorange = False)

markers = pd.concat([fig1df1["Marker"], fig1df2["Marker"]])
if markers.isin(["*"]).any() and markers.isin(["..."]).any():
    fig1.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                       annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.4, align="left", showarrow=False),
                                    dict(text="*<i>Use with caution<br>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
elif markers.isin(["*"]).any():
    fig1.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                       annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.4, align="left", showarrow=False),
                                    dict(text="*<i>Use with caution</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
elif markers.isin(["..."]).any():
    fig1.update_layout(margin={'l': 30, 'b': 75, 'r': 10, 't': 40},
                       annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.19, x=1.4, align="left", showarrow=False),
                                    dict(text="<i>Some results too unreliable to be shown</i>", xref="paper", yref="paper", xanchor='right', yanchor="top", y=-0.11, x=1.2, align="right", showarrow=False, font=dict(size=13))])
else:
    fig1.update_layout(margin={'l': 30, 'b': 30, 'r': 10, 't': 40},
                       annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.21, x=1.4, align="left", showarrow=False)])


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
                      options=[{'label': region_names[i], 'value': region_values[i]} for i in range(len(region_values))],
                      # Default value, shows up at top of dropdown list and automatically filters graphs upon loading
                      value='CA',
                      style={'verticalAlgin': 'middle'}
                  ),
                  ],
                 style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div([
        dcc.Graph(id='FormsVolunteering', style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-prv', figure=fig1, style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-Gndr', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-Gndr', style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-Age', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-Age', style={'marginTop': 100}),
        dcc.Graph(id='VolRateAvgHours-Educ', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-Educ', style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-MarStat', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-MarStat', style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-Inc', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-Inc', style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-Relig', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-Relig', style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-Labour', style={'marginTop': 50}),
        dcc.Graph(id='VolRateAvgHours-ImmStat', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-Labour', style={'marginTop': 50}),
        dcc.Graph(id='PercVolHours-ImmStat', style={'marginTop': 50})

    ],
        style={'width': '50%', 'display': 'inline-block', "marginTop": 20}),

])

def forms_of_giving(dff, title):
    dff['Text'] = np.select([dff["Marker"] == "*", dff["Marker"] == "...", pd.isnull(dff["Marker"])],
                            [dff.Estimate.map(str)+"%"+"*", "...", dff.Estimate.map(str)+"%"])
    dff['HoverText'] = np.select([dff["Marker"] == "*",
                                  dff["Marker"] == "...",
                                  pd.isnull(dff["Marker"])],
                                 ["Estimate: "+dff.Estimate.map(str)+"% ± "+(dff["CI Upper"] - dff["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                  "Estimate Suppressed",
                                  "Estimate: "+dff.Estimate.map(str)+"% ± "+(dff["CI Upper"] - dff["Estimate"]).map(str)+"%"])

    fig = go.Figure()

    fig.add_trace(go.Bar(y=dff['CI Upper'],
                         x=dff['QuestionText'],
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         text=None,
                         textposition='outside',
                         hoverinfo="skip",
                         showlegend=False,
                         offsetgroup=1
                         )
                  )

    fig.add_trace(go.Bar(y=dff['Estimate'],
                         x=dff['QuestionText'],
                         error_y=None, # need to vectorize subtraction
                         marker=dict(color="#c8102e"),
                         name="Forms of giving",
                         hovertext =dff['HoverText'],
                         hovertemplate ="%{hovertext}",
                         hoverlabel=dict(font=dict(color="white")),
                         hoverinfo="text",
                         text=dff['Text'],
                         textposition='outside',
                         cliponaxis=False,
                         showlegend=False,
                         offsetgroup=1
                         )
                  )

    fig.update_layout(title={'text': title,
                             'y': 0.99},
                      margin={'l': 30, 'b': 30, 'r': 10, 't': 10},
                      height=400,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      updatemenus=[
                          dict(
                              type = "buttons",
                              xanchor='right',
                              x = 1.4,
                              y = 0.5,
                              buttons=list([
                                  dict(
                                      args=[{"error_y": [None, None],
                                             "text": [None, dff['Text']]}],
                                      label="Reset",
                                      method="restyle"
                                  ),
                                  dict(
                                      args=[{"error_y": [None, dict(type="data", array=dff["CI Upper"]-dff["Estimate"], color="#424242", thickness=1.5)],
                                             "text": [dff['Text'], None]}],
                                      label="Confidence Intervals",
                                      method="restyle"
                                  )
                              ]),
                          ),
                      ])

    # Aesthetics for fig
    fig.update_yaxes(showticklabels=False,
                     autorange = False,
                     range = [0, 1.1*max(dff["CI Upper"])])
    fig.update_xaxes(showgrid=False, tickfont=dict(size=12))

    markers = dff["Marker"]
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
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.23, x=1.4, align="left", showarrow=False)])

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

def perc_don_perc_amt(dff1, dff2, name1, name2, title):
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
    dff1 = dff1[(dff1.Attribute != "Not in labour force")]
    # & (dff1.Attribute != "Unknown")]
    dff2 = dff2[(dff2.Attribute != "Not in labour force")]
    #& (dff2.Attribute != "Unknown")]

    # Scatter plot - data frame, x label, y label
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
                         error_x=None, # need to vectorize subtraction
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
                         error_x=None, # need to vectorize subtraction
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
                      height=400,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      bargroupgap=0.05,
                      barmode="group",
                      legend={'orientation': 'h', 'yanchor': "middle"},
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

    # Aesthetics for fig
    fig.update_xaxes(showgrid=False,
                     showticklabels=False,
                     autorange = False,
                     range = [0, 1.25*max(np.concatenate([dff1["CI Upper"], dff2["CI Upper"]]))])
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
                          annotations=[dict(text="<a href=\"https://www.scribbr.com/statistics/confidence-interval/\">What is this?</a>", xref="paper", yref="paper", xanchor='right', y=0.21, x=1.2, align="left", showarrow=False)])


    return fig

@app.callback(
    dash.dependencies.Output('FormsVolunteering', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = FormsVolunteering_2018[FormsVolunteering_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "All"]

    title = '{}, {}'.format("Forms of giving", region)

    return forms_of_giving(dff1, title)

# Interaction: graph-1, with region-selection
@app.callback(
    dash.dependencies.Output('VolRateAvgHours-Age', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by age group", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('VolRateAvgHours-Gndr', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by gender", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('VolRateAvgHours-MarStat', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by marital status", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('VolRateAvgHours-Educ', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by education", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)


@app.callback(
    dash.dependencies.Output('VolRateAvgHours-Labour', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by employment status", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('VolRateAvgHours-Relig', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by religious attendance", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('VolRateAvgHours-Inc', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by income", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('VolRateAvgHours-ImmStat', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = VolRate_2018[VolRate_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "Volunteer rate"


    dff2 = AvgTotHours_2018[AvgTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Average hours"

    title = '{}, {}'.format("Volunteer rate & average hours volunteered by immigration status", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)



@app.callback(
    dash.dependencies.Output('PercVolHours-Age', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])

def update_graph(region):



    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by age", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercVolHours-Gndr', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):



    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by gender", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercVolHours-MarStat', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):



    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by marital status", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercVolHours-Educ', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):



    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by education", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercVolHours-Labour', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):



    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by employment", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercVolHours-Relig', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):



    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by religious attendance", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercVolHours-Inc', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):



    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by income", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercVolHours-ImmStat', 'figure'),
    [

        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):

    dff1 = PercTotVols_2018[PercTotVols_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "% volunteers"


    dff2 = PercTotHours_2018[PercTotHours_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "% volunteer hours"

    title = '{}, {}'.format("Percentage of Canadians & total hours volunteered by immigration status", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

if __name__ == '__main__':
    app.run_server(debug=True)
