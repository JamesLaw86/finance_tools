# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 18:16:41 2018

@author: James
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def make_request(ticker, function = 'TIME_SERIES_DAILY',
                 api_key = '',
                 outputsize = 'compact',
                 **kwargs):
    """
    makes a request to alpha vantage api
    returns pandas dataframe
    """
    if not api_key:
        api_key = read_key()
    url = "https://www.alphavantage.co/query"
    params = {'symbol' : ticker,
              'function' : function,
              'apikey' : api_key,
              'outputsize' : outputsize}
    params = {**params, **kwargs}
    results = requests.get(url, params = params)
    if not results:
        return None
    
    results = results.json()
    time_series = results['Time Series (Daily)']
    datas = [time_series[time_point] for time_point in time_series]
    time_points = [pd.to_datetime(time_point) for time_point in time_series]
    
    df = pd.DataFrame(datas, time_points, dtype = float)
    if time_points[0] > time_points[1]:
        df = df.reindex(index=df.index[::-1])
    for column in df.columns:
        new_column = re.sub(r'\d.\s+', '', column)
        df.rename(columns = {column : new_column}, inplace = True)
    return df

def read_key():
    """ Reads text sring from apikey.txt"""
    with open('apikey.txt') as txt_file:
        data = txt_file.read()
    return data


