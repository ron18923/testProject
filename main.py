import gemini
from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze

# TODO - optimize params

OPEN_TRADE = False
TIME_EXPRESSION = 0
IS_SMA_BELOW = False

CMO_PERIOD = 9
SMA_PERIOD = 25
PAIR = "BTC_USDT"
DAYS_HISTORY = 75

"""
PERIOD ALLOWED VALUES:
-number - period in sec-
    * 300 - 5M
    * 900 - 15M
    * 1800 - 30M
    * 7200 - 2H
    * 14400 - 4H
    * 86400 - 1D
"""
PERIOD = 300


OVERBOUGHT_VALUE = 50
OVERSOLD_VALUE = -50

"""
DATA FREQUENCY ALLOWED VALUES:
    * T - minute (15T - 15 minutes),
    * H - hour,
    * D - day,
    * W - week,
    * M - month
"""
params = {
    'capital_base': 1000,
    'data_frequency': '5T',
    'fees': {
        'open_fee': 0.0001,
        'close_fee': 0.0001
    }
}


def cmo_logic(data, cmo_period):
    first_day = len(data) - cmo_period
    last_day = len(data)
    higher_close_price = 0
    lower_close_price = 0

    for ticker in range(first_day, last_day):
        if data['close'][ticker] > data['open'][ticker]:
            higher_close_price += 1
        elif data['close'][ticker] < data['open'][ticker]:
            lower_close_price += 1

    cmo = ((higher_close_price - lower_close_price) / (higher_close_price + lower_close_price)) * 100

    return cmo


def sma_logic(data, sma_period):
    # TODO make it more accurate to what shows on 'poloniex.com'
    first_day = len(data) - sma_period
    last_day = len(data)
    averages_sum = 0

    for ticker in range(first_day, last_day):
        average = data["high"][ticker] - (data["high"][ticker] - data["low"][ticker]) / 2.0
        averages_sum += average
    return averages_sum / sma_period


def trading_strategy(gemini: Gemini, data):
    global IS_SMA_BELOW

    if sma_logic(data, SMA_PERIOD) < data["close"][len(data)-1] and not IS_SMA_BELOW:
        IS_SMA_BELOW = True
        return


if __name__ == '__main__':
    data_df = poloniex.load_dataframe(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

    trading_strategy(gemini, data_df)
    backtesting_engine = Gemini(logic=trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)
    backtesting_engine.run(data=data_df)

# def cmo_trading_strategy(gemini: Gemini, data):
#     global OPEN_TRADE
#     global TIME_EXPRESSION
#
#     if len(data) >= CMO_PERIOD and (not OPEN_TRADE):
#         cmo = cmo_logic(data, CMO_PERIOD)
#         assert -100 <= cmo <= 100, "CMO value can't be less than a -100 and more than a 100"
#
#         if cmo < OVERSOLD_VALUE:
#             gemini.account.enter_position(type_="Short",
#                                           entry_capital=params['capital_base'] * 0.1,
#                                           entry_price=data.iloc[-1]['high'])
#             TIME_EXPRESSION = len(data)
#             OPEN_TRADE = True
#         # elif cmo > OVERBOUGHT_VALUE:
#
#     elif TIME_EXPRESSION + 1 <= len(data):
#         gemini.account.close_position(position=gemini.account.positions[0],
#                                       percent=1,
#                                       price=data.iloc[-1]['low'])
#         OPEN_TRADE = False
