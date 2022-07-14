import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
#3询问与入住日期的装换，产生新特征的分析与数据清理

F1_2 = pd.read_csv('workeddata/F1_2.csv')
# 将日期作转换，算出入住日期与询问日期相差几天
F1_2['F1.40'] = pd.to_datetime(F1_2['F1.39']) - pd.to_datetime(F1_2['F1.38'])
#F1.40的值：0 days, 将格式转为str
F1_2['F1.40'] = F1_2['F1.40'].astype('str')
#获取数值
F1_2['F1.40'] = F1_2['F1.40'].apply(lambda x: x.split(' ')[0])
# 将实际日期中的假日(周六、周日)转化为1，其余转化成0
#将原先的格式转为datetime
F1_2['F1.41'] = pd.to_datetime(F1_2['F1.38'])
F1_2['F1.42'] = pd.to_datetime(F1_2['F1.39'])
#将日期转为星期几
F1_2['F1.41'] = F1_2['F1.41'].dt.dayofweek
F1_2['F1.42'] = F1_2['F1.42'].dt.dayofweek
#将周一到周五的数值替换为0
F1_2.loc[F1_2['F1.41'] <= 5, 'F1.41'] = 0
F1_2.loc[F1_2['F1.42'] <= 5, 'F1.42'] = 0
#将周末的数值替换为1
F1_2.loc[F1_2['F1.41'] > 5, 'F1.41'] = 1
F1_2.loc[F1_2['F1.42'] > 5, 'F1.42'] = 1

#4缺失值处理
# 二次产生的变数
F1_2['F1.43'] = F1_2['F1.26']/F1_2['F1.27']
F1_2['F1.44'] = F1_2['F1.32']/F1_2['F1.33']
F1_2['F1.45'] = F1_2['F1.24']/F1_2['F1.23']

# 空值取代
F1_2 = F1_2.fillna(0)
# 二次产生的变数
F1_2['F1.46'] = F1_2['F1.34']/F1_2['F1.15']


mean = F1_2[['F1.46']].mean().values[0]
#空值替换为均值
F1_2 = F1_2.fillna(mean)
#print(F1_2)

#用聚类算法产生新特征，并把结果写入表中
# 设置要进行聚类的字段
loan1 = np.array(F1_2[['F1.1', 'F1.2', 'F1.3', 'F1.4', 'F1.5', 'F1.6', 'F1.7']])
# 将用户分成3类
clf1 = KMeans(n_clusters=3)
# 将数据代入到聚类模型中
clf1 = clf1.fit(loan1)
# 在原始数据表中增加聚类结果标签
F1_2['F1.47'] = clf1.labels_

# 设置要进行聚类的字段
loan2 = np.array(F1_2[['F1.21', 'F1.22', 'F1.23', 'F1.24', 'F1.25']])
# 将用户分成3类 设置类别为3
clf2 = KMeans(n_clusters=3)
# 将数据代入到聚类模型中
clf2 = clf2.fit(loan2)
# 在原始数据表中增加聚类结果标签
F1_2['F1.48'] = clf2.labels_

table_database = F1_2
table_database.to_csv('workeddata/table_database.csv', index=False, encoding="utf_8_sig")
#print(F1_2)
