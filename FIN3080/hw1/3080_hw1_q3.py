import pandas as pd
import matplotlib.pyplot as plt


def roe_compare(group):
    count = -1
    for value in group['ROEC']:
        count += 1
        if count == 10:
            break
        if value >= roe_median_annual[2011 + count]:
            list_1[count] += 1
        else:
            break


def rate_compare(group):
    count = -1
    for value in group['TotalRevenueGrowthRate']:
        count += 1
        if count == 10:
            break
        if value >= rate_median_annual[2011 + count]:
            list_2[count] += 1
        else:
            break


data = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/problem3_data.csv")
data['EndDate'] = pd.to_datetime(data['EndDate']).dt.year.astype(int)
data = data.groupby('Symbol').filter(lambda x: x['EndDate'].min() <= 2011 and x['EndDate'].max() >= 2020)  # 筛选包含在2011-2020的公司
data = data.sort_values(by=['Symbol', 'EndDate'])
data['TotalRevenueGrowthRate'] = data.groupby('Symbol')['TotalRevenue'].pct_change(fill_method=None)

data = data[(data['EndDate'] >= 2011) & (data['EndDate'] <= 2020)]
group_roe_sizes = data.groupby('EndDate')["ROEC"].count()
group_rate_sizes = data.groupby('EndDate')["TotalRevenueGrowthRate"].count()

roe_median_annual = data.groupby('EndDate')["ROEC"].median()
rate_median_annual = data.groupby('EndDate')["TotalRevenueGrowthRate"].median()

list_1 = [0] * 10
list_2 = [0] * 10
percentage_list_roe = []
percentage_list_rate = []
data.groupby('Symbol').apply(roe_compare)
data.groupby('Symbol').apply(rate_compare)

for i, size in enumerate(group_roe_sizes):
    up = list_1[i]
    num = up / size
    percentage_list_roe.append(num)

for i, size in enumerate(group_rate_sizes):
    up = list_2[i]
    num = up / size
    percentage_list_rate.append(num)

plt.figure(figsize=(10, 6))
plt.scatter(range(2011, 2021), percentage_list_roe, label='ROE', color='blue', marker='o')
plt.scatter(range(2011, 2021), percentage_list_rate, label='Growth Rate', color='red', marker='o')
plt.plot(range(2011, 2021), percentage_list_roe, color='blue', linestyle='-')
plt.plot(range(2011, 2021), percentage_list_rate, color='red', linestyle='-')
plt.title('Percentages of companies that consistently maintain above-median')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.xticks(range(2011, 2021))  # 设置 x 轴刻度为每一年
plt.grid(True, linestyle='--', color='gray', alpha=0.5)
plt.legend()
plt.show()