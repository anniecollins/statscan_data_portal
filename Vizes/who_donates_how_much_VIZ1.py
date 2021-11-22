import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import textwrap


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Reading in data from public urls
# DonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-DonRate.csv")
DonRates_2018 = pd.read_csv("../Tables/2018-DonRate.csv")
# AvgTotDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotDon.csv")
AvgTotDon_2018 = pd.read_csv("../Tables/2018-AvgTotDon.csv")
# AvgNumCauses_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgNumCauses.csv")
AvgNumCauses_2018 = pd.read_csv("../Tables/2018-AvgNumCauses.csv")
FormsGiving_2018 = pd.read_csv("../Tables/2018-FormsGiving.csv")
TopCauseFocus_2018 = pd.read_csv("../Tables/2018-TopCauseFocus.csv")
PropTotDon_2018 = pd.read_csv("../Tables/2018-PercTotDonors.csv")
PropTotDonAmt_2018 = pd.read_csv("../Tables/2018-PercTotDonations.csv")

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

for i in range(len(data)):
    # Suppress Estimate and CI Upper where necessary (for visualizations and error bars)
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

    # Round rates and dollar amounts to zero decimal places
    data[i]['Estimate'] = data[i]['Estimate'].round(0).astype(int)
    data[i]["CI Upper"] = data[i]["CI Upper"].round(0).astype(int)
    data[i]['cv'] = data[i]['cv'].round(2)

for i in range(len(data_num)):
    # Suppress Estimate and CI Upper where necessary (for visualizations and error bars)
    data_num[i]["Estimate"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["Estimate"])
    data_num[i]["CI Upper"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["CI Upper"])

    data_num[i]["Region"] = np.select([data_num[i]["Province"] == "SK",
                                       data_num[i]["Province"] == "MB",
                                       data_num[i]["Province"] == "NB",
                                       data_num[i]["Province"] == "NS",
                                       data_num[i]["Province"] == "PE",
                                       data_num[i]["Province"] == "NL"],
                                     ["SK", "MB", "NB", "NS", "PE", "NL"], default=data_num[i]["Region"])

    data_num[i]["Group"] = np.where(data_num[i]["Attribute"]=="Unable to determine", "", data_num[i]["Group"])
    data_num[i]["Group"] = np.where(data_num[i]["Attribute"]=="Unknown", "", data_num[i]["Group"])

    data_num[i]["Attribute"] = data_num[i]["Attribute"].str.wrap(15)
    data_num[i]["Attribute"] = data_num[i]["Attribute"].replace({'\n': '<br>'}, regex=True)

    # Round number amounts to two decimal places
    data_num[i]['Estimate'] = data_num[i]['Estimate'].round(1)
    data_num[i]["CI Upper"] = data_num[i]["CI Upper"].round(1)
    data_num[i]['cv'] = data[i]['cv'].round(2)

# Extract info from data for selection menus
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

fig1df1 = DonRates_2018[DonRates_2018['Group'] == "All"]
fig1df1 = fig1df1[fig1df1.Province.notnull()]

fig1df2 = AvgTotDon_2018[AvgTotDon_2018['Group'] == "All"]
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


# Donation rate &amp; average donation amount by province
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
                      name="Donor rate",
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
                      name="Average donation amount",
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
                        name="Donor rate",
                        yaxis='y2',
                        offsetgroup=2
                     ),
              )



y1 = go.layout.YAxis(overlaying='y', side='left', range = [0, 1.25*max(fig1df2["CI Upper"])])
y2 = go.layout.YAxis(overlaying='y', side='right', range = [0, 1.25*max(fig1df1["CI Upper"])])

