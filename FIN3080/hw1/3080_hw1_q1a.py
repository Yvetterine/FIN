import pandas as pd

# Q1
name_1 = "C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/ii.csv"
data_1 = pd.read_csv(name_1)
data_1 = data_1[data_1['Statement Type'] != 'B']     # 删b股
data_1["Ending Date of Statistics"] = pd.to_datetime(data_1["Ending Date of Statistics"])
data_1 = data_1[data_1['Ending Date of Statistics'].dt.month != 1]    # 删一月
data_1["Quarter"] = data_1["Ending Date of Statistics"].dt.to_period('Q')

name_2 = "C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/i.csv"
data_2 = pd.read_csv(name_2)
data_2["Trading Month"] = pd.to_datetime(data_2["Trading Month"])
data_2["Quarter"] = data_2["Trading Month"].dt.to_period('Q') - 1

merge = pd.merge(data_1, data_2, how="right", right_on=["Stock Code", "Quarter"], left_on=["Stock Code", "Quarter"])

merge["Earnings per Share - TTM1"] = merge["Earnings per Share - TTM1"].astype(float)
merge["Monthly Closing Price"] = merge["Monthly Closing Price"].astype(float)
merge["Net Assets per Share"] = merge["Net Assets per Share"].astype(float)
data_1["R&D Expenses"] = data_1["R&D Expenses"].astype(float)
data_1["Total Assets"] = data_1["Total Assets"].astype(float)

merge["monthly P/E ratios"] = merge["Monthly Closing Price"] / (merge["Earnings per Share - TTM1"] / 3)
merge["monthly P/B ratios"] = merge["Monthly Closing Price"] / merge["Net Assets per Share"]
data_1["quarterly R&D expense / total asset ratios"] = data_1["R&D Expenses"] / data_1["Total Assets"]
merge.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/new_i.csv', index=False)         # 包含PE\PB
data_1.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/new_ii.csv', index=False)       # 包含R&D ratio


data_3 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/iii.csv")
data_3["Establishment Date"] = pd.to_datetime(data_3["Establishment Date"]).dt.to_period('Q')
current_date = pd.to_datetime('now').to_period('Q')
data_3["Quarterly Firm Ages"] = (current_date - data_3["Establishment Date"]).apply(lambda x: x.n)
data_3.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/new_iii.csv', index=False)             # 包含firm age