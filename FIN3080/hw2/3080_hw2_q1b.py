import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
merge["monthly P/B ratios"] = merge["Monthly Closing Price"] / merge["Net Assets per Share"]
percentile_5 = merge['monthly P/B ratios'].quantile(0.05)
percentile_95 = merge['monthly P/B ratios'].quantile(0.95)
merge = merge[(merge['monthly P/B ratios'] >= percentile_5) & (merge['monthly P/B ratios'] <= percentile_95)]

# -------------------------------------------------------------------------------------------

merge['Trading Month'] = pd.to_datetime(merge['Trading Month']).dt.to_period('M')
group_means = []
merge['Previous Month PB'] = merge.groupby('Stock Code')['monthly P/B ratios'].shift(1)

filtered_data = merge[(merge['Trading Month'] != merge['Trading Month'].min()) & (merge['Trading Month'] != merge['Trading Month'].max())].copy()
filtered_data.sort_values(by=['Stock Code', 'Trading Month'], inplace=True)

result_data = pd.DataFrame()

for month in filtered_data['Trading Month'].unique():

    month_data = filtered_data[filtered_data['Trading Month'] == month].copy()
    month_data_without_na = month_data['Previous Month PB'].dropna()
    quantiles = month_data['Previous Month PB'].quantile(np.arange(0, 1.1, 0.1))

    closest_index = (np.abs(quantiles.index - 0.3)).argmin()
    third_quantile = quantiles.iloc[closest_index]

    closest_index = (np.abs(quantiles.index - 0.6)).argmin()
    sixth_quantile = quantiles.iloc[closest_index]

    closest_index = (np.abs(quantiles.index - 0.7)).argmin()
    seventh_quantile = quantiles.iloc[closest_index]

    groups = []

    # 遍历数据
    for value in month_data['Previous Month PB']:
        # 检查是否小于等于第一个分位数
        if value <= quantiles[0.1]:
            group = 1
        # 检查是否大于等于最后一个分位数
        elif value >= quantiles[0.9]:
            group = 10
        elif quantiles[0.1] < value <= quantiles[0.2]:
            group = 2
        elif quantiles[0.2] < value <= third_quantile:
            group = 3
        elif third_quantile < value <= quantiles[0.4]:
            group = 4
        elif quantiles[0.4] < value <= quantiles[0.5]:
            group = 5
        elif quantiles[0.5] < value <= sixth_quantile:
            group = 6
        elif sixth_quantile < value <= seventh_quantile:
            group = 7
        elif seventh_quantile < value <= quantiles[0.8]:
            group = 8
        elif quantiles[0.8] < value <= quantiles[0.9]:
            group = 9
        # 将确定的分组添加到列表中
        groups.append(group)

    # 将分组列表添加到数据中
    month_data['PB Group'] = groups

    group_means.append(month_data.groupby('PB Group')['Monthly Return Without Cash Dividend Reinvested'].mean())

group_means_df = pd.concat(group_means, axis=1)
final_means = group_means_df.mean(axis=1)
final_means.plot(kind='bar', color='skyblue')
plt.xlabel('Group')
plt.ylabel('Average Return')
plt.title('Average Return for Each Group')
plt.show()