fig1.update_layout(title={'text': "Donation rate & average donation amount by province",
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
                      options=[{'label': region_names[i], 'value': region_values[i]} for i in range(len(region_values))],
                      # Default value, shows up at top of dropdown list and automatically filters graphs upon loading
                      value='CA',
                      style={'verticalAlgin': 'middle'}
                  ),
                  ],
                 style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div([
        # Graph components!
        dcc.Graph(id='FormsGiving', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-prv', figure=fig1, style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Gndr', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-Gndr', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-Gndr', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Age', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-Age', style={'marginTop': 100}),
        dcc.Graph(id='PrimCauseNumCause-Age', style={'marginTop': 100}),
        dcc.Graph(id='DonRateAvgDonAmt-Educ', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-Educ', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-Educ', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Inc', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-Inc', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-Inc', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Relig', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-Relig', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-Relig', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-MarStat', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-Labour', style={'marginTop': 50}),
        dcc.Graph(id='DonRateAvgDonAmt-ImmStat', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-MarStat', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-Labour', style={'marginTop': 50}),
        dcc.Graph(id='PercDon-ImmStat', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-MarStat', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-Labour', style={'marginTop': 50}),
        dcc.Graph(id='PrimCauseNumCause-ImmStat', style={'marginTop': 50}),

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
    # Make text column - dff1.Estimate.map(str)+"%" where Marker == NA, dff1.Estimate.map(str)+"%"+"*" where Marker == *, "..." where Marker == ...
    dff1['Text'] = np.select([dff1["Marker"] == "*", dff1["Marker"] == "...", pd.isnull(dff1["Marker"])],
                            [dff1.Estimate.map(str)+"%"+"*", "...", dff1.Estimate.map(str)+"%"])
    dff1['HoverText'] = np.select([dff1["Marker"] == "*",
                                   dff1["Marker"] == "...",
                                   pd.isnull(dff1["Marker"])],
                                  ["Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: "+dff1.Estimate.map(str)+"% ± "+(dff1["CI Upper"] - dff1["Estimate"]).map(str)+"%"])
    dff2['Text'] = np.select([dff2["Marker"] == "*", dff2["Marker"] == "...", pd.isnull(dff2["Marker"])],
                            [dff2.Estimate.map(str)+"*", "...", dff2.Estimate.map(str)])
    dff2['HoverText'] = np.select([dff2["Marker"] == "*",
                                   dff2["Marker"] == "...",
                                   pd.isnull(dff2["Marker"])],
                                  ["Estimate: "+dff2.Estimate.map(str)+" ± "+(dff2["CI Upper"] - dff2["Estimate"]).map(str)+"<br><b>Use with caution</b>",
                                   "Estimate Suppressed",
                                   "Estimate: "+dff2.Estimate.map(str)+" ± "+(dff2["CI Upper"] - dff2["Estimate"]).map(str)])

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
                         cliponaxis=False,
                         showlegend=False,
                         xaxis='x2',
                         offsetgroup=2
                         ),
                  )

    fig.add_trace(go.Bar(x=dff2['CI Upper'],
                         y=dff2['Attribute'],
                         orientation="h",
                         error_x=None, # need to vectorize subtraction
                         marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF")),
                         hoverinfo="skip",
                         text=None,
                         textposition='outside',
                         cliponaxis=False,
                         showlegend=False,
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
                         hoverinfo="text",
                        marker=dict(color="#7BAFD4"),
                        text=dff2['Text'],
                        textposition='outside',
                        cliponaxis=False,
                        insidetextanchor=None,
                        name=name2,
                        xaxis='x1',
                        offsetgroup=1
                     ),
              )

    x1 = go.layout.XAxis(overlaying='x', side='top', range= [0, 1.25*max(dff2['CI Upper'])])
    x2 = go.layout.XAxis(overlaying='x', side='bottom', range= [0, 1.25*max(dff1['CI Upper'])])

    fig.update_layout(title={'text': title,
                         'y': 0.99},
                      margin={'l': 30, 'b': 30, 'r': 10, 't': 10},
                      height=400,
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      bargroupgap=0.05,
                      barmode="group",
                      xaxis1 =x1,
                      xaxis2=x2,
                      legend={'orientation': 'h', 'yanchor': "bottom", 'y': -0.15},
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
                     autorange=False)
    fig.update_yaxes(autorange="reversed",
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
    dash.dependencies.Output('DonRateAvgDonAmt-Gndr', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by gender", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('DonRateAvgDonAmt-MarStat', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by marital status", region)

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
    dash.dependencies.Output('DonRateAvgDonAmt-Labour', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by employment status", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('DonRateAvgDonAmt-Relig', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by religious attendance", region)

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
    dff1 = dff1[dff1['Group'] == "Family income category"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Family income category"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by income", region)

    # Uses external function with dataframes, names, and title set up above
    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-1
    dash.dependencies.Output('DonRateAvgDonAmt-ImmStat', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "Donation rate"

    # Average annual donation data, filtered for selected region and demographic group (age group)
    # Corresponding name assigned
    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Average annual donations"

    # Format title according to dropdown input
    title = '{}, {}'.format("Donor rate and average annual donation by immigration status", region)

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
    dash.dependencies.Output('PercDon-Gndr', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by gender", region)

    # Uses external function with dataframes, names, and title set up above
    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('PercDon-MarStat', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Marital status (original)"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by marital status", region)

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
    dash.dependencies.Output('PercDon-Labour', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by employment", region)

    # Uses external function with dataframes, names, and title set up above
    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('PercDon-Relig', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by religious attendance", region)

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
    dff1 = dff1[dff1['Group'] == "Family income category"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Family income category"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by income", region)

    # Uses external function with dataframes, names, and title set up above
    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    # Output: change to graph-2
    dash.dependencies.Output('PercDon-ImmStat', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "Proportion of donors"

    # Average annual donation data, filtered for selected region and demographic group (education)
    # Corresponding name assigned
    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Percentage of donation value"

    # Format title according to dropdown input
    title = '{}, {}'.format("Percentage of donors & total donation value by immigration status", region)

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

    # Average number of annual donations data, filtered for selected region and demographic group
    # Corresponding name assigned
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
    dash.dependencies.Output('PrimCauseNumCause-Gndr', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by gender", region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('PrimCauseNumCause-MarStat', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by marital status", region)

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

    # Average number of annual donations data, filtered for selected region and demographic group
    # Corresponding name assigned
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
    dash.dependencies.Output('PrimCauseNumCause-Labour', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by employment status", region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('PrimCauseNumCause-Relig', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by religious attendance", region)

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
    dff1 = dff1[dff1['Group'] == "Family income category"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Family income category"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by income", region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    # Output: change to graph-4
    dash.dependencies.Output('PrimCauseNumCause-ImmStat', 'figure'),
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
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "Average number of causes"

    # Average number of causes supported data, filtered for selected region and demographic group
    # Corresponding name assigned
    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Average concentration on first cause"

    # Format title according to dropdown input
    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by immigration status", region)

    # Uses external function with dataframes, names, and title set up above
    return prim_cause_num_cause(dff2, dff1, name2, name1, title)



if __name__ == '__main__':
    app.run_server(debug=True)
