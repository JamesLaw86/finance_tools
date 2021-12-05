# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 14:03:15 2021

@author: james
"""

import retrieve_stock_data as rsd
import numpy as np

def get_biggest_changes(dfs, days = -1):
    """
    Get the stocks that have changed the most in the given timeframe
    based on the average over the given period. 
    Note wer'e assuming dataframe is in period of days
    """
    percent_changes = get_percentage_changes(dfs, days)
    most_increased, most_decreased = determine_biggest_changes(percent_changes)
    return most_increased, most_decreased
    

def get_percentage_changes(dfs, days):
    """
    Calculate the amount all stocks have changed over the given period
    """
    changes = {}
    for company in dfs:
        df = dfs[company]
        close_prices = df['Adj Close']
        if(len(close_prices)) ==0:
            continue
        
        if days != -1:
            length = len(close_prices)
            close_prices = close_prices[(length - days)::]

        try:
            mean = close_prices.mean()
            cur = close_prices[len(close_prices)-1]
            per = (cur - mean)/mean * 100
            changes[company] = per
        except Exception as e:
            print(f"Error getting {company}:{e}")
            
    return changes
    
def determine_biggest_changes(changes):
    """
    Retrieve a list of the companies that have changed the most based on
    the calculated percentage change. Returns sepearte lists of those that 
    have increased the most and those that have decreased
    """
    list_companies = [company for company in changes]
    list_changes = [changes[change] for change in changes]
    arr_changes = np.array(list_changes)
    indexes = np.argsort(arr_changes)
    
    decreases = [list_companies[i] for i in indexes[0:20]]
    increases = [list_companies[i] for i in indexes[::-1][0:20]]
    return increases, decreases
    

dfs, stocks = rsd.get_all_data_frames()

most_increased, most_decreased = get_biggest_changes(dfs, 6*30)

