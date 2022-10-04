import logging
import time
import traceback

import pandas as pd
import requests


def get_data_from_poloniex(params):
    response = requests.get('https://poloniex.com/public', params=params)
    data = response.json()
    return data


def get_chart(pair, period, days_history=30):
    """
    Returns historical charts data from poloniex.com
    :param pair: the pair to get historical data of
    :param period: the intervals between each point
    :param days_history: from when to get the data
    :return: pandas.dataframe of the pair's historical data
    """

    df = pd.DataFrame()
    items_per_iteration = 100

    # counting how much items we need to get (24 * 60 * 60 * days_history) / period
    # counting how much times the for loop needs to run int(items_amount/100) + (1 if items_amount%100 > 0 else 0)
    # rounding to last time stamp: int(time.time()/period)*period
    items_amount = (24 * 60 * 60 * days_history) / period
    loop_amount = int((items_amount / items_per_iteration) + (1 if items_amount % items_per_iteration > 0 else 0))
    rounded_timestamp = int(time.time() / period) * period
    for index in range(loop_amount):
        if index != loop_amount - 1:
            start = rounded_timestamp - (items_per_iteration - 1) * period
            end = rounded_timestamp
            rounded_timestamp = rounded_timestamp - (items_per_iteration - 1) * period

        else:
            items_left_to_get = (items_amount % items_per_iteration)
            if items_left_to_get == 0:
                continue

            start = rounded_timestamp - (items_left_to_get - 1) * period
            end = rounded_timestamp
            rounded_timestamp = rounded_timestamp - (items_amount % items_per_iteration - 1) * period

        params = {
            'command': 'returnChartData',
            'currencyPair': pair,
            'start': start,
            'end': end,
            'period': period
        }

        data = get_data_from_poloniex(params)

        try:
            df = pd.concat([df, pd.DataFrame(data)])
        except ValueError:
            response = requests.get('https://poloniex.com/public', params=params)
            data = response.json()
            df = pd.concat([df, pd.DataFrame(data)])

    df = df.sort_values(by=['date'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')  # pandas default is
    df = df.set_index(['date'])
    return df


def load_save_df(pair, period, save= None):
    """
    loads or saves a dataframe with the specified pair and period.
    :param pair: pair to get
    :param period: period to get
    :param save: add dataframe to save, else data will be loaded.
    :return: returns the file with the needed dataframe
    """
    file_path = "C:/Users/Ronro/IdeaProjects/test/history_data/" + pair + "-" + str(period) + ".pkl"
    if save is None:
        df = pd.read_pickle(file_path)
        return df
    else:
        save.to_pickle(file_path)


def get_data(pair, period, days_history=30):
    saved_df = load_save_df(pair, period)

    last_saved_timestamp = saved_df.index[len(saved_df)-1].timestamp()

    items_amount = (24 * 60 * 60 * days_history) / period
    rounded_timestamp = int(time.time() / period) * period

    start_timestamp = rounded_timestamp - items_amount * period
    start_date = pd.to_datetime(start_timestamp, unit='s')

    index = (list(saved_df.index)).index(start_date)
    df = saved_df[index:]

    time_stamp_difference = rounded_timestamp - last_saved_timestamp

    items_per_iteration = 100
    items_amount = time_stamp_difference/period + 1
    loop_amount = int((items_amount / items_per_iteration) + (1 if items_amount % items_per_iteration > 0 else 0))

    df_to_add = pd.DataFrame()

    for index in range(loop_amount):
        if index != loop_amount - 1:
            start = rounded_timestamp - (items_per_iteration - 1) * period
            end = rounded_timestamp
            rounded_timestamp = rounded_timestamp - (items_per_iteration - 1) * period

        else:
            items_left_to_get = (items_amount % items_per_iteration)
            if items_left_to_get == 0:
                continue

            start = rounded_timestamp - (items_left_to_get - 1) * period
            end = rounded_timestamp
            rounded_timestamp = rounded_timestamp - (items_amount % items_per_iteration - 1) * period

        params = {
            'command': 'returnChartData',
            'currencyPair': pair,
            'start': start,
            'end': end,
            'period': period
        }

        data = get_data_from_poloniex(params)

        try:
            df_to_add = pd.concat([df_to_add, pd.DataFrame(data)])
        except ValueError:
            response = requests.get('https://poloniex.com/public', params=params)
            data = response.json()
            df_to_add = pd.concat([df_to_add, pd.DataFrame(data)])

    df_to_add = df_to_add.sort_values(by=['date'])
    df_to_add['date'] = pd.to_datetime(df_to_add['date'], unit='ms')  # pandas default is
    df_to_add = df_to_add.set_index(['date'])
    df = pd.concat([df, df_to_add])

    saved_df = pd.concat([saved_df, df_to_add])
    load_save_df(pair, period, saved_df)
    return df
