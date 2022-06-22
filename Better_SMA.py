# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 00:59:43 2019

@author: Dhiraj Thareja

 two Simple Moving Average strategies on Apple, Google, Microsoft, Citigroup, TSLA

Dates  1/1/2018 - 6/1/2021

Strategy 1 use short 50, long 200

Strategy 2 uses short 13 and long 50


"""
# This script enacts the SMA strategies in bt

import bt
# download data
data = bt.get('aapl,msft,c,tsla', start='2018-01-01', end='2021-06-01')

# calculate moving average DataFrame using pandas' rolling_mean
import pandas as pd


# define the length of the short and long averages
short = 50
long = 200

# a rolling mean is a moving average, right?
sma_short = data.rolling(short).mean()
sma_long = data.rolling(long).mean()

# and compute sma_50 for replicating earlier strat
sma_50 = data.rolling(50).mean()

# let's see what the data looks like - this is by no means a pretty chart, but it does the job
plot = bt.merge(data, sma_short, sma_long).plot(figsize=(15, 5))

# We need to set up our target weights. This will be the same size as sma_long
# weight = 1 means go long; weight = -1 means short

target_weights = sma_long.copy()


# set appropriate target weights
target_weights[sma_short > sma_long] =  0.25
target_weights[sma_short <= sma_long] = -0.25


# Now set up the MA_cross strategy for our moving average cross strategy
MA_cross = bt.Strategy('MA_cross', [bt.algos.WeighTarget(target_weights),
                                    bt.algos.Rebalance()])

test_MA = bt.Backtest(MA_cross, data)
res_MA = bt.run(test_MA)

# plot security weights to test logic
res_MA.plot_security_weights()


# define a signal to feed to the SelectWhere class to select securities to trade
# The signal is simple, data>sma_50 because data is price and sma_50 is moving average
signal = data > sma_50
bt.algos.SelectWhere(signal, include_no_data=False)

# first we create the Strategy 1
s = bt.Strategy('above50sma', [bt.algos.SelectWhere(signal),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])

# now we create the Backtest for first strategy
t = bt.Backtest(s, data)

# define the length of the short and long averages second strategy
short = 13
long = 50


sma_short = data.rolling(short).mean()
sma_long = data.rolling(long).mean()

# and compute sma_13_50 for replicating earlier strat
sma_13_50 = data.rolling(13).mean()

# let's see what the data looks like - this is by no means a pretty chart, but it does the job
plot = bt.merge(data, sma_short, sma_long).plot(figsize=(15, 5))

# We need to set up our target weights. This will be the same size as sma_long
# weight = 1 means go long; weight = -1 means short

target_weights = sma_long.copy()


# set appropriate target weights
target_weights[sma_short > sma_long] =  0.25
target_weights[sma_short <= sma_long] = -0.25


# define a signal to feed to the SelectWhere class to select securities to trade
# The signal is simple, data>sma_13_50 because data is price and sma_13_50 is moving average
signal = data > sma_13_50
bt.algos.SelectWhere(signal, include_no_data=False)

# first we create the Strategy 2
u = bt.Strategy('above-13-50-sma', [bt.algos.SelectWhere(signal),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])

v = bt.Backtest(u, data)




# and let's run it all
res = bt.run(t, v, test_MA)


# create plot
res.plot()

# display res
res.display()

