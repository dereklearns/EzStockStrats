from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from data_transformations import get_buy_dates, get_stock_df, get_sell_dates, merge_buy_and_sell_dates, create_buy_hold


import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# df = merge_buy_and_sell_dates(get_stock_df('GE'))
df = merge_buy_and_sell_dates(get_stock_df('GE')).reset_index()

colors = {
    'background': '#ffffff',
    'text': '#7FDBFF'
}

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Stock Strategies',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Explore basic strategies.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(children=[dcc.Dropdown(['GE', 'JNJ', 'MSFT'], 'GE', id='input_dropdown')

                       ]),

    dcc.Slider(marks={i: str(i)
               for i in [3, 5, 8, 20, 50, 100]}, value=5, id='input-sma-1'),
    dcc.RadioItems([5, 8, 12, 20, 50, 100, 200], 100,
                   id='input-ema-1', labelStyle={'display': 'block'}),

    html.Div(style={"width": "75%"}, children=[

        dcc.Graph(
            id='line-chart-1'
        )]
    ),
    html.Div(style={"width": "75%"}, children=[
        dash_table.DataTable(
            id='table-chart-1',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict("rows"),
            style_table={'margin-left': '3vw', 'margin-top': '3vw'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            fill_width=False),


    ])

])


app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(html.Div(html.H1("EzStockStrats")))),

        dbc.Row(
            [
                dbc.Col(html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Underlying", className="card-title"),
                                html.H6("(SYMBOL/TICKER)",
                                        className="card-subtitle"),
                                html.P(
                                    "Commonly referred to as a ticker/symbol, the underlying for a traded company.",
                                    className="card-text",
                                ),
                                dcc.Dropdown(['GE', 'JNJ', 'MSFT'],
                                             'GE', id='input_dropdown')
                                # dcc.RadioItems([5, 8, 12, 20, 50, 100, 200], 100, id='input-ticker-1', labelStyle={'display': 'block'}),
                            ]
                        )
                        #                     ,
                        # style={"width": "18rem"},
                    ),



                )),

                dbc.Col(html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Simple Moving Average",
                                        className="card-title"),
                                html.H6("(SMA)", className="card-subtitle"),
                                html.P(
                                    "Non-weighted moving average of an underlying."
                                    "Select the # of days below for the SMA.",
                                    className="card-text",
                                ),
                                dcc.RadioItems(
                                    [5, 8, 12, 20, 50, 100, 200], 100, id='input-sma-1', labelStyle={'display': 'block'}),
                            ]
                        )
                        # ,
                        #     # style={"width": "18rem"},
                    ),


                )),

                dbc.Col(html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Exponential Moving Average",
                                        className="card-title"),
                                html.H6("(EMA)", className="card-subtitle"),
                                html.P(
                                    "Weighted moving average of an underlying."
                                    "Select the # of days below for the EMA.",
                                    className="card-text",
                                ),
                                dcc.RadioItems(
                                    [5, 8, 12, 20, 50, 100, 200], 100, id='input-ema-1', labelStyle={'display': 'block'}),
                            ]
                        )
                        #                     ,
                        # style={"width": "18rem"},
                    ),



                )),

                dbc.Col(html.Div("One of three columns"), id="the-results"),
            ]
        ),

        dbc.Row([
            dbc.Col(

                html.Div(
                    dcc.Graph(
                        id='line-chart-1'
                    ))),

            dbc.Col(
                html.Div(children=[
                    dash_table.DataTable(
                        id='table-chart-1',
                        columns=[{'name': i, 'id': i} for i in df.columns],
                        data=df.to_dict("rows"),
                        style_table={'margin-left': '3vw',
                                     'margin-top': '3vw'},
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{Type} = Buy',
                                    # 'column_id': 'Type'
                                },
                                'backgroundColor': '#3D9970',
                                'color': 'white',
                                # 'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Type} = Sell',
                                    # 'column_id': 'Type'
                                },
                                'backgroundColor': 'tomato',
                                'color': 'white',
                                # 'fontWeight': 'bold'
                            }

                        ],
                        fill_width=False),
                ]))
        ])
    ]
)

@app.callback(
    Output('line-chart-1', 'figure'),
    Input('input_dropdown', 'value'),
    Input('input-sma-1', 'value'),
    Input('input-ema-1', 'value'))
def update_figure(selected_stock, sma, ema):
    filtered_df = get_stock_df(selected_stock, sma, ema)

    buy_signals = get_buy_dates(filtered_df)
    sell_signals = get_sell_dates(filtered_df)

    fig = px.line(
        filtered_df,
        x=filtered_df.index,
        y="Adj Close", title='Stock Chart for: {}'.format(selected_stock))

    '''
    fig.add_annotation(x=2, y=5,
            text="Text annotation with arrow",
            showarrow=True,
            arrowhead=1)
    
    '''

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df['Adj Close'], name="Price",
                             line_shape='linear'))
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df['SMA'], name="SMA",
                             line_shape='linear'))
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df['EMA'], name="EMA",
                             line_shape='linear'))

    for index, sma in sell_signals.items():
        fig.add_vline(
            x=str(index), line_width=3, line_dash="dash",
            line_color="red")
    for index, sma in buy_signals.items():
        fig.add_vline(
            x=str(index), line_width=3, line_dash="dash",
            line_color="green")

    fig.update_layout(transition_duration=100)

    return fig


@app.callback(
    Output('table-chart-1', 'data'),
    Input('input_dropdown', 'value'),
    Input('input-sma-1', 'value'),
    Input('input-ema-1', 'value'))
def update_figure(selected_stock, sma, ema):
    filtered_df = get_stock_df(selected_stock, sma, ema)
    buy_signals = get_buy_dates(filtered_df)
    sell_signals = get_sell_dates(filtered_df)

    merged = merge_buy_and_sell_dates(filtered_df)
    merged = merged.reset_index()

    table_df = merged.to_dict("rows")

    return table_df







if __name__ == '__main__':
    app.run_server(debug=True)
