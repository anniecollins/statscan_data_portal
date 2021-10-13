import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

from Utils.graphs.who_donates_how_much_graph_utils import *

###################### App setup ######################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Reading in data from public urls

# DonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-DonRate.csv")
DonRates_2018 = pd.read_csv("Tables/2018-DonRate.csv")
# AvgTotDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotDon.csv")
AvgTotDon_2018 = pd.read_csv("Tables/2018-AvgTotDon.csv")
AvgNumCauses_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgNumCauses.csv")
FormsGiving_2018 = pd.read_csv("Tables/2018-FormsGiving.csv")
TopCauseFocus_2018 = pd.read_csv("Tables/2018-TopCauseFocus.csv")
PropTotDon_2018 = pd.read_csv("Tables/2018-PercTotDonors.csv")
PropTotDonAmt_2018 = pd.read_csv("Tables/2018-PercTotDonations.csv")

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


# Add annotation, suppress estimates/CI bounds where necessary, round estimate values according to estimate type (as above)
# Annotation text
values = ["Use with caution", "Estimate suppressed", ""]

i = 0
while i < len(data):
    # Different marker values
    conditions = [data[i]["Marker"] == "*",
                  data[i]["Marker"] == "...",
                  pd.isnull(data[i]["Marker"])]
    # Assign annotation text according to marker values
    data[i]["Annotation"] = np.select(conditions, values)

    # Suppress Estimate and CI Upper where necessary (for visualizations and error bars)
    data[i]["Estimate"] = np.where(data[i]["Marker"]=="...", 0, data[i]["Estimate"])
    data[i]["CI Upper"] = np.where(data[i]["Marker"]=="...", 0, data[i]["CI Upper"])

    # Round rates and dollar amounts to zero decimal places
    data[i]['Estimate'] = data[i]['Estimate'].round(0)
    data[i]["CI Upper"] = data[i]["CI Upper"].round(0)
    i = i + 1

i = 0
while i < len(data_num):
    # Different marker values
    conditions = [data_num[i]["Marker"] == "*",
                  data_num[i]["Marker"] == "...",
                  pd.isnull(data_num[i]["Marker"])]
    # Assign annotation text according to marker values
    data_num[i]["Annotation"] = np.select(conditions, values)

    # Suppress Estimate and CI Upper where necessary (for visualizations and error bars)
    data_num[i]["Estimate"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["Estimate"])
    data_num[i]["CI Upper"] = np.where(data_num[i]["Marker"]=="...", 0, data_num[i]["CI Upper"])

    # Round number amounts to two decimal places
    data_num[i]['Estimate'] = data_num[i]['Estimate'].round(2)
    data_num[i]["CI Upper"] = data_num[i]["CI Upper"].round(2)
    i = i + 1

# Extract info from data for selection menus
region_names = np.array(['CA', 'CA (without QC)', 'AB', 'AT', 'BC', 'ON', 'PR', 'QC'], dtype=object)


fig1df1 = DonRates_2018[DonRates_2018['Group'] == "All"]
fig1df1 = fig1df1[fig1df1.Province.notnull()]

fig1df2 = AvgTotDon_2018[AvgTotDon_2018['Group'] == "All"]
fig1df2 = fig1df2[fig1df2.Province.notnull()]

fig2df = FormsGiving_2018[FormsGiving_2018['Group'] == "All"]
fig2df = fig2df[fig2df['Region'] == "CA"]


# ###################### Data processing ######################

# SubSecAvgDon_2018, SubSecDonRates_2018, DonRates_2018, AvgTotDon_2018,SubSecAvgNumDon_2018, AvgNumCauses_2018, AvgTotNumDon_2018 = get_data()

# data = [SubSecAvgDon_2018, SubSecDonRates_2018, DonRates_2018, AvgTotDon_2018] 
# data_num = [SubSecAvgNumDon_2018, AvgNumCauses_2018, AvgTotNumDon_2018] 

# # TODO: Move this to data_utils
# process_data(data)
# process_data(data_num)

# # Extract info from data for selection menus
# region_names = SubSecAvgDon_2018['Region'].unique()
# demo_names = SubSecAvgDon_2018['Group'].unique()

