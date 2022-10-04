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
DAYS_HISTORY = 1  # oldest date 08/10/2021(dd/mm/yyyy)

COMPARISON_LENGTH = 10


def max_elements(df, comparison_length):
    list = pd.DataFrame(columns=['accuracy', 'date', 'close'])

    for j in range(5, len(df['close']) - comparison_length + 1):
        accuracy = calculations.manual_similarity_measure(df['close'][len(df) - j - comparison_length: len(df) - j], df['close'][len(df) - comparison_length:])
        date = df.index[len(df) - j - comparison_length]
        close = df['close'][len(df) - j - comparison_length]
        list = list.append({'accuracy': accuracy, 'date': date, 'close': close}, ignore_index=True)
    list = list.sort_values(by=['accuracy'])
    return list

if __name__ == '__main__':
    data_df = chart_data.get_data(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)
    max_elements(data_df, COMPARISON_LENGTH)

    # x axis values
    x = [1,2,3]
    # corresponding y axis values
    y = [2,4,1]

    # plotting the points
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')

    # giving a title to my graph
    plt.title('My first graph!')

    # function to show the plot
    plt.show()
    pass

