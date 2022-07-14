#2建立模型
"""最后是进行数据分析的阶段。本阶段会用到上一步产生的数据集，然后将数据随机抽样90%作为训练数据集，剩下10%作为测试数据集，
并且按照XGBoost函数的格式进行数据挖掘的计算。而后针对训练出来的模型，将测试数据导入其中，得到预测数据。将预测数据与是假数据对比，
通过计算模型评估指标(ACU)进行计算后，对训练模型做出评价"""
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split

#读取文件
train = pd.read_csv('workeddata/table_database.csv')
#名义特征设定。大部分名义特征在读取是会被装变为数值特真，为次，要将这些特征装换为名义特征
train['F2.19'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F2.22'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F2.25'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F2.28'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F2.31'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F2.34'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F3.31'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F3.32'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
train['F3.33'] = pd.factorize(train['F2.19'])[0].astype(np.uint16)
#删除列
train = train.drop(['F1.1', 'F1.2', 'F1.3'], axis=1)

#设为目标 所要划分的样本结果(测试集)
df_train = train['target'].values

#删除列  所要划分的样本特征集(训练集)
train = train.drop(['target'], axis=1)


#随机抽取90%的资料作为训练数据，剩余10%作为测试数据
X_train, X_test, y_train, y_test = train_test_split(train, df_train, test_size=0.1, random_state=1)
#test_size：测试数据的比例
#random_state：是一个随机种子，是在任意带有随机性的类或函数里作为参数来控制随机模式。当random_state取某一个值时，也就确定了一种规则
# 使用XGBoost的原生版本需要对数据进行转化(封装训练和测试数据)
data_train = xgb.DMatrix(X_train, y_train) #构造训练集
data_test = xgb.DMatrix(X_test, y_test) #构造测试集
# 设置参数 'max_depth':表示树的深度   'eta':表示权重参数  'objective':表示训练目标的学习函数
param = {'max_depth': 4, 'eta': 0.2, 'objective': 'reg:linear'}
watchlist = [(data_test, 'test'), (data_train, 'train')]
#表示训练次数
n_round = 1000
# 训练数据载入模型
data_train_booster = xgb.train(param, data_train, num_boost_round=n_round, evals=watchlist)

# 计算错误率
y_predicted = data_train_booster.predict(data_train)
y = data_train.get_label()
accuracy = sum(y == (y_predicted > 0.5))
accuracy_rate = float(accuracy) / len(y_predicted)
print('测试集样本总数：{0}'.format(len(y_predicted)))
print('正确数目：{0}'.format(accuracy))
print('正确率：{0:.10f}'.format((accuracy_rate)))


#对测试集进行预测(回归问题用MSE:均方误差即预测误差
from sklearn.metrics import mean_squared_error
dtest = xgb.DMatrix(X_test)
ans = data_train_booster.predict(dtest)
print('mse:', mean_squared_error(y_test, ans))


