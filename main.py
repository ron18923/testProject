import pandas as pd

# TODO - optimize params
import calculations
import chart_data

import bokeh.plotting

from bokeh.layouts import row
from bokeh.models import LinearAxis, Range1d

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
PAIR = "USDT_BTC"
DAYS_HISTORY = 10  # 300 period, oldest date 08/10/2021(dd/mm/yyyy)
                     # 900 period, oldest date 12/09/2018

COMPARISON_LENGTH = 70


def without_unintended_results(results_list, period):

    results_date = results_list["date"]

    for index in range(1, len(results_date) + 1):
        time = results_date.iloc[len(results_date) - index]
        for j in range(1, 4):
            time_to_delete = time + pd.to_timedelta(period*j, unit='s')
            results_list = results_list.drop(results_list.index[results_list['date'] == time_to_delete])
    return results_list


def max_elements(df, comparison_length):
    results_list = pd.DataFrame(columns=['accuracy', 'date', 'close'])

    for j in range(5, len(df['close']) - comparison_length + 1):
        first = pd.to_numeric(df['close'][len(df) - j - comparison_length: len(df) - j])
        second = pd.to_numeric(df['close'][len(df) - comparison_length:])
        accuracy = calculations.manual_similarity_measure(first, second)

        date = df.index[len(df) - j - comparison_length]
        close = df['close'][len(df) - j - comparison_length]
        results_list = pd.concat([results_list, pd.DataFrame({'accuracy': [accuracy], 'date': [date], 'close': [close]})], ignore_index=True)
    results_list = results_list.sort_values(by=['accuracy'])
    return results_list


def display_data(df, similarities):
    bokeh.plotting.output_file("last_results.html")

    length = 51  # the first one will be the main plot, so the for loop will run length-1 times.
    plots = [None] * length

    main_plot = bokeh.plotting.figure(x_axis_type="datetime", plot_width=410,
                                      plot_height=300)
    main_plot.grid.grid_line_alpha = 0.3
    main_plot.xaxis.axis_label = 'Date'
    main_plot.yaxis.axis_label = 'Value'

    main_plot.line(data_df.index[len(data_df) - COMPARISON_LENGTH:],
                   data_df["close"][len(data_df) - COMPARISON_LENGTH:],
                   color='#00fffb', )

    plots[0] = main_plot

    for plot_index in range(1, length):
        df_timestamp = similarities["date"].iloc[-1 - plot_index]
        df_index = list(df.index).index(df_timestamp)

        current_plot = bokeh.plotting.figure(x_axis_type="datetime",
                                             title=str(df_timestamp) + " | " + str(
                                                 similarities["accuracy"].iloc[-1 - plot_index]),
                                             plot_width=750,
                                             plot_height=300)
        current_plot.grid.grid_line_alpha = 0.3
        current_plot.xaxis.axis_label = 'Date'
        current_plot.yaxis.axis_label = 'Value'

        current_plot.line(data_df.index[df_index:df_index + COMPARISON_LENGTH * 2],
                          data_df["close"][df_index:df_index + COMPARISON_LENGTH * 2],
                          color='#00fffb', )

        current_plot.extra_x_ranges = {"x": Range1d(start=0, end=1)}

        current_plot.add_layout(LinearAxis(x_range_name="x"), 'above')

        divider = bokeh.models.Span(location=0.5,
                                    dimension="height",
                                    line_color="black",
                                    x_range_name="x")
        current_plot.add_layout(divider)

        plots[plot_index] = current_plot
    bokeh.plotting.show(bokeh.layouts.column(plots))


if __name__ == '__main__':
    data_df = chart_data.get_data(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)
    similarities_list = max_elements(data_df, COMPARISON_LENGTH)

    similarities_list = without_unintended_results(similarities_list, PERIOD)

    display_data(data_df, similarities_list)
