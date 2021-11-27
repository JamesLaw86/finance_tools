# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 18:20:17 2018

@author: James


"""
import numpy as np
import matplotlib.pyplot as plt

def percent_match(col = 'adjusted close', df = None, 
                  window = 5, offset = 0):
    """
    Get the trend of the last 10 days.
    Compare against the last X years of data.
    Keep the top 20% of matches. If there's a >50% chance of 
    increase in money then buy. If there's a > 50% chance of 
    loss then short. 
    """
    w_df = df[col]
    if offset:
        w_df = w_df[0 : offset]
    number_of_days = (252 * 4) #5years
    w_df = w_df.pct_change()
    w_df = w_df.replace([np.inf, -np.inf], np.nan)
    w_df = w_df.dropna()
    working_array = w_df[-window::]
    cut_off = w_df.mean()
    index = 0
    scores = {}
    all_scores = []
    plt.plot(np.arange(len(working_array)), working_array)
    for time in w_df[-number_of_days : -window]:
        test_array = w_df[index: index + window]
        try:
            score = __abs_difference(test_array, working_array)
            next_day = w_df[index+1]
            diff = next_day  - time
            if np.abs(diff) > cut_off:
                scores[index] = {'score' : score, 'Dir': diff > 0, 'points':test_array} #True = increase, False = decrease
                all_scores.append(score)
                plt.plot(np.arange(len(working_array)), test_array)
        except ValueError as e:
            print(e)
        index += 1
    
    all_scores = np.array(all_scores)
    top_lot = np.percentile(all_scores, 25)
    
    final_counts = {'up' : 0, 'down' : 0}
    for index in scores:
        score = scores[index]['score']
        if score <= top_lot:
            if scores[index]['Dir']:
                final_counts['up'] += 1
            else:
                final_counts['down'] += 1
            plt.plot(np.arange(len(working_array)), scores[index]['points'])
    return final_counts
    
        
def __abs_difference(arr1, arr2):
    if (arr1 == 0).any():
        raise ValueError('Has a zero' + str(arr1))
    if(arr2 == 0).any():
        raise ValueError('Has a zero' + str(arr2))
    
    return np.sum(np.abs(arr1-arr2))


def follow_trend(df, col = 'adjusted close', big_range = 30 , small_range = 10):
    """
    If average of a recent number of days (small range) is 
    higher than the average of a longer period of days (long range)
    then trend is up (buy), if it's below then rend is down (short)
    """
    w_df = df[col]
    av_small_range = w_df[-small_range::].mean()
    av_big_range = w_df[-big_range::].mean()
    
    results = {'Ratio': av_small_range / av_big_range}
    if av_small_range > av_big_range:
        results['Trend'] = 'up'
    else:
        results['Trend' ] = 'down'
    return results


if __name__ == '__main__':
    import data_requests
    #df = data_requests.make_request('^FTSE', 'TIME_SERIES_DAILY_ADJUSTED', 
                                    #outputsize = 'full')
    results = follow_trend(df)
    print(results)






