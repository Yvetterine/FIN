import pandas as pd
import statsmodels.api as sm

name_1 = "C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw2/i.csv"
data_1 = pd.read_csv(name_1)
rename_dict_1 = {
    'Stkcd': 'Stock Code',
    'Trdmnt': 'Trading Month',
    'Mclsprc': 'Monthly Closing Price',
    'Mretnd': 'Monthly Return Without Cash Dividend Reinvested',
}
data_1.rename(columns=rename_dict_1, inplace=True)
data_1["Trading Month"] = pd.to_datetime(data_1["Trading Month"])
data_1["Match_Quarter"] = data_1['Trading Month'].dt.to_period('Q') - 1


name_2 = "C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw2/ii(2.csv"
rename_dict_2 = {
    'Stkcd': 'Stock Code',
    'ShortName_EN': 'Stock Short Name',
    'Accper': 'Ending Date of Statistics',
    'Typrep': 'Code for Statement Type',
    'F091001A': 'Net Assets per Share',
}
data_2 = pd.read_csv(name_2)
data_2.rename(columns=rename_dict_2, inplace=True)
data_2 = data_2[data_2['Code for Statement Type'] != 'B']     # 删b股
data_2["Ending Date of Statistics"] = pd.to_datetime(data_2["Ending Date of Statistics"])
data_2["Quarter"] = data_2["Ending Date of Statistics"].dt.to_period('Q')

merge = pd.merge(data_1, data_2, how="left", right_on=["Stock Code", "Quarter"], left_on=["Stock Code", "Match_Quarter"])
target_date = pd.to_datetime('2009-12-01')
# merge_1 是进行过日期删除和百分位数删除的。
merge_1 = merge[merge['Trading Month'] != target_date]
merge_1["monthly P/B ratios"] = merge_1["Monthly Closing Price"] / merge_1["Net Assets per Share"]
percentile_5 = merge_1['monthly P/B ratios'].quantile(0.05)
percentile_95 = merge_1['monthly P/B ratios'].quantile(0.95)
merge_1 = merge_1[(merge_1['monthly P/B ratios'] >= percentile_5) & (merge_1['monthly P/B ratios'] <= percentile_95)]


name_3 = "C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw2/ii(1.csv"
data_3 = pd.read_csv(name_3)
rename_dict_3 = {
    'Stkcd': 'Stock Code',
    'ShortName_EN': 'Stock Short Name',
    'Accper': 'Ending Date of Fiscal Year',
    'Typrep': 'Code for Statement Type',
    'F050504C': 'Return on Equity - TTM',
}
data_3.rename(columns=rename_dict_3, inplace=True)
data_3 = data_3[data_3['Code for Statement Type'] != 'B']     # 删b股
data_3["Ending Date of Fiscal Year"] = pd.to_datetime(data_3["Ending Date of Fiscal Year"])
data_3["Quarter"] = data_3["Ending Date of Fiscal Year"].dt.to_period('Q')


name_4 = "C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw2/iii.csv"
data_4 = pd.read_csv(name_4)
rename_dict_4 = {
    'Symbol': 'Stock Code',
    'TradingDate': 'Trading Date',
    'Volatility': 'Return Volatility',
}
data_4.rename(columns=rename_dict_4, inplace=True)
# merge.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw2/lala.csv', index=False)


# 读取第一张表，并筛选出指定时间的数据
table_1 = merge_1[merge_1['Trading Month'] == '2010/12/1']
table_2 = data_3[data_3['Quarter'] == '2010Q4']

# 将第一张表的指定列添加到主表中
data_4 = pd.merge(data_4, table_1[['Stock Code', 'monthly P/B ratios']], on="Stock Code", how="left")
data_4 = pd.merge(data_4, table_2[['Stock Code', 'Return on Equity - TTM']], on="Stock Code", how="left")
data_4.dropna(subset=['Stock Code', 'Return on Equity - TTM', 'monthly P/B ratios'], inplace=True)
y = data_4['monthly P/B ratios']
X = data_4[['Return on Equity - TTM', 'Return Volatility']]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())