import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import skew, kurtosis

data_1 = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw3/Q1/TRD_Index.csv")
data_1 = data_1[data_1['Indexcd'] == 300]
data_1["Trddt"] = pd.to_datetime(data_1["Trddt"])
data_1["Match_month"] = data_1['Trddt'].dt.to_period('M')
# data_1.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw3/llllxexe3.csv', index=False)
grouped_by_month = data_1.groupby(pd.Grouper(key='Match_month'))
monthly_last_index = grouped_by_month["Clsindex"].last()
monthly_300_index_return = monthly_last_index.pct_change()  # 使用pct_change()函数计算月度回报率
monthly_300_index_return.to_csv('C:/Users/yifan/Desktop/大二/下学期/FIN3080/hw3/llllxe3.csv', index=False)
monthly_300_index_return = monthly_300_index_return.dropna()

mean_return = monthly_300_index_return.mean()
std_return = monthly_300_index_return.std()
skewness = skew(monthly_300_index_return)
kurt = kurtosis(monthly_300_index_return)

print("Mean return:", mean_return)
print("Standard deviation:", std_return)
print("Skewness:", skewness)
print("Kurtosis:", kurt)
# -----------------------------------------------------------------------------
# 注意第二问画出来的直方图的柱子的高度大于1
result_df = pd.DataFrame({
    'Date': monthly_300_index_return.index,
    'Index_Return': monthly_300_index_return.values
})
plt.hist(result_df["Index_Return"], bins=30, edgecolor='black', density=True)   # bins=16/50???
plt.title('Histogram of Monthly CSI 300 Index Returns')
plt.xlabel('Returns')
plt.ylabel('Density')
plt.grid(True)
plt.show()
# -----------------------------------------------------------------------------
shapiro_test_stat, shapiro_p_value = stats.shapiro(result_df["Index_Return"])
print("Shapiro-Wilk test statistic:", shapiro_test_stat)
print("Shapiro-Wilk test p-value:", shapiro_p_value)