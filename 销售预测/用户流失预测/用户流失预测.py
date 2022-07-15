import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cluster import KMeans
from pandas import MultiIndex
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')  #忽略警告设置


#1导入与导出数据
table = pd.read_csv('rawdata/table1.csv')
#获取列信息
F1_1 = table[['label', 'sampleid', 'historyvisit_7ordernum', 'historyvisit_totalordernum', 'ordercanceledprecent', 'ordercanncelednum',
              'historyvisit_avghotelnum', 'delta_price1', 'businessrate_pre', 'cr_pre', 'landhalfhours', 'starprefer', 'price_sensitive',
              'commentnums_pre2', 'cancelrate_pre', 'novoters_pre2', 'novoters_pre', 'commentnums_pre2', 'cancelrate_pre', 'lowestprice_pre',
              'uv_pre', 'uv_pre2', 'hoteluv', 'cancelrate', 'novoters', 'commentnums', 'hotelcr', 'visitnum_oneyear', 'ordernum_oneyear',
              'cityorders', 'iforderpv_24h', 'consuming_capacity', 'avgprice', 'ctrip_profits', 'customer_value_profit', 'commentnums_pre',
              'delta_price2', 'ordernum_oneyear', 'firstorder_bu', 'd', 'arrival']]
#重命名列名
F1_1.columns = ['label', 'ID', 'F1.1', 'F1.2', 'F1.3', 'F1.4', 'F1.5', 'F1.6', 'F1.7', 'F1.8', 'F1.9', 'F1.10', 'F1.11', 'F1.12', 'F1.13', 'F1.14',
                'F1.15', 'F1.16', 'F1.17', 'F1.18', 'F1.19', 'F1.20', 'F1.21', 'F1.22', 'F1.23', 'F1.24', 'F1.25', 'F1.26', 'F1.27', 'F1.28', 'F1.29',
                'F1.30', 'F1.31', 'F1.32', 'F1.33', 'F1.34', 'F1.35', 'F1.36', 'F1.37', 'F1.38', 'F1.39']
#空值替换为NA
F1_1 = F1_1.fillna('NA')
F1_1.to_csv('workeddata/F1_1.csv', index=False, encoding="utf_8_sig")
#table.info()
#print(F1_1)


#2客户基本数据分析处理、缺失值填补

F1_1 = pd.read_csv('workeddata/F1_1.csv')
#读取列
F1_2_1 = F1_1[['ID', 'F1.1', 'F1.2', 'F1.4', 'F1.5', 'F1.9', 'F1.15', 'F1.23', 'F1.24', 'F1.27', 'F1.35', 'F1.38', 'F1.39']]
#空值替换为0
F1_2_1 = F1_2_1.fillna(0)
#读取列
F1_2_2 = F1_1[['label', 'ID']]
#设置所需列的空值替换为均值
title = ['F1.3', 'F1.6', 'F1.7', 'F1.8', 'F1.10', 'F1.11', 'F1.12', 'F1.13', 'F1.14', 'F1.16', 'F1.17', 'F1.18', 'F1.19',
         'F1.20', 'F1.21', 'F1.22', 'F1.25', 'F1.26', 'F1.28', 'F1.29', 'F1.30', 'F1.31', 'F1.32', 'F1.33', 'F1.34', 'F1.36',
         'F1.37']
for t in title:
    #获取每一列的均值
    mean = F1_1[[t]].mean().values[0]
    #获取列
    null = F1_1[['ID', t]]
    #空值替换为均值
    null = null.fillna(mean)
    #根据用户ID合并特征
    F1_2_2 = F1_2_2.join(null.set_index('ID'), on='ID')
#根据用户ID合并表格
F1_2 = F1_2_1.join(F1_2_2.set_index('ID'), on='ID')
#计算所需列值除以该列的均值，结果替换该列的值
for t in list(F1_2):
    #跳过以下几列
    if t == 'ID' or t == 'label' or t == 'F1.38' or t == 'F1.39':
        continue #跳出循环，执行后面的
    mean = F1_2[[t]].mean().values[0]
    #列值/均值，然后赋值到原有列
    F1_2[t] = F1_2[t]/mean

F1_2 = F1_2[['label', 'ID', 'F1.1', 'F1.2', 'F1.3', 'F1.4', 'F1.5', 'F1.6', 'F1.7', 'F1.8', 'F1.9', 'F1.10',
             'F1.11', 'F1.12', 'F1.13', 'F1.14', 'F1.15', 'F1.16', 'F1.17', 'F1.18', 'F1.19', 'F1.20', 'F1.21',
             'F1.22', 'F1.23', 'F1.24', 'F1.25', 'F1.26', 'F1.27', 'F1.28', 'F1.29', 'F1.30', 'F1.31', 'F1.32',
             'F1.33', 'F1.34', 'F1.35', 'F1.36', 'F1.37', 'F1.38', 'F1.39']]
