# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
df2 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

app.title = 'Дэшборд Sibur Challenge'


def generate_table(dataframe, max_rows=3):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

colors = {
    'background': '#222222',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(children='Прогноз цен ПЭТФ'),

    html.Div(children='''
        Интеракивный график прогноза цены ПЭТФ
    '''),

    dcc.Checklist(
    options=[
        {'label': 'SMA', 'value': 'SMA'},
        {'label': 'EMA', 'value': 'EMA'},
    ],
    value=['SMA', 'EMA'],
    labelStyle={'display': 'inline-block'}
    ),

    dcc.Input(id='my-id', value='initial value', type='text'),

    html.Div(id='my-div'),  

    html.Div([
    html.Div([html.H1("Ebola Cases Reported in Africa - 2014")], style={"textAlign": "center"}),
    dcc.Graph(id="my-graph-pie"),
    html.Div([dcc.Slider(id='month-selected', min=3, max=12, value=8,
                         marks={3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September",
                                10: "October", 11: "November", 12: "December"})],
             style={'textAlign': "center", "margin": "30px", "padding": "10px", "width": "65%", "margin-left": "auto",
                    "margin-right": "auto"}),
    ], className="container"),


    ###График из jypiter





    dcc.Graph(
    figure=dict(
        data=[
            dict(
                x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003
                ],
                y=[219, 146, 112, 127, 124, 180, 236, 207, 236],
                name='Исторические данные',
                marker=dict(
                    color='rgb(55, 83, 109)'
                )
            ),
            dict(
                x=[
                   2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                y=[236, 88, 105, 156, 270,
                   299, 340, 403, 549, 499],
                name='Прогноз',
                marker=dict(
                    color='rgb(26, 118, 255)'
                )
            )
        ],
        layout=dict(
            title='Прогноз цен ПЭТФ',
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=30)
        )
    ),
    style={'height': 300},
    id='my-graph-PETF'
    ),

    html.H4(children='Таблица прогнозных данных'),
    generate_table(df2)
])


@app.callback(
    Output("my-graph-pie", "figure"),
    [Input("month-selected", "value")]
    )

def update_graph(selected):
    return {
        "data": [go.Pie(labels=df1["Country"].unique().tolist(), values=df1[df1["Month"] == selected]["Value"].tolist(),
                        marker={'colors': ['#EF963B', '#C93277', '#349600', '#EF533B', '#57D4F1']}, textinfo='label')],
        "layout": go.Layout(title=f"Cases Reported Monthly", margin={"l": 300, "r": 300, },
                            legend={"x": 1, "y": 0.7})}


if __name__ == '__main__':
    app.run_server(debug=True)