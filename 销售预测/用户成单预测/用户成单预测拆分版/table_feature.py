import pandas as pd

#6特征汇总

F1 = pd.read_csv('workeddata/F1.csv')
F2 = pd.read_csv('workeddata/F2.csv')
F3 = pd.read_csv('workeddata/F3.csv')
F23 = pd.read_csv('workeddata/F2.3.csv')

#读取列
F2no = F2[['ID', 'F2.2', 'F2.19', 'F2.22', 'F2.25', 'F2.28', 'F2.31', 'F2.34']]
F3no = F3[['ID','F3.13', 'F3.14', 'F3.15', 'F3.16', 'F3.17', 'F3.18', 'F3.19', 'F3.20',
           'F3.21', 'F3.22', 'F3.23', 'F3.31', 'F3.32', 'F3.33']]

#删除列
F2 = F2.drop(['F2.2', 'F2.19', 'F2.22', 'F2.25', 'F2.28', 'F2.31', 'F2.34'], axis=1)
F3 = F3.drop(['F3.13', 'F3.14', 'F3.15', 'F3.16', 'F3.17', 'F3.18', 'F3.19', 'F3.20',
              'F3.21', 'F3.22', 'F3.23', 'F3.31', 'F3.32', 'F3.33'], axis=1)

#根据用户ID合并表
feature = F1.join(F2.set_index('ID'), on='ID')
feature = feature.join(F3.set_index('ID'), on='ID')
feature = feature.join(F23.set_index('ID'), on='ID')
#print(feature)


"""特征归一化"""
#读取所有列名遍历
c = 0
for t in list(feature):
    #跳过前4列
    if c < 4:
        c = c + 1
        continue   #跳出循环
    #读取列
    demo = feature[[t]]
    #获取当前列最大值
    max = demo.sort_values(t, ascending=False).head(1)
    maxvalue = max.get(t).values[0]
    #归一化：列值/最大值
    feature[t] = feature[t] / maxvalue
#print(feature)


#把数据写入表格，以待建模时读取

#空值替换为1
feature = feature.fillna(1)
#根据用户ID合并表
feature = feature.join(F2no.set_index('ID'), on='ID')
feature = feature.join(F3no.set_index('ID'), on='ID')
feature = feature[['ID', 'F1.1', 'F1.2', 'F1.3', 'F2.1', 'F2.2', 'F2.3', 'F2.4', 'F2.5', 'F2.6', 'F2.7', 'F2.8', 'F2.9', 'F2.10',
                   'F2.11', 'F2.12', 'F2.13', 'F2.14', 'F2.15', 'F2.16', 'F2.17', 'F2.18', 'F2.19', 'F2.20',
                   'F2.21', 'F2.22', 'F2.23', 'F2.24', 'F2.25', 'F2.26', 'F2.27', 'F2.28', 'F2.29', 'F2.30',
                   'F2.31', 'F2.32', 'F2.33', 'F2.34', 'F2.35', 'F2.36',
                   'F3.1', 'F3.2', 'F3.3', 'F3.4', 'F3.5', 'F3.6', 'F3.7', 'F3.8', 'F3.9','F3.10',
                   'F3.11', 'F3.12', 'F3.13', 'F3.14', 'F3.15', 'F3.16', 'F3.17', 'F3.18', 'F3.19', 'F3.20',
                   'F3.21', 'F3.22', 'F3.23', 'F3.24', 'F3.25', 'F3.26', 'F3.27', 'F3.28', 'F3.29', 'F3.30',
                   'F3.31', 'F3.32', 'F3.33', 'F3.34', 'F3.35', 'F3.36', 'F3.37', 'F3.38', 'F3.39', 'F3.40',
                   'F3.41', 'F3.42', 'F3.43', 'F3.44', 'F3.45', 'F3.46', 'F3.47', 'F3.48', 'F3.49', 'F3.50',
                   'F3.51', 'F3.52', 'F3.53', 'F3.54', 'F3.55', 'F3.56', 'F3.57', 'F3.58', 'F3.59', 'F3.60',
                   'F3.61', 'F3.62', 'F3.63', 'F3.64', 'F3.65', 'F3.66', 'F3.67', 'F3.68', 'F3.69', 'F3.70',
                   'F3.71', 'F3.72', 'F3.73', 'F3.74', 'F3.75', 'F3.76', 'F3.77', 'F3.78', 'F3.79', 'F3.80',
                   'F3.81', 'F3.82', 'F3.83', 'F3.84', 'F3.85', 'F3.86', 'F3.87', 'F3.88', 'F3.89',
                   'F2.3.1', 'F2.3.2', 'F2.3.3', 'F2.3.4', 'F2.3.5', 'F2.3.6', 'F2.3.7', 'F2.3.8', 'F2.3.9', 'F2.3.10',
                   'F2.3.11', 'F2.3.12', 'F2.3.13', 'F2.3.14', 'F2.3.15', 'F2.3.16', 'F2.3.17', 'F2.3.18', 'F2.3.19', 'F2.3.20',
                   'F2.3.21', 'F2.3.22', 'F2.3.23', 'F2.3.24']]
#空值替换为0
feature = feature.fillna(0)
#把数据写入table_feature.csv，为相对路径
feature.to_csv('workeddata/table_feature.csv', index=False, encoding="utf_8_sig")
#print(feature)

