# from cv2 import dft
import pandas as pd
import numpy as np
import json
import os
import logging


base = 'Tickers/'
ticker = 'GE'
filename = base + ticker + '.csv'
datafile = filename

def initialize_dataframe(datafile):
    # # Date will be index
    data = pd.read_csv(datafile, index_col = 'Date')

    # Converting the dates from string to datetime format:
    # Keep as time for intraday future data
    # data.index = pd.to_datetime(data.index)
    data.index = pd.to_datetime(data.index, utc=False)

    # data.index = data.index.date
    # Check types
    # data.dtypes
    # data.shape

    return data


def format_ticker_url(ticker, base=None):
    base = 'Tickers/'
    result = "{}{}.csv".format(base, ticker)
    return result

def get_buy_dates(df):
    buy_dates = (df['Position'] == 1) & (df['Position'].shift(1) == 0)
    buy_axis_y= df.SMA[buy_dates]
    return buy_axis_y

def get_sell_dates(df):
    sell_dates = (df['Position'] == 0) & (df['Position'].shift(1) == 1)
    sell_axis_y = df.SMA[sell_dates]
    return sell_axis_y

def load_strategy(strategy_name, base_path='Strategies/'):
    with open(base_path + strategy_name + '.json') as json_file:
        data = json.load(json_file)
        return data

# Load strategy SMA/EMA for Basic Trading SMA cross
def create_strategy_consts_1(df, sma, ema):
    # Parse strategy constants from strategy selected strategy JSON 
    # Add columns for EWM, SMA, SHORT, MED, LONG
    # logging.info("Creating strategy constants for {}".format(strategy['strategy_name']))
    # Parse SMA/EMA values from strategy JSON
    SMA_CONST = int(sma)
    EMA_CONST = int(ema)

    # Create new columns for SMA & EMA
    # Simple Moving Average:
    # Exponential Weighted Average
    df['SMA'] = df['Adj Close'].rolling(SMA_CONST).mean()
    df['EMA'] = df['Adj Close'].ewm(span=EMA_CONST).mean()

    # Load Short/Med/Long Term 50/100/200 to look for Bullish Breakout
    # Parse SHORT/MED/LONG term values from strategy JSON
    STANDARD_SHORT_TERM = int(50)
    STANDARD_MED_TERM = int(100)
    STANDARD_LONG_TERM = int(200)

    # Create new columns for SHORT/MED/TERM from parsed Strategy JSON
    df['SMA_ST'] = df['Adj Close'].rolling(STANDARD_SHORT_TERM).mean()
    df['SMA_MT'] = df['Adj Close'].rolling(STANDARD_MED_TERM).mean()
    df['SMA_LT'] = df['Adj Close'].rolling(STANDARD_LONG_TERM).mean()

    df.dropna(inplace=True)

    return df
# Load strategy SMA/EMA for Basic Trading SMA cross
def create_strategy_consts(df, strategy):
    # Parse strategy constants from strategy selected strategy JSON 
    # Add columns for EWM, SMA, SHORT, MED, LONG
    # logging.info("Creating strategy constants for {}".format(strategy['strategy_name']))
    # Parse SMA/EMA values from strategy JSON
    SMA_CONST = int(strategy['movingAverages']['SMA']['val'])
    EMA_CONST = int(strategy['movingAverages']['EMA']['val'])

    # Create new columns for SMA & EMA
    # Simple Moving Average:
    # Exponential Weighted Average
    df['SMA'] = df['Adj Close'].rolling(SMA_CONST).mean()
    df['EMA'] = df['Adj Close'].ewm(span=EMA_CONST).mean()

    # Load Short/Med/Long Term 50/100/200 to look for Bullish Breakout
    # Parse SHORT/MED/LONG term values from strategy JSON
    STANDARD_SHORT_TERM = int(strategy['standardAverages'][0])
    STANDARD_MED_TERM = int(strategy['standardAverages'][1])
    STANDARD_LONG_TERM = int(strategy['standardAverages'][2])

    # Create new columns for SHORT/MED/TERM from parsed Strategy JSON
    df['SMA_ST'] = df['Adj Close'].rolling(STANDARD_SHORT_TERM).mean()
    df['SMA_MT'] = df['Adj Close'].rolling(STANDARD_MED_TERM).mean()
    df['SMA_LT'] = df['Adj Close'].rolling(STANDARD_LONG_TERM).mean()

    df.dropna(inplace=True)

    return df

