# -*- coding: utf-8 -*-
"""
Created on Sun June 12 2022 10amEST

This scripts shows the following strategy:

Dates to run strategy 1/1/17 - 6/1/21:

Dividing assets equally into GME, AMC, NFLX, and MVIS

Rebalancing portfolio every month, daily, weekly

@author: Dhiraj Thareja
"""

import bt

#%matplotlib inline


# Fetch some data
data = bt.get('GME, AMC, NFLX, MVIS', start='2017-01-01', end='2021-06-01')

# Recreate the strategy named First_Strat
First_Strat = bt.Strategy('First Strat - Monthly', [bt.algos.RunMonthly(),
                                     bt.algos.SelectAll(),
                                     bt.algos.WeighEqually(),
                                     bt.algos.Rebalance()])

# Create a backtest named test
test = bt.Backtest(First_Strat, data)

# create a second strategy named Second_Strat

Second_Strat = bt.Strategy('Second Strat - Weekly', [bt.algos.RunWeekly(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighEqually(),
                        bt.algos.Rebalance()])


Third_Strat = bt.Strategy('Third Strat - Daily', [bt.algos.RunDaily(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighEqually(),
                        bt.algos.Rebalance()])

# Test Second_Strat and name it test2
test2 = bt.Backtest(Second_Strat, data)

test3 = bt.Backtest(Third_Strat, data)

# To see the results side-by-side, we must tell the bt.run to use all tests
# All res2 commands will produce output comparing s1 and s2 because we have test and test2 and test3 
results_all = bt.run(test, test2, test3)

# res_First_Strat only has test in it, so you will only see Second_Strat from it
res_First_Strat = bt.run(test)

# res_Second_Strat only has test2 in it, so you will only see Second_Strat from it
res_Second_Strat = bt.run(test2)

res_Third_Strat = bt.run(test3)

# res2 plots here include both s1 and s2 and s3 info
results_all.plot()

results_all.display()

# Plot weights from the first strategy to illustrate the different weighting schemes
res_First_Strat.plot_security_weights()
res_Second_Strat.plot_security_weights()
# For some reason, I cannot plot weights or histograms for both at the same time
results_all.plot_security_weights()







