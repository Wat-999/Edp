import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split


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
table_database_inf = table_database.mask(np.isinf, None) 
table_database_inf = table_database_inf.fillna(table_database_inf.apply('mean'))

#设为目标 所要划分的样本结果(测试集)
df_train = table_database_inf['label'].values
#删除列  所要划分的样本特征集(训练集)
train = table_database_inf.drop(['label'], axis=1)

# 随机抽取90%的数据作为训练数据，剩余10%作为测试资料
X_train, X_test, y_train, y_test = train_test_split(train, df_train, test_size=0.1, random_state=1)


# 使用XGBoost的原生版本需要对数据进行转化(封装训练和测试数据)
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
y_predicted = data_train_booster.predict(data_test)
y = data_test.get_label()
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


