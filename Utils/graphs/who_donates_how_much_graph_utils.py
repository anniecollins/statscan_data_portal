import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


###################### Graph functions ######################

def forms_of_giving(dff, title):
    fig = go.Figure()

    fig.add_trace(go.Bar(y=dff['Estimate'],
                         x=dff['QuestionText'],
                         error_y=dict(type="data", array=dff["CI Upper"]-dff["Estimate"]), # need to vectorize subtraction
                         # hover_data =['Annotation'],
                         marker=dict(color="#c8102e"),
                         hovertext=dff['Annotation'],
                         text=dff.Estimate.map(str)+"%",
                         textposition='inside',
                         insidetextanchor='start',
                         )
                  )

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

def don_rate_avg_don_by_prov(DonRates_2018, AvgTotDon_2018):
    fig1df1 = DonRates_2018[DonRates_2018['Group'] == "All"]
    fig1df1 = fig1df1[fig1df1.Province.notnull()]

    fig1df2 = AvgTotDon_2018[AvgTotDon_2018['Group'] == "All"]
    fig1df2 = fig1df2[fig1df2.Province.notnull()]
    
    fig1 = go.Figure()

    fig1.add_trace(go.Bar(x=fig1df1['Region'],
                        y=fig1df1['Estimate'],
                        error_y=dict(type="data", array=fig1df1["CI Upper"]-fig1df1["Estimate"]),
                        hovertext=fig1df1['Annotation'],
                        marker=dict(color="#c8102e"),
                        text=fig1df1.Estimate.map(str)+"%",
                        textposition='inside',
                        insidetextanchor='start',
                        name="Donor rate",
                        yaxis='y2',
                        offsetgroup=2
                        ),
                )

    fig1.add_trace(go.Bar(x=fig1df2['Region'],
                        y=fig1df2['Estimate'],
                        error_y=dict(type="data", array=fig1df2["CI Upper"]-fig1df2["Estimate"]), # need to vectorize subtraction
                        hovertext =fig1df2['Annotation'],
                        marker=dict(color="#7BAFD4"),
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
    fig1.update_traces(error_y_color="#757575")

    # Aesthetics for fig
    fig1.update_yaxes(showgrid=False, showticklabels=False)

    fig1.update_layout(height=400, margin={'l': 30, 'b': 30, 'r': 10, 't': 10})

    return fig1

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
                         marker=dict(color="#7BAFD4"),
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
                         marker=dict(color="#c8102e"),
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
                         marker=dict(color="#7BAFD4"),
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
                         marker=dict(color="#c8102e"),
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
                     marker=dict(color="#7BAFD4"),
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
                     marker=dict(color="#c8102e"),
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