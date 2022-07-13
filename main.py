import logging
import math
import calculations as cl
import gemini
from gemini.gemini_core.exchange import OpenedTrade
from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze

# TODO - optimize params
import calculations

PAIR = "BTC_USDT"
DAYS_HISTORY = 100

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


# def similarity_between_two_candles(first_candle, second_candle):
#     open_list = []
#     close_list = []
#     high_list = []
#     low_list = []
#     # based on: https://developers.google.com/machine-learning/clustering/similarity/manual-similarity
#     open_list.append(first_candle["open"])
#     close_list.append(first_candle["close"])
#     high_list.append(first_candle["high"])
#     low_list.append(first_candle["low"])
#
#     open_list.append(second_candle["open"])
#     close_list.append(second_candle["close"])
#     high_list.append(second_candle["high"])
#     low_list.append(second_candle["low"])
#
#     open_list.sort(reverse=True)
#     close_list.sort(reverse=True)
#     high_list.sort(reverse=True)
#     low_list.sort(reverse=True)
#
#     open_diff_pow = (1 - (open_list.__getitem__(len(open_list) - 1) / open_list.__getitem__(0))) ** 2
#     close_diff_pow = (1 - (close_list.__getitem__(len(close_list) - 1) / close_list.__getitem__(0))) ** 2
#     high_diff_pow = (1 - (high_list.__getitem__(len(high_list) - 1) / high_list.__getitem__(0))) ** 2
#     low_diff_pow = (1 - (low_list.__getitem__(len(low_list) - 1) / low_list.__getitem__(0))) ** 2
#
#     return 1 - math.sqrt((open_diff_pow + close_diff_pow + high_diff_pow + low_diff_pow) / 4)
#     # Todo check if dividing in integer makes the float number into integer


# def similarity_between_four_candles(list_candles):
#     if len(list_candles) != 4:
#         logging.warning("list should include 4 candles!")
#         return
#
#     open_list = []
#     close_list = []
#     high_list = []
#     low_list = []
#     # based on: https://developers.google.com/machine-learning/clustering/similarity/manual-similarity
#     for candle in list_candles:
#         open_list.append(candle["open"])
#         close_list.append(candle["close"])
#         high_list.append(candle["high"])
#         low_list.append(candle["low"])
#
#     open_list.sort(reverse=True)
#     close_list.sort(reverse=True)
#     high_list.sort(reverse=True)
#     low_list.sort(reverse=True)

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

    open_diff_pow = (1 - (open_list.__getitem__(len(open_list) - 1) / open_list.__getitem__(0))) ** 2
    close_diff_pow = (1 - (close_list.__getitem__(len(close_list) - 1) / close_list.__getitem__(0))) ** 2
    high_diff_pow = (1 - (high_list.__getitem__(len(high_list) - 1) / high_list.__getitem__(0))) ** 2
    low_diff_pow = (1 - (low_list.__getitem__(len(low_list) - 1) / low_list.__getitem__(0))) ** 2

    return 1 - math.sqrt((open_diff_pow + close_diff_pow + high_diff_pow + low_diff_pow) / 4)
    # Todo check if dividing in integer makes the float number into integer


def similarity_two_sections(first_section, second_section):
    similarities_list = []
    percentages_sum = 0

    if len(first_section) != len(second_section):
        logging.warning("Sections length must match!")
        return

    for index in range(len(first_section)):
        first_section_candle = first_section.iloc[index]
        second_section_candle = second_section.iloc[index]
        similarities_list.append(similarity_between_two_candles(first_section_candle, second_section_candle))

    for similarity in similarities_list:
        percentages_sum += similarity
    final_percentage = percentages_sum / len(similarities_list)

    return final_percentage


def trading_strategy(gemini: Gemini, data):
    last_candle = data.iloc[len(data) - 1]
    second_last_candle = data.iloc[len(data) - 2]

    similarity_between_two_candles(last_candle, second_last_candle)


if __name__ == '__main__':
    # data_df = poloniex.load_dataframe(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

    # print(cl.manual_similarity_measure([98.19, 99.64], [98.32, 99.46], [98.43, 99.39], [98.41, 99.40], [98.57, 99.34], [98.71, 99.33], [98.66, 99.34], [98.72, 99.39], [98.80, 99.34], [98.70, 99.24]))
    # down below are different trending chunks of charts
    print(cl.manual_similarity_measure([-.02, .07], [.13, -.18], [.11, -.07], [-.02, .01], [.16, -.06], [.14, -.01], [-.05, .01], [.06, .05], [.08, -.05], [-.10, -.10]))
    # down below are kinda simillar chunks of charts
    print(cl.manual_similarity_measure([-.02, .04], [.13, .13], [.11, .16], [-.02, .06], [.16, -.14], [.14, 18], [-.05, -.03], [.06, -.08], [.08, .04], [-.10, .01]))
# last_candle = data_df.iloc[len(data_df) - 1]
    # second_last_candle = data_df.iloc[len(data_df) - 200]
    #
    # similarity_between_two_candles(last_candle, second_last_candle)

    # first_section = data_df.iloc[0:10]
    # second_section = data_df.iloc[28000:28010]
    # similarity_two_sections(first_section, second_section)

    # backtesting_engine = Gemini(logic=trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)
    # backtesting_engine.run(data=data_df)
