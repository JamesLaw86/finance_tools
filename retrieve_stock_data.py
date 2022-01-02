# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 14:03:15 2021

@author: james
"""

#stocks available: https://globefunder.com/revolut-stocks-list/

import yfinance as yf
import datetime
import shelve
import re
from dataclasses import dataclass

@dataclass
class stock:
    """Class to represent a particular company"""
    company: str = ''
    symbol: str = ''
    price: str = ''
    market_cap: str = ''
    sector: str = ''
    industry: str = ''
    market: str = ''
    
    """
    def __init__(self):
        self.company = ''
        self.symbol = ''
        self.price = ''
        self.market_cap = ''
        self.sector = ''
        self.industry = ''
        self.market = ''
    """
    
    
def read_available_stocks():
    """
    Read the list of stocks in Revolut stocks list.csv
    """
    stocks = {}
    with open('Revolut Stocks List - Revolut stocks list.csv', 'r') as csv_file:
        csv_file.readline()
        
        #remove all commas that are part of numbers
        for line in csv_file:
            results = re.findall(r'\$\d+,\d', line)
            if len(results) > 0:
                for result in results:
                    wo_comma = result.replace(',', '')
                    line = line.replace(result, wo_comma)
                    
            results = re.findall(r'\d,\d', line)
            if len(results) > 0:
                for result in results:
                    wo_comma = result.replace(',', '')
                    line = line.replace(result, wo_comma)
    
            split_line = line.split(',')
            this_stock = stock()
            this_stock.company = split_line[1]
            this_stock.symbol = split_line[2]
            this_stock.price = split_line[3]
            this_stock.market_cap = split_line[4]
            this_stock.sector = split_line[5]
            this_stock.industry = split_line[6]
            this_stock.market = split_line[7]
            stocks[this_stock.company] = this_stock
    return stocks

def get_data(stock, months = 0, weeks = 0, days = 0):
    """Request the data from yfinance"""
    dt = get_past_datetime_ago(months, weeks, days)
    df = yf.download(stock.symbol, start=dt, progress=False)
    return df
    
def get_past_datetime_ago(months, weeks, days):
    """Get datetime from the number of months, weeks, and days before now"""
    days_per_month = 365/12
    total_days = months * days_per_month
    total_days += (weeks * 7)
    total_days += days
    dt = datetime.datetime.now() - datetime.timedelta(total_days)
    return dt


def get_all_dfs(stocks, months):
    """Try to retrieve all the data for every stock"""
    dfs = {}
    count = 0
    total = len(stocks)
    for company in stocks:
        try:
            stock = stocks[company]
            df = get_data(stock, months)
            dfs[stock.company] = df
        except Exception as e:
            print(f"Error getting {stock.company}:{e}")
            print(f"count: {count}")
        count+=1
        
        if count % 20 == 0:
            print(f"Done {count} or {total}")
    
    return dfs

def get_all_data_frames(new_data = False, months = 18):
    """
    Get dataframes of all stocks. If new_data then we actually
    reques the data from yfinance. Otherwise we used saved data
    """
    if new_data:
        stocks = read_available_stocks()
        dfs = get_all_dfs(stocks, 18)
        with shelve.open('stocks') as db:
            db['stocks'] = stocks
            db['dfs'] = dfs
    else:
        with shelve.open('stocks') as db:
            stocks = db['stocks']
            dfs = db['dfs']
    return dfs, stocks

def plot(company, dfs):
    dfs[company]['Adj Close'].plot()
    