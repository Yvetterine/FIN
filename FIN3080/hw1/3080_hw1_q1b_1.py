import pandas as pd

# Q2
# 读取数据
data_1 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/new_i.csv")
data_2 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/new_ii.csv")
data_3 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/new_iii.csv")

# 创建 Market Type 映射字典
mapping = {1: 'main board', 4: 'main board', 64: 'main board', 16: 'GEM', 32: 'GEM'}
data_3['Market Type Category'] = data_3['Market Type'].map(mapping)
grouped_data_3 = data_3.groupby('Market Type Category')

mapping_dict = data_3.set_index('Stock Code')['Market Type Category'].to_dict()
data_1['Market Type'] = data_1['Stock Code'].map(mapping_dict)
grouped_data_1 = data_1.groupby('Market Type')

data_2['Market Type'] = data_2['Stock Code'].map(mapping_dict)
grouped_data_2 = data_2.groupby('Market Type')

# firm ages
firm_ages_describe = grouped_data_3['Quarterly Firm Ages'].describe().transpose()
firm_ages_describe['Attribute'] = 'Firm Ages'

# monthly return
stock_return = grouped_data_1['Monthly Return With Cash Dividend Reinvested'].describe().transpose()
stock_return['Attribute'] = 'Monthly Return'

# pe
pe = grouped_data_1['monthly P/E ratios'].describe().transpose()
pe['Attribute'] = 'Monthly P/E Ratios'

# pb
pb = grouped_data_1['monthly P/B ratios'].describe().transpose()
pb['Attribute'] = 'Monthly P/B Ratios'

# roa
roa = grouped_data_2['Return on Assets - B'].describe().transpose()
roa['Attribute'] = 'ROA'

# roe
roe = grouped_data_2['Return on Equity - B'].describe().transpose()
roe['Attribute'] = 'ROE'

# rd
rd = grouped_data_2['quarterly R&D expense / total asset ratios'].describe().transpose()
rd['Attribute'] = 'R&D Expense / Total Asset Ratios'


result = pd.concat([firm_ages_describe, stock_return, pe, pb, roa, roe, rd], axis=0)
result.to_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/summary.csv")

# #  Q3
target_date_start = pd.Timestamp('2000-01')
target_date_end = pd.Timestamp('2023-09')
data_1['Trading Month'] = pd.to_datetime(data_1['Trading Month'])
data_1 = data_1[(data_1['Trading Month'] >= target_date_start) & (data_1['Trading Month'] <= target_date_end)]
pe_median_by_market_type = data_1.groupby(['Market Type', 'Trading Month'])['monthly P/E ratios'].median().unstack()
pe_median_by_market_type.to_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/1b.csv", index=False)