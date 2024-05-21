import pandas as pd
import matplotlib.pyplot as plt


def half_year_label(month):
    if month <= 6:
        return 'h1'
    else:
        return 'h2'


def second_half_eps(month):
    if month[-1] == 1:
        return 0
    else:
        return 1


def calculate_sue(group):
    rolling_std = group["UE"].rolling(window=4).std()
    sue = group['earnings_per_share'] / rolling_std
    return sue


def calculate_sue_deciles(group):
    sorted_sue = group['SUE'].sort_values()
    sue_deciles = pd.qcut(sorted_sue, 10, labels=False)
    return sue_deciles


# step_1
data_1 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data/TRD_Dalyr0.csv")
for i in range(1, 9):
    file_path = "C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data/TRD_Dalyr%s.csv" % i
    data = pd.read_csv(file_path)
    data_1 = pd.concat([data_1, data], axis=0)
data_1 = data_1.rename(columns={'Stkcd': 'stock_code', 'Trddt': 'trading_date', 'Dretnd': 'daily_return'})
data_1["trading_date"] = pd.to_datetime(data_1["trading_date"])
# 根据股票代码和日期排序
data_1.sort_values(by=['stock_code', 'trading_date'], inplace=True)
data_1.reset_index(drop=True, inplace=True)
# data_1.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data_1.csv', index=False)

# step_2
data_2 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data/TRD_Dalym.csv")
data_2 = data_2.rename(columns={'Markettype': 'mkt type', 'Trddt': 'trading_date', 'Dretmdeq': 'daily_mkt_return'})
data_2 = data_2[data_2['mkt type'] == 1]
data_2["trading_date"] = pd.to_datetime(data_2["trading_date"])
# data_2.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data_2.csv', index=False)

# step_3
data_3 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data/FI_T9.csv")
data_3 = data_3.rename(columns={'Stkcd': 'stock_code', 'ShortName_EN': 'stock_short_name',
                                'Accper': 'ending_date_of_statistics', 'Typrep': 'code_for_statement_type',
                                'Indcd': 'industry_code', 'F090101B': 'earnings_per_share'})
data_3 = data_3[data_3['code_for_statement_type'] != "B"]
data_3.drop(data_3[data_3['stock_short_name'].str.startswith('ST')].index, inplace=True)
data_3.drop(data_3[data_3['stock_short_name'].str.startswith('*ST')].index, inplace=True)
data_3.drop(data_3[data_3['stock_short_name'].str.startswith('PT')].index, inplace=True)
data_3.drop(data_3[data_3['stock_short_name'].str.startswith('*PT')].index, inplace=True)
# data_3 = data_3[~data_3['stock_short_name'].str.startswith('ST ') & ~data_3['stock_short_name'].str.startswith('PT ')]
data_3 = data_3[~data_3['industry_code'].str.startswith('J')]
data_3 = data_3[data_3['ending_date_of_statistics'].str.endswith('06-30') | data_3['ending_date_of_statistics'].str.endswith('12-31')]
data_3["ending_date_of_statistics"] = pd.to_datetime(data_3["ending_date_of_statistics"])
data_3['ending_date_of_statistics_h'] = data_3['ending_date_of_statistics'].dt.year.astype(str) + \
                                      data_3['ending_date_of_statistics'].dt.month.apply(half_year_label)
data_3 = data_3[['stock_code', 'ending_date_of_statistics_h', 'earnings_per_share']]   # tut14页表格
data_3.sort_values(by=['stock_code', 'ending_date_of_statistics_h'], inplace=True)
data_3['previous_earnings_per_share'] = data_3.groupby('stock_code')['earnings_per_share'].shift(1)
data_3['previous_earnings_per_share'] = data_3['previous_earnings_per_share'].fillna(0)
data_3['earnings_per_share'] = data_3['earnings_per_share'] - \
            data_3['ending_date_of_statistics_h'].apply(second_half_eps) * data_3['previous_earnings_per_share']
data_3['previous_2_earnings_per_share'] = data_3.groupby('stock_code')['earnings_per_share'].shift(2)
data_3["UE"] = data_3['earnings_per_share'] - data_3['previous_2_earnings_per_share']
data_3['SUE'] = data_3.groupby('stock_code').apply(calculate_sue).reset_index(level=0, drop=True)
data_3['SUE'] = data_3['SUE'].mask(data_3['SUE'].abs() > 1.96)
data_3.dropna(subset=['SUE'], inplace=True)

