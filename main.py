import pandas as pd

# TODO - optimize params
import calculations
import chart_data

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
DAYS_HISTORY = 250  # oldest date 08/10/2021(dd/mm/yyyy)

COMPARISON_LENGTH = 70


def max_elements(df, comparison_length):
    list = pd.DataFrame(columns=['accuracy', 'date', 'close'])

    for j in range(5, len(df['close']) - comparison_length + 1):
        accuracy = calculations.manual_similarity_measure(df['close'][len(df) - j - comparison_length: len(df) - j],
                                                          df['close'][len(df) - comparison_length:])
        date = df.index[len(df) - j - comparison_length]
        close = df['close'][len(df) - j - comparison_length]
        list = list.append({'accuracy': accuracy, 'date': date, 'close': close}, ignore_index=True)
    list = list.sort_values(by=['accuracy'])
    return list


import bokeh.plotting
from bokeh.io import show

from bokeh.layouts import row, column, gridplot
from bokeh.models import LinearAxis, Range1d


def display_data(df, similarities):
    bokeh.plotting.output_file("last_results.html")

    length = 11  # the first one will be the main plot, so the for loop will run length-1 times.
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
                                             title=str(df_timestamp),
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

    display_data(data_df, similarities_list)

    # p1 = bokeh.plotting.figure(x_axis_type="datetime", plot_width=410,
    #                            plot_height=300)
    #
    # p2 = bokeh.plotting.figure(x_axis_type="datetime", plot_width=750,
    #                            plot_height=300)
    #
    # p3 = bokeh.plotting.figure(x_axis_type="datetime", plot_width=750,
    #                            plot_height=300)
    #
    # p1.grid.grid_line_alpha = 0.3
    # p1.xaxis.axis_label = 'Date'
    # p1.yaxis.axis_label = 'Value'
    # p2.grid.grid_line_alpha = 0.3
    # p2.xaxis.axis_label = 'Date'
    # p2.yaxis.axis_label = 'Equity'
    # p3.grid.grid_line_alpha = 0.3
    # p3.xaxis.axis_label = 'Date'
    # p3.yaxis.axis_label = 'Equity'
    #
    # p1.line(data_df.index[len(data_df) - COMPARISON_LENGTH:], data_df["close"][len(data_df) - COMPARISON_LENGTH:],
    #         color='#00fffb', )
    #
    # timestamp = similarities_list["date"].iloc[-1]
    # index = list(data_df.index).index(timestamp)
    # p2.line(data_df.index[index:index + COMPARISON_LENGTH * 2], data_df["close"][index:index + COMPARISON_LENGTH * 2],
    #         color='#00fffb', )
    #
    # p2.extra_x_ranges = {"x": Range1d(start=0, end=1)}
    #
    # p2.add_layout(LinearAxis(x_range_name="x"), 'above')
    #
    # divider = bokeh.models.Span(location=0.5,
    #                             dimension="height",
    #                             line_color="black",
    #                             x_range_name="x")
    # p2.add_layout(divider)
    #
    # timestamp = similarities_list["date"].iloc[-2]
    # index = list(data_df.index).index(timestamp)
    # p3.line(data_df.index[index:index + COMPARISON_LENGTH * 2], data_df["close"][index:index + COMPARISON_LENGTH * 2],
    #         color='#00fffb', )
    #
    # p3.extra_x_ranges = {"x": Range1d(start=0, end=1)}
    #
    # # Adding the second axis to the plot.
    # p3.add_layout(LinearAxis(x_range_name="x"), 'above')
    #
    # divider = bokeh.models.Span(location=0.5,
    #                             dimension="height",
    #                             line_color="black",
    #                             x_range_name="x")
    # p3.add_layout(divider)
    #
    # bokeh.plotting.show(bokeh.layouts.column(p1, p2, p3))
    # pass