# # Remove "All" from demographic names (will cause visualization to not show if not removed since demographic group "All" has no values under "Attribute", which is the column used for x-axis values in the graohs)
# demo_names = np.delete(demo_names, 0)


###################### App layout ######################

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More blogs", header=True),
                    dbc.DropdownMenuItem("Blog 1", href="#"),
                    dbc.DropdownMenuItem("Blog 2", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="StatsCan Data Portal",
        brand_href="#",
        color="#c7102e",
        dark=True,
    ),
    html.Header([
        html.Div(className='overlay'),
        dbc.Container(
            dbc.Row(
                html.Div(
                    html.Div([
                        html.H1('Who Donates and How Much Do They Give?'),
                        html.Span(
                            'David Lasby',
                            className='meta'
                        )
                        ],
                        className='post-heading'
                    ),
                    className='col-md-10 col-lg-8 mx-auto position-relative'
                )
            )
        ),
    ], 
        # className='masthead'       
        className="bg-secondary text-white text-center py-4",
    ),
   dbc.Container(
       dbc.Row([
            html.Div(
                [
                    "Select a region of focus:",
                    dcc.Dropdown(
                        # Object id (used to reference object within callbacks)
                        id='region-selection',
                        # Dropdown menu options (region_names is nparray defined above
                        options=[{'label': i, 'value': i} for i in region_names],
                        # Default value, shows up at top of dropdown list and automatically filters graphs upon loading
                        value='ON',
                        style={'verticalAlign': 'middle'}
                        ),
                    html.Br(),   
                ], 
                className='col-md-10 col-lg-8 mx-auto mt-4'
            ),
            # Starting text
            html.Div(
                [
                    html.P("According to the 2018 General Social Survey on Giving, Volunteering, and Participating, almost nine in ten Canadians made some form of financial or in-kind contribution to charitable and nonprofit organizations during the one year period prior to the survey. Over two-thirds donated money (68%) or household goods, toys, and clothing (71%), and about half contributed food. Three percent said they have made a bequest to a nonprofit or charity in their will or via some other financial planning instrument. On average, those making financial donations to charities and nonprofits contributed $569 each, for a grand total of approximately $11.9 billion."),
                ], className='col-md-10 col-lg-8 mx-auto'
            ),
            # Forms of Giving
            html.Div(
                [
                    html.H4('Forms of Giving'),
                    dcc.Graph(id='FormsGiving', style={'marginTop': 50}),
                    html.P("The likelihood of making financial donations and the typical amounts donated vary according to where Canadians live. Broadly speaking, donation rates tend to be higher in the east while typical donation amounts tend to be higher in the west. More specifically, residents of Newfoundland and Labrador and Prince Edward Island were most likely to donate, while British Columbians were least likely. Those living in Western Canada, particularly Alberta, tended to donate larger amounts than average, while Quebeckers tended to make significantly smaller donations."),
                    html.Br(), 
                ], className='col-md-10 col-lg-8 mx-auto'
            ),
            # Donation rate & average donation amount by province
            html.Div(
                [
                    html.H4('Donation rate & average donation amount by province'),
                    dcc.Graph(id='DonRateAvgDonAmt-prv', figure=don_rate_avg_don_by_prov(DonRates_2018, AvgTotDon_2018), style={'marginTop': 50}),
                ], className='col-md-10 col-lg-8 mx-auto'
            ),
            # Key personal & economic characteristics
            html.Div(
                [
                    html.H3('Key personal & economic characteristics'),
                    html.P("In addition to varying according to where individuals live, donation patterns also tend to vary according to their personal and economic characteristics. Below we look at the demographic patterning of a number of key measures of donating, including:"),
                    html.Ul([
                        html.Li('Likelihood of donating and average amounts contributed by donors,'),
                        html.Li('Percentages of donors and total donation value contributed by each sub-group, and'),
                        html.Li('Average focus of donations on primary cause and the average number of causes supported. '),
                    ]),
                    html.P("Collectively, these measures present a detailed picture of the Canadian donor base, as well as the depth and breadth of the support it provides to charities and nonprofits. The text below describes national patterns and by default the graphs display national figures. Readers can interact with the graphs to show regional figures."),
                    # Gender
                    html.Div([
                        html.H5("Gender"),
                        html.P("At the national level, women are somewhat more likely to donate than men (72% vs. 64%). Men and women tend to donate very similar amounts, with the average gift sizes being virtually statistically indistinguishable. This trend is consistent across all regions."),
                        # Donation rate & average donation amount by gender 
                        html.Div([
                            html.H6("Donation rate & average donation amount by gender"),
                            dcc.Graph(id='DonRateAvgDonAmt-Gndr', style={'marginTop': 50}),
                            html.P("Reflecting their higher likelihood of donating, women account for a majority of donors, beyond their representation in the population (nationally, women accounted for 50.7% of the population 15 and over). Because men and women typically make very similar sized gifts, the proportions of total donations from each gender were very consistent with their representation among donors."),
                            html.Br(),
                        ]),
                        # Percentage of donors & total donation value by gender 
                        html.Div([
                            html.H6("Percentage of donors & total donation value by gender"),
                            dcc.Graph(id='PercDon-Gndr', style={'marginTop': 50}),
                            html.P("Looking at how donors tend to allocate their support across different causes, women and men have very similar degrees of focus on their primary cause. Nationally, both allocate just over three quarters of their financial support to their primary cause. While their degree of focus on the primary cause is quite similar, women are somewhat more likely to support secondary causes, as shown by the slightly higher average number of causes supported."),
                            html.Br(),
                        ]),
                        # Focus on primary cause & average number of causes supported by gender
                        html.Div([
                            html.H6("Focus on primary cause & average number of causes supported by gender"),
                            dcc.Graph(id='PrimCauseNumCause-Gndr', style={'marginTop': 50}),
                            html.Br(),
                        ]),  
                    ]),
                    # Age
                    html.Div([
                        html.H5("Age"),
                        html.P("As a general trend, both the likelihood of giving and the typical amounts donated tend to increase with age. Compared to overall giving levels, those aged 15 to 24 are less likely, those 25 to 54 about as likely, and those 55 and older somewhat more likely to donate, at least at the national level. The amounts typically contributed by donors in these age groups follow a broadly similar pattern."),
                        # Donation rate & average donation amount by age 
                        html.Div([
                            html.H6("Donation rate & average donation amount by age"),
                            dcc.Graph(id='DonRateAvgDonAmt-Age', style={'marginTop': 50}),
                            html.P("Because they are less likely to donate and tend to contribute smaller amounts, those 15 to 24 account for a relatively small proportion of donors and total donation value. In contrast, Canadians aged 55 and older play a disproportionately large role. Because of their higher likelihood of donating and generally larger donations, they account for higher percentages of total donation value than of donors across all age sub-groups."),
                            html.Br(),
                        ]),
                        # Percentage of donors & total donation value by age 
                        html.Div([
                            html.H6("Percentage of donors & total donation value by age"),
                            dcc.Graph(id='PercDon-Age', style={'marginTop': 100}),
                            html.P("Reflecting their smaller typical gift, those aged 15 to 24 tend to allocate more of their contributions on their primary cause and to support a smaller number of causes, on average. While donors aged 25 and older are quite consistent in their level of focus on their primary cause, they are somewhat more likely to support a broader range of causes, as indicated by increases in the average number of causes supported."),
                            html.Br(),
                        ]),
                        # Focus on primary cause & average number of causes supported by age
                        html.Div([
                            html.H6("Focus on primary cause & average number of causes supported by age"),
                            dcc.Graph(id='PrimCauseNumCause-Age', style={'marginTop': 100}),
                            html.Br(),
                        ]),  
                    ]),
                    # Formal Education
                    html.Div([
                        html.H5("Formal Education"),
                        html.P("Both the likelihood of donating and the typical amounts contributed increase with level of formal education attained. At the national level, those with a university degree were about 1.4 times as likely to donate than those with less than a high school diploma (76% vs. 54%). Likely reflecting their generally higher earnings, more highly educated donors also tend to contribute larger amounts. Nationally, the average donations of university-educated donors were about two and a half times larger than those without a high school diploma ($834 vs. $319)."),
                        # Donation rate & average donation amount by Formal Education 
                        html.Div([
                            html.H6("Donation rate & average donation amount by formal education"),
                            dcc.Graph(id='DonRateAvgDonAmt-Educ', style={'marginTop': 10}),
                            html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.  "),
                            html.Br(),
                        ]),
                        # Percentage of donors & total donation value by formal education 
                        html.Div([
                            html.H6("Percentage of donors & total donation value by formal education"),
                            dcc.Graph(id='PercDon-Educ', style={'marginTop': 10}),
                            html.P("As a result of their higher likelihood of donating and the typically larger amounts they donate, those with university degrees play a disproportionate role in donating. At the national level they account for about a third of donors, but contribute almost half of total donations. In contrast, those without a high school diploma account for about a tenth of donors and 6% of total donations."),
                            html.Br(),
                        ]),
                        # Focus on primary cause & average number of causes supported by formal education
                        html.Div([
                            html.H6("Focus on primary cause & average number of causes supported by formal education"),
                            dcc.Graph(id='PrimCauseNumCause-Educ', style={'marginTop': 10}),
                            html.P("While donors without a high school diploma focus slightly more of their donations on the primary cause, the degree of variation by level of formal eduction is low. Educational attainment does have an appreciable impact on the number causes of supported, almost certainly related to the increase in typical donation amounts with higher levels of formal education."),
                            html.Br(),
                        ]),  
                    ]),
                    # household income
                    html.Div([
                        html.H5("Income"),
                        html.P("The relationship between donating and household income is somewhat complex, due to the other personal characteristics those living in households with particular levels of income tend to possess. Broadly speaking, the likelihood of donating and the average amounts donated tend to increase with household income, though there are some fluctuations and the trend is most clearly seen towards the ends of the income spectrum. "),
                        # Donation rate & average donation amount by household income 
                        html.Div([
                            html.H6("Donation rate & average donation amount by household income"),
                            dcc.Graph(id='DonRateAvgDonAmt-Inc', style={'marginTop': 10}),
                            html.P("Driven by variations in the size of the typical donation, at the national level those who reside in households with annual incomes less than $75,000 tend to play disproportionately small roles in total donations. In contrast, those from households in the highest income category tend to play a much more significant role, accounting for under third of donors but two fifths of the total value of donations."),
                            html.Br(),
                        ]),
                        # Percentage of donors & total donation value by household income 
                        html.Div([
                            html.H6("Percentage of donors & total donation value by household income"),
                            dcc.Graph(id='PercDon-Inc', style={'marginTop': 50}),
                            html.Br(),
                        ]),
                        # Focus on primary cause & average number of causes supported by household income
                        html.Div([
                            html.P("Overall, the degree of focus on the primary cause supported tends to decrease as household income increases while the breadth of causes supported tends to increase."),
                            html.H6("Focus on primary cause & average number of causes supported by household income"),
                            dcc.Graph(id='PrimCauseNumCause-Inc', style={'marginTop': 50}),
                            html.Br(),
                        ]),  
                    ]),
                    # Religious attendance
                    html.Div([
                        html.H5("Religious Attendance"),
                        html.P("Participation in religious traditions has a very significant effect on both the likelihood of donating and the amounts donors typically contribute. Both the likelihood of donating and the average amounts contributed increase with the frequency of attendance at religious services. At the national level, donors attending religious services at least weekly were about a third again as likely to donate and, when they donated, they contributed nearly five times the amount, on amount, as those who never attend services. While many of the donations made by those attending services more frequently are allocated to religious organizations, this is not exclusively the case - for more detail, please refer to The Role of Religion in Giving elsewhere on this site."),
                        # Donation rate & average donation amount by religious attendance 
                        html.Div([
                            html.H6("Donation rate & average donation amount by religious attendance"),
                            dcc.Graph(id='DonRateAvgDonAmt-Relig', style={'marginTop': 10}),
                            html.P("Driven by their high likelihood of giving and particularly by the large amounts they tend to donate, weekly attenders account for just under half of the total value of donations at the national level, but just 17% of donors. In contrast, those who never attend services account for half of donors, but roughly one quarter of total donations."),
                            html.Br(),
                        ]),
                        # Percentage of donors & total donation value by religious attendance 
                        html.Div([
                            html.H6("Percentage of donors & total donation value by religious attendance"),
                            dcc.Graph(id='PercDon-Relig', style={'marginTop': 50}),
                            html.P("While weekly attenders allocate a somewhat higher proportion of their donations towards their primary cause (almost always religious organizations), they also tend to support a broader range of causes than do those who attend religious services very infrequently or not at all. Interestingly, monthly attenders have the lowest degree of focus on the primary cause and typically support the greatest number of causes. Perhaps unsurprisingly, given their low likelihood of donating and typically smaller donations, non-attenders tend to support the smallest number of causes and tend to be fairly focused on their primary cause."),
                            html.Br(),
                        ]),
                        # Focus on primary cause & average number of causes supported by religious attendance
                        html.Div([
                            html.Br(),
                            html.H6("Focus on primary cause & average number of causes supported by religious attendance"),
                            dcc.Graph(id='PrimCauseNumCause-Relig', style={'marginTop': 50}),
                            html.Br(),
                        ]),  
                    ]),
                    # Other personal & economic characteristics
                    html.Div([
                        html.H5("Other Personal & Economic Characteristics"),
                        html.P("Other significant personal and economic characteristics include marital status, labour force status and immigration status. In broad terms, those who are married or widowed are generally more likely to give and to give larger amounts, as are those who are employed or not in the labour force (many of those not in the labour force have retired). Looking at immigration status, native-born Canadians are somewhat more likely to give than those who immigrated to Canada, but New Canadians tend to give larger amounts. For more detail on the giving and volunteering of New Canadians, readers are referred to the Giving and Volunteering of New Canadians elsewhere on this website."),
                        # Donation rate & average donation amount by religious attendance 
                        html.Div([
                            html.H6("Donation rate & average donation amount by marital status"),
                            dcc.Graph(id='DonRateAvgDonAmt-MarStat', style={'marginTop': 10}),
                            html.Br(),
                        ]),
                        # Donation rate & average donation amount by labour force status
                        html.Div([
                            html.H6("Donation rate & average donation amount by labour force status"),
                            dcc.Graph(id='DonRateAvgDonAmt-Labour', style={'marginTop': 50}),
                            html.Br(),
                        ]),
                        # Donation rate & average donation amount by immigration status
                        html.Div([
                            html.H6("Donation rate & average donation amount by immigration status"),
                            dcc.Graph(id='DonRateAvgDonAmt-ImmStat', style={'marginTop': 50}),
                            html.P("Looking at the relative donation roles of the various sub-groups, those who are married or widowed tend to contribute disproportionately large proportions of total donations, while the smaller average donations made by single donors mean they account for a disproportionately small fraction of total donations. The relative role of donors does not vary significantly by labour force status, but New Canadians tend to play a slightly larger financial role in donations than their numbers would indicate."),
                            html.Br(),
                        ]),  
                        # Percentage of donors & total donation value by marital status
                        html.Div([
                            html.H6("Percentage of donors & total donation value by marital status"),
                            dcc.Graph(id='PercDon-MarStat', style={'marginTop': 10}),
                            html.Br(),
                        ]), 
                        # Percentage of donors & total donation value by labour force status
                        html.Div([
                            html.H6("Percentage of donors & total donation value by labour force status"),
                            dcc.Graph(id='PercDon-Labour', style={'marginTop': 50}),
                            html.Br(),
                        ]),   
                        # Percentage of donors & total donation value by immigration status
                        html.Div([
                            html.H6("Percentage of donors & total donation value by immigration status"),
                            dcc.Graph(id='PercDon-ImmStat', style={'marginTop': 50}),
                            html.Br(),
                            html.P("The degree to which Canadians focus on the primary cause they support does not seem to vary significantly according to their marital or labour force status. Married, widowed, and to a certain extent divorced Canadians tend to support a somewhat wider range of causes, as do those who are not in the labour force. Turning to immigration status, New Canadians and those residing in Canada who have not yet obtained landed immigrant status tend to focus more of their support on the primary cause and to support fewer causes than do native-born Canadians."),
                        ]),
                        # Focus on primary cause & average number of causes supported by marital status
                        html.Div([
                            html.H6("Focus on primary cause & average number of causes supported by marital status"),
                            dcc.Graph(id='PrimCauseNumCause-MarStat', style={'marginTop': 50}),
                            html.Br(),
                        ]), 
                        # Focus on primary cause & average number of causes supported by labour force status
                        html.Div([
                            html.H6("Focus on primary cause & average number of causes supported by labour force status"),
                            dcc.Graph(id='PrimCauseNumCause-Labour', style={'marginTop': 50}),
                            html.Br(),
                        ]),   
                        # Focus on primary cause & average number of causes supported by immigration status
                        html.Div([
                            html.H6("Focus on primary cause & average number of causes supported by immigration status"),
                            dcc.Graph(id='PrimCauseNumCause-ImmStat', style={'marginTop': 50}),
                            html.Br(),
                        ]),    
                    ]),
                ], className='col-md-10 col-lg-8 mx-auto'
    
            ),
        ]),     
   ),
   html.Footer(
       dbc.Container(
           dbc.Row(
               html.Div(
                   html.P('Copyright © Imagine Canada 2021',className="text-center"),
                   className='col-md-10 col-lg-8 mx-auto mt-5'
               ),
           )
       )
   )
])