data_3['SUE_deciles'] = data_3.groupby('ending_date_of_statistics_h').apply(calculate_sue_deciles).reset_index(level=0, drop=True)
data_3['SUE_deciles'] += 1
data_3 = data_3[['stock_code', 'ending_date_of_statistics_h', 'SUE_deciles']]
data_3_ = pd.pivot_table(data_3, values='SUE_deciles', index='stock_code', columns='ending_date_of_statistics_h')
data_3_old_col = data_3_.columns
new_columns = [f'sue_deciles_{col}' for col in data_3_.columns]
data_3_.columns = new_columns
# data_3_.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data_3_.csv')

# step_4
data_4 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data/IAR_Rept.csv")
data_4 = data_4[(data_4['Reptyp'] == 2) | (data_4['Reptyp'] == 4)]
data_4 = data_4.rename(columns={'Stkcd': 'stock_code', 'Stknme_en': 'stock_short_name',
                                'Accper': 'ending_date_of_statistics', 'Reptyp': 'report_type',
                                'Annodt': 'announcement_date'})
data_4["ending_date_of_statistics"] = pd.to_datetime(data_4["ending_date_of_statistics"])
data_4["announcement_date"] = pd.to_datetime(data_4["announcement_date"])
data_4['ending_date_of_statistics_h'] = data_4['ending_date_of_statistics'].dt.year.astype(str) + \
                                      data_4['ending_date_of_statistics'].dt.month.apply(half_year_label)
data_4 = data_4[['stock_code', 'ending_date_of_statistics_h', 'announcement_date']]
data_4_ = pd.pivot_table(data_4, values='announcement_date', index='stock_code', columns='ending_date_of_statistics_h')
# data_4_old_col = data_4_.columns
new_columns = [f'ann_date_{col}' for col in data_4_.columns]
data_4_.columns = new_columns
# data_4_.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/data_4_.csv')

# step_5
# merged_1 = pd.merge(data_1, data_2[['trading_date', 'daily_mkt_return']], on='trading_date', how='left')
merged_1 = pd.merge(data_1, data_2[['trading_date', 'daily_mkt_return']], on='trading_date', how='left')
merged_2 = pd.merge(merged_1, data_3_, on='stock_code', how='left')
merged = pd.merge(merged_2, data_4_, on='stock_code', how='left')
merged = merged.sort_values(by=["trading_date", "stock_code"])
# print(merged.columns)

# step_6
merged["ARs"] = merged["daily_return"] - merged["daily_mkt_return"]
merged = merged.drop(columns=["daily_return", "daily_mkt_return"])
for col in data_3_old_col:
    sue_deciles = "sue_deciles_%s" % col
    ann_date = "ann_date_%s" % col
    event_panel = merged[["stock_code", "trading_date", "ARs", sue_deciles, ann_date]]
    event_panel["event_date"] = (event_panel["trading_date"] - event_panel[ann_date]).dt.days
    event_panel = event_panel[abs(event_panel["event_date"]) <= 60]
    # event_panel.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/11.csv')
    event_panel = event_panel.groupby(['event_date', sue_deciles])["ARs"].mean().reset_index()
    new_name = "CARs_%s" % col
    old_name = "sue_deciles_%s" % col
    event_panel[new_name] = event_panel.groupby(old_name)['ARs'].cumsum()  # 叠加
    # event_panel.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/22.csv')
    event_panel = event_panel.rename(columns={old_name: "sue_deciles"})
    event_panel = event_panel[['event_date', "sue_deciles", new_name]]
    if col != "2016h2":
        final_panel = pd.merge(final_panel, event_panel, on=['event_date', "sue_deciles"], how='left')
    else:
        final_panel = event_panel
car_columns = [col for col in final_panel.columns if col.startswith('CARs_')]
mean_values = final_panel[car_columns].mean(axis=1)
final_panel['mean_CARs'] = mean_values
final_panel = final_panel[["event_date", "sue_deciles", "mean_CARs"]]
# final_panel.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw4/final.csv')

grouped = final_panel.groupby('sue_deciles')
plt.figure(figsize=(10, 6))

for name, group in grouped:
    plt.plot(group['event_date'], group['mean_CARs'], label=f'sue_deciles={name}')

plt.xlabel('event_date')
plt.ylabel('mean_CARs')
plt.title('Mean CARs by sue_deciles over event_date')
plt.legend()
plt.grid(True)
plt.show()