from dash import Dash, dcc, html, dash_table, Input, Output
#import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd; import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.options.display.max_rows = 10

df = pd.read_excel('GDP by Expenditure and Income Approach 2021 -2022 (1).xlsx')
df.rename(columns={'TABLE 8             ':'TABLE8'}, inplace=True)
df = df.dropna(how='all')
df = df.set_index('TABLE8')
df = df.T
df = df.fillna(method='ffill')
dff = df.iloc[ : , [0, 1, 3, 4, 5, 6]]


df2 = pd.read_excel('gdp_WORLDBANK_2022.07.11.xlsx', skiprows=4)
df2['WHO Ind'] = df2['WHO Ind'].fillna(method='ffill')

df2.drop('Series Code', inplace=True, axis=1)

df2 = df2.loc[df2['Country Code'].isin(['NGA'])]
df2 = df2.set_index('WHO Ind')

df2 = df2.loc[: , 'YR1985':]
df2 = df2.T

df2['percentage'] = df2.div(df2.sum())


df2.index.name = 'Year'
df2 = df2.reset_index()

k = df2.sort_values(by='percentage', ascending=False)[:7]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(children=[
        dbc.Container([    
        dbc.Row([
        html.Div(children=[html.H4("Analysis of Nigeria's GDP PER CAPITA from the year 1985 to the year 2021")]),
        dbc.Col(dcc.Graph(figure=px.bar(df2, x='percentage', y='Year', color='Year', title='GDP PER CAPITA from the year 1985 to the year 2021'))),
        dbc.Col(dcc.Graph(figure=px.bar(k, x='percentage', y='Year', color='Year', title='Top seven years with the highest GDP PER CAPITA')))
    ]),
    
    html.Div(children=[html.H4("Analysis of Nigerian GDP by Expenditure and Income Approach 2021 -2022")]),
    dbc.Row([
    dbc.Col(dcc.Graph(id="graph1")),
    dbc.Col(dcc.Graph(id='graph2'))
    ]),
    html.P("Filter:"),
    html.P("Amount Of Expenditures:"),
    html.Div(children=[dcc.Dropdown(id='values',
        options=["FINAL CONSUMPTION EXPENDITURE OF HOUSEHOLD", "FINAL CONSUMPTION EXPENDITURE OF NON-PROFIT INSTITUTIONS SERVING HOUSEHOLD", "FINAL CONSUMPTION EXPENDITURE OF GENERAL GOVERNMENT", "              Individual Cosumption Expenditure of general government"],
        value='FINAL CONSUMPTION EXPENDITURE OF HOUSEHOLD', clearable=False
    )], style={'width':700})
])
], style={'background-color':'lightblue'} )
@app.callback(
    [Output("graph1", "figure"), Output('graph2', 'figure')], 
    #Input("names", "value"), 
    Input("values", "value"))
def generate_chart(values): 
    fig1 = px.pie(dff, values=values, names="GROSS DOMESTIC PRODUCT AND EXPENDITURE AT CURRENT", hole=.3, color_discrete_sequence=px.colors.sequential.RdBu)
    #fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    #fig.add_trace(go.Pie(labels=dff["GROSS DOMESTIC PRODUCT AND EXPENDITURE AT CURRENT"], values=values, name="GHG Emissions"),
    #          1, 1)
    #fig.add_trace(go.Pie(labels=dff["PURCHASERS' VALUE"], values=values, name="CO2 Emissions"),
    #          1, 2)
    fig2 = px.pie(dff, values=values, names="PURCHASERS' VALUE", hole=.3, color_discrete_sequence=px.colors.sequential.RdBu)
    
    fig1.update_layout(
    title_text="Gross domestic product and expenditure at current"
    )
    
    fig2.update_layout(
    title_text="Purchasers' value"
    )
    
    
    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)