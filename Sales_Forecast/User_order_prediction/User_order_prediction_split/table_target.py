import pandas as pd

#1读取原始数据
table_target = pd.read_csv('rawdata/table_0.csv')
#重命名列名，ID为用户id，target为预测结果
table_target.columns = ['ID', 'target']
#把数据写入table_target.csv文件
table_target.to_csv('workeddata/table_target.csv', index=False, encoding='utf_8_sig')
#print(table_target)
