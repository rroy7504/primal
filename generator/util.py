import numpy as np  
import pandas as pd
from common import storage

from datetime import datetime
from dateutil import tz
import pytz


def DAILY_CHANGE(symbol):
    storage_client = storage.Storage()
    stock_data = storage_client.read_historic_quote(symbol)
    timestamps = list(stock_data['timestamp'].nlargest(2))
    todays_close = stock_data[stock_data.timestamp == timestamps[0]].iloc[0]['close']
    yesterdays_close = stock_data[stock_data.timestamp == timestamps[1]].iloc[0]['close']
    return "{0:.2f}".format(todays_close - yesterdays_close)


def LATEST_CLOSE(symbol):
    storage_client = storage.Storage()
    stock_data = storage_client.read_historic_quote(symbol)
    latest_timestamp = stock_data['timestamp'].max()
    return "{0:.2f}".format(stock_data[stock_data.timestamp == latest_timestamp].iloc[0]['close'])


def DAILY_PERCENTAGE_CHANGE(symbol):
    storage_client = storage.Storage()
    stock_data = storage_client.read_historic_quote(symbol)
    timestamps = list(stock_data['timestamp'].nlargest(2))
    todays_close = stock_data[stock_data.timestamp == timestamps[0]].iloc[0]['close']
    yesterdays_close = stock_data[stock_data.timestamp == timestamps[1]].iloc[0]['close']
    return "{0:.2f}".format(((todays_close - yesterdays_close) / yesterdays_close) * 100) + '%'