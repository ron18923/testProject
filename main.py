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


def trading_strategy(gemini: Gemini, data):
    last_candle = data_df.iloc[len(data_df)-1]

    pass


if __name__ == '__main__':
    data_df = poloniex.load_dataframe(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

    backtesting_engine = Gemini(logic=trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)
    backtesting_engine.run(data=data_df)
