import math

import gemini
from gemini.gemini_core.exchange import OpenedTrade
from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze

# TODO - optimize params

PAIR = "BTC_USDT"
DAYS_HISTORY = 1

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


def order_by_size(num1, num2):
    # ordering 2 numbers by size. first number is the larger one.
    list.append(num1)
    list.append(num2)
    list.sort()
    list.index()
    return list


def similarity_between_two_candles(first_candle, second_candle):
    open_list = []
    close_list = []
    high_list = []
    low_list = []
    # based on: https://developers.google.com/machine-learning/clustering/similarity/manual-similarity
    open_list.append(first_candle["open"])
    close_list.append(first_candle["close"])
    high_list.append(first_candle["high"])
    low_list.append(first_candle["low"])

    open_list.append(second_candle["open"])
    close_list.append(second_candle["close"])
    high_list.append(second_candle["high"])
    low_list.append(second_candle["low"])

    open_list.sort(reverse=True)
    close_list.sort(reverse=True)
    high_list.sort(reverse=True)
    low_list.sort(reverse=True)

    open_diff_pow = (1-(open_list.__getitem__(len(open_list)-1)/open_list.__getitem__(0))) ** 2
    close_diff_pow = (1-(close_list.__getitem__(len(close_list)-1)/close_list.__getitem__(0))) ** 2
    high_diff_pow = (1-(high_list.__getitem__(len(high_list)-1)/high_list.__getitem__(0))) ** 2
    low_diff_pow = (1-(low_list.__getitem__(len(low_list)-1)/low_list.__getitem__(0))) ** 2

    return 1-math.sqrt((open_diff_pow + close_diff_pow + high_diff_pow + low_diff_pow) / 4)


def trading_strategy(gemini: Gemini, data):
    last_candle = data_df.iloc[len(data) - 1]
    second_last_candle = data_df.iloc[len(data) - 2]

    similarity_between_two_candles(last_candle, second_last_candle)
    pass


if __name__ == '__main__':
    data_df = poloniex.load_dataframe(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

    backtesting_engine = Gemini(logic=trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)
    backtesting_engine.run(data=data_df)
