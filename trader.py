if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                        default='training_data.csv',
                        help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()
    import pandas as pd
    import numpy as np
    # trader = Trader()
    testing_data = pd.read_csv(args.testing, header=None, names=["Open", "High", "Low", "Close"])
    open = testing_data['Open']
    close = testing_data['Close']
    rows = len(testing_data)
    print(rows)
    count = np.zeros(rows) # 計數單位
    action = np.zeros(rows)  # action為一271*1array
    count[0] = 1
    count[1] = 1

    action[0] = 1
    action[1] = 0

    for i in range(2, rows, 1):
        if open.iloc[i - 1] > open.iloc[i - 2]:
            if 5 < open.iloc[i - 1] - open.iloc[i]:
                if count[i - 1] == 1:
                    action[i] = 0
                else:
                    action[i] = 1
            else:
                action[i] = 0

        elif open.iloc[i - 1] < open.iloc[i - 2]:
            if open.iloc[i] - open.iloc[i - 1] > 5:
                if count[i - 1] == -1:
                    action[i] = 0
                else:
                    action[i] = -1
            else:
                action[i] = 0
        count[i] = count[i - 1] + action[i] # 算股票目前持有單位

    money = np.zeros(rows) # 算現在手上的現金
    for i in range(0, rows-1, 1):
        if action[i] == 1:
            money[i] = money[i - 1] - open.iloc[i + 1]
        elif action[i] == 0:
            money[i] = money[i - 1]
        elif action[i] == -1:
            money[i] = open.iloc[i + 1] + money[i - 1]

    if count[rows-1] == 1:
        money[rows-1] = close.iloc[rows-1] + money[rows-2]  # 將股票賣掉得到收盤價現金
    elif count[rows-1] == 0:
        money[rows-1] = money[rows-2]
    elif count[rows-1] == -1:
        money[rows-1] = money[rows-2] - close.iloc[rows-1]  # 買股票將現有的錢減掉收盤價

    testing_data.insert(4, 'Action', action)  # 插入最後一行
    testing_data.insert(5, 'Unit', count)
    testing_data.insert(6, 'Money', money)

    print(testing_data)
    print('----------------')
    print(action)
    submission = pd.DataFrame(action[:rows-1])
    submission.to_csv(args.output, index=False, header=False)
