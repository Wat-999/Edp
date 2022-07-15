import pandas as pd
#2用户基本资料分析处理
F1 = pd.read_csv('rawdata/table_1.csv')
#把表格中对缺失值替换成'未知'，以此区别于其他特征
F1 = F1.fillna('未知')
# 重命名列名， F1.1:性别 , F1.2:省份 , F1.3:年龄段
F1.columns = ['ID', 'F1.1', 'F1.2', 'F1.3']
F1.to_csv('workeddata/F1.csv', index=False, encoding="utf_8_sig")
#print(F1)