###################### Callbacks ######################

@app.callback(
    dash.dependencies.Output('FormsGiving', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = FormsGiving_2018[FormsGiving_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "All"]

    title = '{}, {}'.format("Forms of giving", region)

    return forms_of_giving(dff1, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-Age', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by age group", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-Gndr', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by gender", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercDon-Gndr', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by gender", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-Gndr', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):

    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Gender"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Gender"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by gender", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    dash.dependencies.Output('PercDon-Age', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])

def update_graph(region):

    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by age", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-Age', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):

    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Age group"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Age group"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by age", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-Educ', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by education", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercDon-Educ', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by education", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-Educ', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):
    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Education"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Education"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by education", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-Inc', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by income", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercDon-Inc', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by income", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-Inc', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):

    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Personal income category"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Personal income category"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by income", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-Relig', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by religious attendance", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercDon-Relig', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by religious attendance", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-Relig', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):
    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Frequency of religious attendance"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Frequency of religious attendance"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by religious attendance", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-MarStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by marital status", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-Labour', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by employment status", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('DonRateAvgDonAmt-ImmStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = DonRates_2018[DonRates_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "Donation rate"

    dff2 = AvgTotDon_2018[AvgTotDon_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Average annual donations"

    title = '{}, {}'.format("Donor rate and average annual donation by immigration status", region)

    return don_rate_avg_don(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercDon-MarStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by marital status", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercDon-Labour', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by employment", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PercDon-ImmStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value')
    ])
def update_graph(region):
    dff1 = PropTotDon_2018[PropTotDon_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "Proportion of donors"

    dff2 = PropTotDonAmt_2018[PropTotDonAmt_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Percentage of donation value"

    title = '{}, {}'.format("Percentage of donors & total donation value by immigration status", region)

    return perc_don_perc_amt(dff1, dff2, name1, name2, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-MarStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):

    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Marital status"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Marital status"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by marital status", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-Labour', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):

    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Labour force status"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Labour force status"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by employment status", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)

@app.callback(
    dash.dependencies.Output('PrimCauseNumCause-ImmStat', 'figure'),
    [
        dash.dependencies.Input('region-selection', 'value'),
    ])
def update_graph(region):
    dff1 = AvgNumCauses_2018[AvgNumCauses_2018['Region'] == region]
    dff1 = dff1[dff1['Group'] == "Immigration status"]
    name1 = "Average number of causes"

    dff2 = TopCauseFocus_2018[TopCauseFocus_2018['Region'] == region]
    dff2 = dff2[dff2['Group'] == "Immigration status"]
    name2 = "Average concentration on first cause"

    title = '{}, {}'.format("Focus on primary cause & average number of causes supported by immigration status", region)

    return prim_cause_num_cause(dff2, dff1, name2, name1, title)


if __name__ == "__main__":
    app.run_server(debug=True)

