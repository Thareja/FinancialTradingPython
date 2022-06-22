# -*- coding: utf-8 -*-
"""


Introduction to package bt.py for backtesting

Created on Wed June 21 2022

@author: Dhiraj Thareja

Real simple, just playing around with code from the Professor
"""


# Import bt package; you must import all of the packages you use like this
import bt

# fetch some data.
# The first argument is the tickers. The default is to grab adjusted close from Yahoo
data = bt.get('SPY, AGG', start='2011-01-01' )#end='2021-1-31')
# Note: I commented out the end date above so it goes to the most recent data
# I often comment out code I might want to add back later; it saves time

"""
Make a very simple strategy. The bt.algos stuff defines the strategy.
We will run the algo monthly.
Most strategies need the SelectAll option. This means select all the assets.
WeighEqually means equal weights on each security in strategy. This will be all
 the securities in the data you feed to BackTest command below.

"""
# create the strategy
First_Strat = bt.Strategy('Strat1', [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
# This strategy will run every month and distribute all money equally in all assets.

# Create a backtest named test using our strat from above
test = bt.Backtest(First_Strat, data)
# Run the backtest named test and name the results res
# You use that name res to produce output
res = bt.run(test)

# first let's see an equity curve
res.plot()

# Display the statitics bt calculated for us
res.display()

# Plot the security weights over time. This is a useful debugging tool.
res.plot_security_weights()

# ok and how does the return distribution look?
res.plot_histogram()
