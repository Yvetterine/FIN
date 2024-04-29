import pandas as pd
import statsmodels.api as sm


def stock_reg(group):
    stock_code = group["Stkcd"].iloc[0]
    X = group['mkt return premium']  # 假设 'market_return' 是市场收益率列
    y = group['stock return premium']  # 假设 'stock_return' 是股票收益率列
    X = sm.add_constant(X)  # 添加截距项
    model = sm.OLS(y, X).fit()  # 执行最小二乘回归

    beta = model.params['mkt return premium']
    # 如果只是将第一问的贝塔看成一个依据，p-value无用
    # beta_t_value = model.tvalues['mkt return premium']
    # beta_significance = model.pvalues['mkt return premium']

    r_squared = model.rsquared

    result = pd.DataFrame({
        "Stkcd": stock_code,
        'Beta': [beta],
        # 'Beta t-value': [beta_t_value],
        # 'Beta significance': [beta_significance],
        # 'R-squared': [r_squared],
    })
    return result


data_1 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw3/Q2/TRD_Week.csv")
data_1 = data_1[data_1['Markettype'] != 16]
data_2 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw3/Q2/TRD_Week1.csv")
data_2 = data_2[data_2['Markettype'] != 32]
sum_df = pd.concat([data_1, data_2], axis=0)    # 只剩下a和main的合并版

grouped_df = sum_df.groupby('Trdwnt')["Wretnd"].mean()
merge = pd.merge(sum_df, grouped_df, how="left", on=["Trdwnt"])  # 把mkt return放到合并的表里面

data_3 = pd.read_excel("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw3/Q2/weekly_risk_free_rate.xlsx")
data_3['trading_date_yw'] = pd.to_datetime(data_3['trading_date_yw'])
not_2018 = data_3['trading_date_yw'].dt.year != 2018
data_3.loc[not_2018, 'trading_date_yw'] += pd.Timedelta(weeks=1)
data_3['Week'] = data_3['trading_date_yw'].dt.strftime('%Y-%W')
data_3 = data_3.rename(columns={'Week': 'Trdwnt'})


merged_df = pd.merge(merge, data_3[['Trdwnt', 'risk_free_return']], on='Trdwnt')  # 把rf放到合并的表里面
merged_df = merged_df.rename(columns={"Wretnd_y": "mkt return"})
merged_df = merged_df.rename(columns={"Wretnd_x": "stock return"})
merged_df["stock return premium"] = merged_df["stock return"] - merged_df["risk_free_return"]
merged_df["mkt return premium"] = merged_df["mkt return"] - merged_df["risk_free_return"]
merged_df = merged_df.dropna()
# ----分时间-----
merge_1 = merged_df[(merged_df["Trdwnt"] <= "2018-52")]
merge_2 = merged_df[(merged_df["Trdwnt"] >= "2019-01") & (merged_df["Trdwnt"] <= "2020-52")]
merge_3 = merged_df[(merged_df["Trdwnt"] >= "2021-01") & (merged_df["Trdwnt"] <= "2022-52")]

grouped_by_stock = merge_1.groupby("Stkcd").apply(stock_reg)
grouped_by_stock['group'] = pd.qcut(grouped_by_stock['Beta'], q=10, labels=False)
grouped_by_stock.index.names = [None, None]
merge_2 = pd.merge(merge_2, grouped_by_stock[['Stkcd', 'group']], on='Stkcd')
# merged_df.index.names = [None, None]
# group_1 = pd.merge(merge_1, grouped_by_stock, how="left", left_on=["Stkcd"], right_on=["Stkcd"])
# --------------------------------P2--------------------------------------------
# merge_2 这张表已经具有了分组的组号
data_collection_group = pd.DataFrame(columns=['Group', 'Beta'])  # 初始化结果 DataFrame
result_sum = pd.DataFrame(columns=["Group_name", 'Beta', 'Beta t-value', 'Beta significance',
            'Alpha', 'Alpha t-value', 'Alpha significance', 'R-squared'])  # 初始化结果 DataFrame
for group, group_df in merge_2.groupby('group'):
    data_collection = []  # 初始化收集数据的列表
    for date, date_df in group_df.groupby('Trdwnt'):
        avg_stock_return = date_df['stock return premium'].mean()
        avg_mkt_return = date_df['mkt return premium'].mean()
        data_collection.append({'X': avg_mkt_return, 'Y': avg_stock_return})

    if data_collection:  # 检查数据是否为空
        X = [item['X'] for item in data_collection]
        y = [item['Y'] for item in data_collection]
        X = sm.add_constant(X)  # 添加截距项
        model = sm.OLS(y, X).fit()  # 执行最小二乘回归
        beta = model.params[1]
        data_collection_group = pd.concat([data_collection_group, pd.DataFrame({'Group': [group], 'Beta': [beta]})], ignore_index=True)

        # 打印table2
        beta = model.params[1]
        beta_t_value = model.tvalues[1]
        beta_significance = model.pvalues[1]
        alpha = model.params[0]
        alpha_t_value = model.tvalues[0]
        alpha_significance = model.pvalues[0]

        r_squared = model.rsquared

        result_sum = pd.concat([result_sum, pd.DataFrame({"Group_name": [group], 'Beta': [beta], 'Beta t-value': [beta_t_value],
            'Beta significance': [beta_significance], 'Alpha': [alpha], 'Alpha t-value': [alpha_t_value],
            'Alpha significance': [alpha_significance], 'R-squared': [r_squared]})], ignore_index=True)

result_sum.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw3/aaaa.csv', index=False)

        # print(model.summary())  # 笑死了，看每一组的obs不够数，一查发现，估计是春节休市
# -------------------P3--------------------
merge_3 = pd.merge(merge_3, grouped_by_stock[['Stkcd', 'group']], on='Stkcd')
avg = merge_3.groupby("group")["stock return premium"].mean()
total = pd.merge(avg, data_collection_group, left_index=True, right_index=True)
X = total['Beta']  # 假设 'market_return' 是市场收益率列
y = total['stock return premium']  # 假设 'stock_return' 是股票收益率列
X = sm.add_constant(X)  # 添加截距项
model = sm.OLS(y, X).fit()  # 执行最小二乘回归
print(model.summary())