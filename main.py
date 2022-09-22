import logging
import math

import pandas as pd

import calculations as cl
import gemini
from gemini.gemini_core.exchange import OpenedTrade
from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze

# TODO - optimize params
import calculations

PAIR = "USDT_BTC"
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


def maxelements(df, n):
    final_list = pd.DataFrame(columns=['accuracy', 'date', 'close'])
    list_close_only = df['close'].tolist()
    comparison_length = 60

    for i in range(0, n):
        max1 = 0
        a = 1
        for j in range(len(data_df['close'])-comparison_length+1):
            current_accuracy = calculations.manual_similarity_measure(data_df['close'][len(data_df)-j-comparison_length: len(data_df)-j], data_df['close'][len(data_df)-comparison_length:])
            if (current_accuracy > max1) & (df.index.__contains__(data_df.index[len(data_df)-j-comparison_length])):
                max1 = current_accuracy
                date = df.index[len(data_df)-j-comparison_length]
                close = df['close'][len(data_df)-j-comparison_length]

        df = df[df.index != date]

        final_list = final_list.append({'accuracy': max1, 'date': date, 'close': close}, ignore_index=True)
        a = 1
    print(final_list)


if __name__ == '__main__':
    data_df = poloniex.get_past(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

    maxelements(data_df, 3)

    # comparison_length = 60

    # highest = calculations.manual_similarity_measure(data_df["close"][len(data_df)-1-comparison_length: len(data_df)-1], data_df["close"][len(data_df)-comparison_length:])
    # date_of_highest = data_df.index[len(data_df)-1-comparison_length]
    # close_of_highest = data_df["close"][len(data_df)-1-comparison_length]
    # for index in range(2, len(data_df)-comparison_length+1):
    #     current = calculations.manual_similarity_measure(data_df["close"][len(data_df)-index-comparison_length: len(data_df)-index], data_df["close"][len(data_df)-comparison_length:])
    #     if current > highest:
    #         highest = current
    #         date_of_highest = data_df.index[len(data_df)-index-comparison_length]
    #         close_of_highest = data_df["close"][len(data_df)-index-comparison_length]

    # print(highest)
    # print(date_of_highest)
    # print(close_of_highest)