#为相对路径
F1_2.to_csv('workeddata/F1_2.csv', index=False, encoding="utf_8_sig")
#print(F1_2)


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


#数据挖掘

#读取文件
table_database = pd.read_csv('workeddata/table_database.csv')
#名义特征设定。大部分名义特征在读取时会被转变为数值特征，为此，要将这些特征转换为名义特征
table_database['F1.47'] = pd.factorize(table_database['F1.47'])[0].astype(np.uint16)
table_database['F1.48'] = pd.factorize(table_database['F1.48'])[0].astype(np.uint16)


#删除列
table_database = table_database.drop(['F1.38', 'F1.39'], axis=1)

#替换数据集中的inf与nan，并替换为所在列的均值（平均时分母不计inf nan数量）
#注意：在数据集做运算，若其中一列为缺失值或0，就会出现inf、nan，会导致在划分数据集时报错
table_database_inf = table_database.mask(np.isinf, None) #只把元素是np.isinf，全部替换为指定值  mask：显示为假值，替换为真值，戴上面具看到的是假面
table_database_inf = table_database_inf.fillna(table_database_inf.apply('mean'))

#设为目标 所要划分的样本结果(测试集)
df_train = table_database_inf['label'].values
#删除列  所要划分的样本特征集(训练集)
train = table_database_inf.drop(['label'], axis=1)

# 随机抽取90%的数据作为训练数据，剩余10%作为测试资料
X_train, X_test, y_train, y_test = train_test_split(train, df_train, test_size=0.1, random_state=1)


# 使用XGBoost的原生版本需要对数据进行转化
data_train = xgb.DMatrix(X_train, y_train) #构造训练集
data_test = xgb.DMatrix(X_test, y_test) #构造测试集
# 设置参数
# 以XGBoos训练。max.depth表示树的深度，eta表示权重参数，objective表示训练目标的学习函数
param = {'max_depth': 4, 'eta': 0.2, 'objective': 'reg:linear'}
watchlist = [(data_test, 'test'), (data_train, 'train')]
# 表示训练次数
n_round = 10
# 训练数据载入模型
data_train_booster = xgb.train(param, data_train, num_boost_round=n_round, evals=watchlist)



# 以XGBoost测试。分别对训练与测试数据进行测试，其中auc为分类器评价指标，其值越大，则分类器效果越好
# 计算错误率
y_predicted = data_train_booster.predict(data_train)
y = data_train.get_label()
accuracy = sum(y == (y_predicted > 0.5)) #用于设定阀值，概率大于0.5
accuracy_rate = float(accuracy) / len(y_predicted)
print('样本总数：{0}'.format(len(y_predicted)))
print('正确数目：{0}'.format(accuracy))
print('正确率：{0:.10f}'.format((accuracy_rate)))

# 使用F-measure评价测试
#将数组转为dataframe
y_train_f = pd.DataFrame(y_train)
y_predicted_f = pd.DataFrame(y_predicted)
#新建列，列值为索引值
y_train_f['index'] = y_train_f.index.values
y_predicted_f['index'] = y_predicted_f.index.values
#重命名为列名
y_train_f.columns = ['train', 'index']
y_predicted_f.columns = ['y_n', 'index']
#新建列，列值为0
y_predicted_f['test'] = 0
#当y_n列值大于0.5时，把test列当值替换为1
y_predicted_f.loc[y_predicted_f['y_n'] > 0.5, 'test'] = 1
#读取列
y_predicted_f = y_predicted_f[['test', 'index']]
#根据index合并表
F = y_train_f.join(y_predicted_f.set_index('index'), on='index')
#读取列
F = F[['train', 'test']]
#求train等于1和text等于1的数据量
tp = F[(F.train == 1) & (F.test == 1)].test.count()
#求train等于0和text等于1的数据量
fp = F[(F.train == 0) & (F.test == 1)].test.count()
#求train等于1和text等于0的数据量
fn = F[(F.train == 1) & (F.test == 0)].test.count()
#求train等于0和text等于0的数据量
tn = F[(F.train == 0) & (F.test == 0)].test.count()

# 对比两种方式的准确率，可以知道F-measure的方式较AUC效果来的差。
P = tp/(tp+fp)
R = tn/(tn+fn)
F1 = 2*P*R/(P+R)
print('F-measure值：{0:.10f}'.format(F1))
#F值介于[0, 1]说明模型比较有效








