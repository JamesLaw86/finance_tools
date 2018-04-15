# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 18:21:00 2018

@author: James
"""

import data_requests
import analysis_methods

df = data_requests.make_request('^FTSE', 'TIME_SERIES_DAILY_ADJUSTED', 
                                outputsize = 'full')

s = analysis_methods.percent_match('D' , df = df, offset = -5)
#plt.plot(df['open'])