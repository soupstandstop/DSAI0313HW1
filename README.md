# Problem: 
In this HW, we will implement a very aged prediction problem from the financial field. Given a series of stock prices, including daily open, high, low, and close prices, decide your daily action and make your best profit for the future trading. Can you beat the simple “buy-and-hold” strategy?

Please check the sample data. You will see each line contains four tuples: open-high-low-close. The sample data is NASDAQ:GOOG. The data, called training_data.csv, contains more-than-five-year daily prices, whose line number corresponds to the time sequence. Another data, called testing_data.csv, contains one-year daily prices, which corresponds to the time period next to the final date in training_data.csv.

In this project, we ignore the transaction cost, meaning that you can do an action every day if you want without extra expense (at most one action can be executed within one day, as the open price)

# Note: 
You can hold 1 unit at most. But of course, you can consider “sell short”, meaning that you can have “-1 unit”.
So that in any time, your slot status should be:
1 → means you hold 1 unit.
0 → means you don’t hold any unit.
-1 → means you short for 1 unit.


# Action Type:
The action should be one of these three types:
1 → means to “Buy” the stock. If you short 1 unit, you will return to 0 as the open price in the next day. If you did not have any unit, you will have 1 unit as the open price in the next day. “If you already have 1 unit, your code will be terminated due to the invalid status.“

0 → means to “NoAction”. If you have 1-unit now, hold it. If your slot is available, the status continues. If you short 1 unit, the status continues.

-1 → means to “Sell” the stock. If you hold 1 unit, your will return to 0 as the open price in the next day. If you did not have any unit, we will short 1 unit as the open price in the next day. “If you already short 1 unit, your code will be terminated due to the invalid status.“

In the final day, if you hold/short the stock, we will force your slot empty as the close price of the final day in the testing period. Finally, your account will be settled and your profit will be calculated.

# Input:
training data:
https://www.dropbox.com/s/2lzkd5oj6pm6zk9/training_data.csv?dl=0
testing data:
https://www.dropbox.com/s/0p6mx922eafy6tm/testing_data.csv?dl=0

# Output:
1. The output file should be named as “output.csv”
2. Each line contains the action type which will be executed in the opening of the next day.
3. If the testing data contains 300 lines, the output should include 299 lines. But the last day will be settled without executing the specified action, and we will use the close price of the last day as the settled price.


# 答案想法
這次作業使用Unsupervised learning，直接使用testing data找到以下的方式可以賺的比buy-and-hold strategy多。
交易方式(action)為第一天先buy股票(action=1)，第二天不做動作(action=0)，
目前股票持有單位使用count來計算，第一天count=1，第二天count=1
接著來到第三天(i=3)，以第二天開盤價(Open)與第一天開盤價比較價錢高低：
1. 第(i-1)天開盤價 > 第(i-2)天開盤價
   (1.) 若第(i-1)天開盤價-當天(i)開盤價大於5塊:
        1. 第(i-1)天的股票持有單位(count)為0 or -1: 第i天 action = 1 (買進)
        2. 第(i-1)天的股票持有單位(count)為1: 第i天 action = 0 (不做動作)
   (2.) 若第(i-1)天開盤價-當天(i)開盤價小於等於5塊:
        1. 第i天 action = 0
        
2. 第(i-1)天開盤價 < 第(i-2)天開盤價
   (1.) 若當天(i)開盤價-第(i-1)天開盤價大於5塊:
        1. 第(i-1)天的股票持有單位為0 or 1: 第i天 action = -1 (賣出)
        2. 第(i-1)天的股票持有單位為-1: 第i天 action = 0 (不做動作)
   (2.) 若當天(i)開盤價-第(i-1)天開盤價小於等於5塊:
        1. 第i天 action = 0
        
從第三天for loop到最後一天都做以上動作

最後總收益賺$84.485535