def create_buy_signals(df):
    buy_dates = (df['Position'] == 1) & (df['Position'].shift(1) == 0)
    buy_date_x = df.index[buy_dates, 'SMA']
    return buy_date_x

def create_signals_breakout(df):

    buy_signals = (df['Position'] == 1) & (df['Position'].shift(1) == 0) # Find True and makes sure previous day was False
    df.loc[buy_signals].round(3)

    buy_signals_prev = (df['Position'].shift(-1) == 1) & (df['Position'] == 0)
    df.loc[buy_signals | buy_signals_prev].round(3)

    buy_signals_after = (df['Position'].shift(1) == 1) & (df['Position'] == 0)
    df.loc[buy_signals | buy_signals_prev | buy_signals_after].round(3)

    breakout_position = np.where(df['SMA_MT'] > df['SMA_ST'], 1, 0)
    df['Breakout'] = breakout_position

    breakout_signals = (df['Breakout'] == 1) & (df['Breakout'].shift(1) == 0)
    df.loc[breakout_signals].round(3)

    return df

def create_buy_hold(df):
    # The returns of the Buy and Hold strategy:
    df['Hold'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
    # The returns of the Moving Average strategy:
    df['Strategy'] = df['Position'].shift(1) * df['Hold']
    # We need to get rid of the NaN generated in the first row:
    df.dropna(inplace=True)
    return df

def get_stock_df(symbol, sma=20, ema=100):
    ticker = format_ticker_url(symbol) 
    data = initialize_dataframe(ticker)
    df = data.copy()  
    df = df['2010':]
    STRAT_DIR = 'Strategies/'
    strategy = load_strategy("BasicStrategy", base_path=STRAT_DIR)
    # df = create_strategy_consts(df, strategy)
    df = create_strategy_consts_1(df, sma, ema)
    long_positions = np.where(df['EMA'] > df['SMA'], 1, 0)
    df['Position'] = long_positions
    print(df['Position'].sum())
    
    # df = create_signals_breakout(df)

    df = create_buy_hold(df)
    print(get_text_results(df))

    return df

def get_text_results(df):
    returns = np.exp(df[['Hold', 'Strategy']].sum()) - 1
    print(f"Buy and hold return: {round(returns['Hold']*100,2)}%")
    a =     f"Buy and hold return: {round(returns['Hold']*100,2)}%"
    print(f"Strategy return: {round(returns['Strategy']*100,2)}%")
    b =    f"Strategy return: {round(returns['Strategy']*100,2)}%"
    a = str(a)
    b = str(b)
    return [a,b]

def merge_buy_and_sell_dates(df):
    bdates = get_buy_dates(df)

    bdates.name = 'sma'
    bdates = bdates.to_frame()
    bdates['Type'] = 'Buy'

    sdates = get_sell_dates(df)
    sdates.name = 'sma'
    sdates = sdates.to_frame()
    sdates['Type'] = 'Sell'
    df = pd.concat([bdates,sdates])
    # df = pd.concat([bdates,sdates],axis=1,)
    # df = df.bfill(axis=1).iloc[:, 0]
    df = df.sort_values('Date')
    # print(df)

    return df

if __name__ == "__main__":
    # select ticker
    symbol = 'GE'

    # format ticker for data shaping
    ticker = format_ticker_url(symbol) 
    df = get_stock_df('GE')
    # bdates = get_buy_dates(df)
    # bdates.name = 'Buy Signal'
    # sdates = get_sell_dates(df)
    # sdates.name = 'Sell Signal'
    # df = pd.concat([bdates,sdates],axis=1)
    # # df = pd.concat([bdates,sdates],axis=1,)
    # df = df.bfill(axis=1).iloc[:, 0]
    merge_buy_and_sell_dates(df)



