#7数据挖掘

#7.1数据合并
feature = pd.read_csv('workeddata/table_feature.csv')
target = pd.read_csv('workeddata/table_target.csv')
#根据用户ID合并表格
database = feature.join(target.set_index('ID'), 'ID')
#空值替换为0
database = database.fillna(0)
#把数据写入table_database.csv
database.to_csv('workeddata/table_database.csv', index=False, encoding="utf_8_sig")
#print(database)