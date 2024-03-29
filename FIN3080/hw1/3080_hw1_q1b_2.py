import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

df = pd.read_csv("C:/Users/yifan/Desktop/大二/下学期/FIN3080/excel/Q1 result/1b.csv", header=None,  dtype=str)
time = pd.to_datetime(df.iloc[0, :])
main_board_data = df.iloc[1, :].astype(float).values
gem_data = df.iloc[2, :].astype(float).values

time_yearly = time[::12]
main_board_data_yearly = main_board_data[::12]
gem_data_yearly = gem_data[::12]

plt.plot(time, main_board_data, label='GEM', marker='o', markersize=3)
plt.plot(time, gem_data, label='Main Board', marker='o', markersize=3)

plt.title('Time Series for Median P/E Ratio by Market Type')
plt.xlabel('Time')
plt.ylabel('Median P/E Ratio')

plt.legend()
plt.xticks(time_yearly)
date_form = DateFormatter("%Y")
plt.gca().xaxis.set_major_formatter(date_form)
plt.gcf().autofmt_xdate()

plt.tight_layout()
plt.show()