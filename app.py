import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Not sure what this is, only used in line 9 below
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read in example data from URL
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

excluded_names = [
    'Arab World',
    'Caribbean small states',
    'Central Europe and the Baltics',
    'Early-demographic dividend',
    'East Asia & Pacific',
    'East Asia & Pacific (excluding high income)',
    'East Asia & Pacific (IDA & IBRD countries)',
    'Euro area',
    'Europe & Central Asia',
    'Europe & Central Asia (excluding high income)',
    'Europe & Central Asia (IDA & IBRD countries)',
    'European Union',
    'Fragile and conflict affected situations',
    'Heavily indebted poor countries (HIPC)',
    'High income',
    'IBRD only',
    'IDA & IBRD total',
    'IDA blend',
    'IDA only',
    'IDA total',
    'Late-demographic dividend',
    'Latin America & Caribbean',
    'Latin America & Caribbean (excluding high income)',
    'Latin America & the Caribbean (IDA & IBRD countries)',
    'Least developed countries: UN classification',
    'Low & middle income',
    'Low income',
    'Lower middle income',
    'Middle East & North Africa',
    'Middle East & North Africa (excluding high income)',
    'Middle East & North Africa (IDA & IBRD countries)',
    'Middle income',
    'North America',
    'Not classified',
    'OECD members',
    'Other small states',
    'Pacific island small states',
    'Post-demographic dividend',
    'Pre-demographic dividend',
    'Small states',
    'South Asia',
    'South Asia (IDA & IBRD)',
    'Sub-Saharan Africa',
    'Sub-Saharan Africa (excluding high income)',
    'Sub-Saharan Africa (IDA & IBRD countries)',
    'Upper middle income'
]

# Function to extract info for country_names below
# Note: this is just a quick solution, in future this will be more streamlined
def generateNames():
    countries = []
    for d in df['Country Name'].unique():
        if d not in excluded_names:
            countries.append(d)
        else:
            pass
    return countries

# Extract info from data for selection menus
available_indicators = df['Indicator Name'].unique()
country_names = generateNames()

# General app layout/set up
app.layout = html.Div([
    # TOP/PAGE LEVEL
    html.Div([
        # Page title
        html.H1('Test Interface'),
        # Page level filter (dropdown menu); shows up just under title vertically
        html.Div([
            dcc.Dropdown(
                # Object id (used to reference object within interface backend/code)
                id='country-selection',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in country_names],
                # Default value, shows up at top of dropdown list
                value='World'
            ),
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ]),
    # SECOND ROW (graph level)
    html.Div([
        # Left dropdown menu
        html.Div([
            dcc.Dropdown(
                # Object id (used to reference object within interface backend/code)
                id='crossfilter-xaxis-column',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in available_indicators],
                # Default value, shows up at top of dropdown list
                value='Fertility rate, total (births per woman)'
            ),
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        # Right dropdown menu
        html.Div([
            dcc.Dropdown(
                # Object id (used to reference object within interface backend/code)
                id='crossfilter-yaxis-column',
                # Dropdown menu options
                options=[{'label': i, 'value': i} for i in available_indicators],
                # Default value, shows up at top of dropdown list
                value='Life expectancy at birth, total (years)'
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'padding': '10px 5px'
    }),
    # Left graph
    html.Div([
        # ID for use with below function implementation
        dcc.Graph(id='left-time-series',)
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    # Right graph
    html.Div([
        # ID for use with below function implementation
        dcc.Graph(id='right-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),


])

# Function: create time series graph
def create_time_series(dff, title):

    # Scatter plot - data frame, x label, y label
    fig = px.scatter(dff, x='Year', y='Value')

    # Aesthetics for fig
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

# Interaction?
@app.callback(
    # Changes left graph...
    dash.dependencies.Output('left-time-series', 'figure'),
    [
    # ...according to input from top (page level) and left (graph level) drop downs
     dash.dependencies.Input('country-selection', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     ])
# TODO: How does this get activated???
def update_y_timeseries(country, xaxis_column_name):
    dff = df[df['Country Name'] == country]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country, xaxis_column_name)
    # Uses above function
    return create_time_series(dff, title)


@app.callback(
    # Changes right graph...
    dash.dependencies.Output('right-time-series', 'figure'),
    [
    # ...according to input from top (page level) and left (graph level) drop downs
    dash.dependencies.Input('country-selection', 'value'),
    dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     ])
# TODO: How does this get activated???
def update_x_timeseries(country, yaxis_column_name):
    dff = df[df['Country Name'] == country]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    # Uses above function
    return create_time_series(dff, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)
