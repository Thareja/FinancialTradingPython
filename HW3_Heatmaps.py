#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:20:19 2022

@author: Dhiraj Thareja

Description: This scripts does a crossover strategy in a loop to find best short between 20-40 and best long between 150-250

It creates heat map to show which long and short combo have best CAGR 
Creates 2nd heat map to show which long and short combo have best Daily Sharpe 

Gets Equity progression of buy hold strategy for same dates for TSLA

Plots this equity progression against best combo for best CAGR vs best daily sharpe

"""

# importing all libraries I need
import bt

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

# Setup variable - we are using Tesla and assigning dates
tickers = 'TSLA'

startdate='2020-01-01'
enddate='2021-06-01'

#get data
data = bt.get(tickers=tickers, start=startdate, end=enddate)

#function to test crossover
def max(tickers, short=50, long=200, name ='Name Me'):

   

    short_sma = data.rolling(short).mean()
    long_sma = data.rolling(long).mean()
    


    target_weights = long_sma.copy()
    target_weights[short_sma > long_sma] = 1
    target_weights[short_sma <= long_sma] = -1

    
    s = bt.Strategy(name, [bt.algos.WeighTarget(target_weights),bt.algos.Rebalance()])

    # now we create the backtest
    return bt.Backtest(s, data)

# Create a result_df to store results
result_df = pd.DataFrame(columns = ['SMA','CAGR','daily_sharpe'])



for short_number in range (20, 41):
    short_name= 'sma'+ str(short_number)
    for long_number in range (150,255,5):
        long_name= 'sma'+ str (long_number)
# generate result feeding the above_sma function variables that change in the loop
        result = bt.run(max(tickers,short=short_number,long=long_number,name=short_name))

#was just testing did a display
        #result.display()

# adding to dataframe
        result_df = result_df.append({'SMA':short_name,'Short_SMA':short_number,'Long_SMA':long_number,'CAGR':result.stats.at['cagr',short_name],'daily_sharpe':result.stats.at['daily_sharpe',short_name]}, ignore_index=True)


# outputting data to excel
result_df.to_excel('HW3-heatmaps.xlsx')

results_heatmap = result_df.copy() # make a copy of the results_df to do a CAGR heatmap


results_heatmap_DS = result_df.copy() # make a copy of the results_df to do a Daily Sharpe heatmap

# Creating Heat Maps

sns.set_theme()

# Creating Heat Map for CAGR

results_heatmap = results_heatmap.pivot("Short_SMA", "Long_SMA", "CAGR")
results_heatmap = results_heatmap.astype(float) # stuck this in because
# I was getting a weird not a number (NaN) error. This forces everything to float (decimal)
f, ax = plt.subplots(figsize=(16, 12))
ax.set_title('CAGR')
ax = sns.heatmap(results_heatmap, annot=True, linewidths=1, ax=ax)


# Creating Heat Maps for Daily Sharpe

results_heatmap_DS = results_heatmap_DS.pivot("Short_SMA", "Long_SMA", "daily_sharpe")
results_heatmap_DS = results_heatmap_DS.astype(float) # stuck this in because
# I was getting a weird not a number (NaN) error. This forces everything to float (decimal)
f, ax = plt.subplots(figsize=(16, 12))
ax.set_title('daily_sharpe')
ax = sns.heatmap(results_heatmap_DS, annot=True, linewidths=1, ax=ax)
#dropped the d because that was not formatting for floats


# Test Buy Hold Strategy of TSLA aka benchmark
BuyHold_Strat = bt.Strategy('Buy Hold TSLA', [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])


# Create a backtest named test using our strat from above 
test = bt.Backtest(BuyHold_Strat, data)
# Run the backtest named test and name the results res 
# You use that name res to produce output


#Find highest value CAGR
# index corresponding max value CAGR
i = result_df['CAGR'].astype(float).idxmax()

CAGR_short = result_df['Short_SMA'][i].astype(int)
CAGR_long = result_df['Long_SMA'][i].astype(int)

test2 = max(tickers,short=CAGR_short,long=CAGR_long,name='Best CAGR')

#Find highest value Daily Sharpe

# index corresponding max value daily_sharpe
i_DS = result_df['daily_sharpe'].astype(float).idxmax()


DS_short = result_df['Short_SMA'][i_DS].astype(int)
DS_long = result_df['Long_SMA'][i_DS].astype(int)

test3 = max(tickers,short=DS_short,long=DS_long,name='Best Daily Sharpe')

res = bt.run(test, test2, test3)

# Lets plot all of them
res.plot()

res = bt.run(test, test3)

# Couldnt see Best CAGR so I plotted CAGR Seperately againts benchmark
res.plot()

res = bt.run(test, test2)

# Couldnt see Best CAGR so I plotted CAGR Seperately  and then now Sharpe against benchmark
res.plot()




