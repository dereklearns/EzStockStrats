from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from data_transformations import get_buy_dates, get_stock_df, get_sell_dates, merge_buy_and_sell_dates


import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

# df = merge_buy_and_sell_dates(get_stock_df('GE'))
df = merge_buy_and_sell_dates(get_stock_df('GE')).reset_index()

colors = {
    'background': '#111111',
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
    dcc.Dropdown(['GE', 'JNJ', 'MSFT'], 'GE', id='input_dropdown'),
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
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            fill_width=False),


    ])

])

@app.callback(
    Output('line-chart-1', 'figure'),
    Input('input_dropdown', 'value'))
def update_figure(selected_stock):
    filtered_df = get_stock_df(selected_stock)
    # print (filtered_df.head(10))


    # buy_dates = (filtered_df['Position'] == 1) & (filtered_df['Position'].shift(1) == 0)
    # buy_signals= filtered_df.SMA[buy_dates]
    # buy_date_x = buy_signals.index
    buy_signals = get_buy_dates(filtered_df)
    sell_signals = get_sell_dates(filtered_df)

    # for index, row in buy_signals.items():
    #     print (index,row)
  
    # buy_dates = (filtered_df['Position'] == 1) & (filtered_df['Position'].shift(1) == 0)
    # # print(filtered_df.index[buy_dates])
    # buy_date_x = filtered_df.index[buy_dates]
    # buy_date_y = filtered_df['SMA'] * filtered_df['Position'][buy_dates]
    # print(buy_date_y)

    # sma200 = filtered_df['sma200']
    # print(buy_dates)

    fig = px.line(
        filtered_df, 
        x= filtered_df.index, 
        y="Adj Close", title='Stock Chart for: {}'.format(selected_stock))


    # for index, sma in buy_axis_y.items():
    #     # print(date)
    #     fig.add_annotation(x=str(index), y=sma, showarrow=True, arrowhead=1, arrowwidth=3, align="center", arrowcolor="green", yshift = 30)

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

    # fig.add_vline(
    #     x=, line_width=3, line_dash="dash", 
    #     line_color="green")
    for index, sma in sell_signals.items():
        # print(date)
        fig.add_vline(
            x=str(index), line_width=3, line_dash="dash", 
            line_color="red")
    for index, sma in buy_signals.items():
        # print(date)
        fig.add_vline(
            x=str(index), line_width=3, line_dash="dash", 
            line_color="green")
        # fig.add_annotation(x=str(index), y=sma, showarrow=True, arrowhead=2, arrowwidth=3, align="center", arrowcolor="green", yshift = 30)

    fig.update_layout(transition_duration=100)



    return fig


@app.callback(
    Output('table-chart-1', 'data'),
    Input('input_dropdown', 'value'))
def update_figure(selected_stock):
    filtered_df = get_stock_df(selected_stock)
    buy_signals = get_buy_dates(filtered_df)
    sell_signals = get_sell_dates(filtered_df)
    # fig3 = dash_table.DataTable(filtered_df.to_dict('Avg Price'), [{"name": i, "id": i} for i in filtered_df.columns])
    # fig2 = px.line(
    #     filtered_df, 
    #     x= filtered_df.index, 
    #     y="Adj Close", title='Stock Chart for: {}'.format(selected_stock))
    # filtered_df = buy_signals + sell_signals
    merged = merge_buy_and_sell_dates(filtered_df)
    # print(merged)
    print(type(merged))
    merged = merged.reset_index()

    table_df = merged.to_dict("rows")


    # print(table_df)
    # table_df = filtered_df.to_dict("rows")

    return table_df


if __name__ == '__main__':
    app.run_server(debug=True)