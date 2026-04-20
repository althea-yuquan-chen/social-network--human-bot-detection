import pandas as pd
from datetime import datetime

# 读取xlsx文件
df = pd.read_excel('C:/Users/Fang/Desktop/信管/社会网络分析/xlsx数据/train.xlsx')

# 将"created_at"列转换为datetime类型
df['created_at'] = pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S +0000 %Y')

# 获取当前日期
current_date = datetime.now()

# 计算账号注册天数
df['account_age'] = (current_date - df['created_at']).dt.days

# 保存结果
df.to_excel('C:/Users/Fang/Desktop/信管/社会网络分析/xlsx数据/train1.xlsx', index=False)
