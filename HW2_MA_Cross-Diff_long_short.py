#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 00:59:43 2019

@author: Dhiraj Thareja

 two Simple Moving Average strategies on Apple, Google, Microsoft, Citigroup, Tesla

Dates  1/1/2018 - 6/1/2021

Strategy 1 use short 50, long 200

Strategy 2 uses short 30 and long 100

Strategy 2 is our test strategy

"""

# This script enacts the crossover strategy in bt

import bt
# download data
data = bt.get('aapl,msft,c,tsla', start='2018-01-01', end='2021-06-01')


# calculate moving average DataFrame using pandas' rolling_mean
import pandas as pd


# define the length of the Strategy 1 -  short and long averages
short = 50
long = 200

# define the length of the Strategy 2 - short2 and long2 averages
short2 = 30
long2 = 100

# a rolling mean is a moving average, right?
sma_short = data.rolling(short).mean()
sma_long = data.rolling(long).mean()



# let's see what the data looks like - this is by no means a pretty chart, but it does the job
plot = bt.merge(data, sma_short, sma_long).plot(figsize=(15, 5))

# We need to set up our target weights. This will be the same size as sma_long
# weight = 1 means go long; weight = -1 means short

target_weights = sma_long.copy()


# set appropriate target weights
target_weights[sma_short > sma_long] =  0.25
target_weights[sma_short <= sma_long] = -0.25


# Now set up the MA_cross strategy for our moving average cross strategy
MA_cross = bt.Strategy('MA_cross_50_200', [bt.algos.WeighTarget(target_weights),
                                    bt.algos.Rebalance()])

test_MA = bt.Backtest(MA_cross, data)
res_MA = bt.run(test_MA)

# plot security weights to test logic
res_MA.plot_security_weights()

# setup strategy 2



# a rolling mean is a moving average, right?
sma_short2 = data.rolling(short2).mean()
sma_long2 = data.rolling(long2).mean()



# let's see what the data looks like - this is by no means a pretty chart, but it does the job
plot = bt.merge(data, sma_short2, sma_long2).plot(figsize=(15, 5))

# We need to set up our target weights. This will be the same size as sma_long2
# weight = 1 means go long2; weight = -1 means short2

target_weights2 = sma_long2.copy()


# set appropriate target weights
target_weights2[sma_short2 > sma_long2] =  0.25
target_weights2[sma_short2 <= sma_long2] = -0.25

title="MA_cross_" + str(short2) + "_" + str(long2)

# Now set up the MA_cross strategy for our moving average cross strategy
MA_cross2 = bt.Strategy(title, [bt.algos.WeighTarget(target_weights2),
                                    bt.algos.Rebalance()])

test_MA2 = bt.Backtest(MA_cross2, data)
res_MA2 = bt.run(test_MA2)

# plot security weights to test logic
res_MA2.plot_security_weights()





# and let's run it!
res = bt.run(test_MA, test_MA2)

# what does the equity curve look like?
res.plot()

# and some performance stats
res.display()

