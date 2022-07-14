import pandasas as pd

#4用户APP行为的分析处理
"""这里的数据必须要进行一个摊平的动作，摊平的指标使用行为类型，因为从table_3表actionType字段(行为类型)了解到行为类型一共有9个，其中1是唤醒APP；
2～4是浏览产品，无先后关系；5～9则是有先后关系的，从填写表单到提交订单再到支付。因此，可以先摊平，然后根据摊平后的部分，做出特征变换的处理"""

userAction = pd.read_csv('rawdata/table_3.csv')
# F3.1 所有动作_总次数
#根据userid分组求每个用户的动作次数(计数)
F3_1 = userAction.groupby('userid', as_index=False).count()
F3_1 = F3_1[['userid', 'actionType']]
F3_1.columns = ['ID', 'F3.1']  #重命名列名

# F3.2 非支付动作_次数
#筛选动作编号小于5的，再根据userid分组求每个用户的动作次数(计数)
F3_2 = userAction[userAction.actionType < 5].groupby('userid', as_index=False).count()
F3_2 = F3_2[['userid', 'actionType']]
F3_2.columns = ['ID', 'F3.2']

# F3.3 支付动作_次数
#筛选动作编号大于或等于5的，再根据userid分组求每个用户的动作次数(计数)
F3_3 = userAction[userAction.actionType >= 5].groupby('userid', as_index=False).count()
F3_3 = F3_3[['userid', 'actionType']]
F3_3.columns = ['ID', 'F3.3']

# 合并
F3 = F3_1.join(F3_2.set_index('ID'), on='ID')
F3 = F3.join(F3_3.set_index('ID'), on='ID')
#print(F3)

#从userAction表清洗出以下新增字段
# F3.4 动作1_次数
# F3.5 动作2_次数
# F3.6 动作3_次数
# F3.7 动作4_次数
# F3.8 动作5_次数
# F3.9 动作6_次数
# F3.10 动作7_次数
# F3.11 动作8_次数
# F3.12 动作9_次数
a1 = 4
for i in range(1, 10):
    #列名
    title1 = 'F3.' + str(a1)
    #获取每一个动作的信息，再根据userid分组，求每个用户每个动作的次数
    action1 = userAction[userAction.actionType == i].groupby('userid', as_index=False).count()
    action1 = action1[['userid', 'actionType']]
    #重命名列名
    action1.columns = ['ID', title1]
    F3 = F3.join(action1.set_index('ID'), on='ID') #合并特征
    a1 = a1 + 1
#0替换空值
F3 = F3.fillna(0)
#print(F3)

#从userAction表清洗出以下新增字段
# F3.13 非支付动作_占比
# F3.14 支付动作_占比
# F3.15 动作1_占比
# F3.16 动作2_占比
# F3.17 动作3_占比
# F3.18 动作4_占比
# F3.19 动作5_占比
# F3.20 动作6_占比
# F3.21 动作7_占比
# F3.22 动作8_占比
# F3.23 动作9_占比
a2 = 13
for i in range(2, 13):
    #设置列名
    title2 = 'F3.' + str(a2)
    actiontitle = 'F3.' + str(i)
    #求每种动作的占比
    F3[title2] = F3[actiontitle] / F3['F3.1']
    a2 = a2 + 1

#print(F3)

#使用diff(actionTime)函数计算时间间隔，然后计算出均值、方差、最小值、最大值
#读取userid和actionTime两列
timeinterval = userAction[['userid', 'actionTime']]

#跟俊userid分组，用diff函数计算出每一行actionTime与上一行的差值，结果赋值到新列interval
timeinterval['interval'] = timeinterval.groupby('userid').actionTime.diff()

#读取userid和interval两列
timeinterval1 = timeinterval[['userid', 'interval']]

# F3.24 时间间隔_均值
#根据userid分组，求均值
F3_24 = timeinterval1.groupby('userid', as_index=False).mean()
F3_24.columns = ['ID', 'F3.24']  #重命名列名
F3 = F3.join(F3_24.set_index('ID'), on='ID')

# F3.25 时间间隔_方差
#根据userid分组，求方差
F3_25 = timeinterval1.groupby('userid', as_index=False).var()
F3_25.columns = ['ID', 'F3.25']  #重命名列名
F3 = F3.join(F3_25.set_index('ID'), on='ID')

# F3.26 时间间隔_最小值
#根据userid分组，求最小值
F3_26 = timeinterval1.groupby('userid', as_index=False).min()
F3_26.columns = ['ID', 'F3.26']  #重命名列名
F3 = F3.join(F3_26.set_index('ID'), on='ID')

# F3.27 时间间隔_最大值
#根据userid分组，求最大值
F3_27 = timeinterval1.groupby('userid', as_index=False).max()
F3_27.columns = ['ID', 'F3.27']  #重命名列名
F3 = F3.join(F3_27.set_index('ID'), on='ID') #合并特征

#print(F3)
#获得最后3个时间的时间间隔与动作，可能有点客户没有3个动作(从填写表单到提交订单再到支付)，因此要对空值进行填补，填补值为该特征最大值
#根据actionTime 降序，再根据userid分组，获取前3条数据
top3time = timeinterval.sort_values('actionTime', ascending=False).groupby('userid', as_index=False).head(3)
#根据userid分组，求最大值
top3timemax = top3time.groupby('userid').max()
# F3.28 时间间隔_倒数第1个
#根据userid分组，获取第一条数据
F3_28 = top3time.groupby('userid', as_index=False).head(1)
F3_28 = F3_28[['userid', 'interval']]  #重命名列名
# 对空值进行填补，填补值为该特征最大值
F3_28null = F3_28.set_index('userid').isnull()  #isnull()判断缺失值，若该处为缺失值，返回True，该处不为缺失值，则返回False
F3_28null = F3_28null[F3_28null.interval == True]  #Interval类描述了一个连续的范围区间，这个区间可以是闭、开、半闭半开、无穷的，他的区间值不一定是数字，可以包含任何的数据类型，比如字符串，时间等等，同时他和python的各种操作(=, >等)也是兼容的
for i in F3_28null.index.values:
    max = top3timemax.at[i, "interval"]  #单元格选取(点选取)：df.at[]，df.iat[]。准确定位一个单元格。
    F3_28.loc[F3_28['userid'] == i, 'interval'] = max
F3_28.columns = ['ID', 'F3.28']
F3 = F3.join(F3_28.set_index('ID'), on='ID')   #合并特征

# F3.29 时间间隔_倒数第2个
F3_29 = top3time.groupby('userid', as_index=False).head(2)  #获取前2条
F3_29 = top3time.groupby('userid', as_index=False).tail(1)  #获取最后一条数据
F3_29 = F3_29[['userid', 'interval']]
# 对空值进行填补，填补值为该特征最大值
F3_29null = F3_29.set_index('userid').isnull()
F3_29null = F3_29null[F3_29null.interval == True]
for i in F3_29null.index.values:
    max = top3timemax.at[i, "interval"]
    F3_29.loc[F3_29['userid'] == i, 'interval'] = max
F3_29.columns = ['ID', 'F3.29']
F3 = F3.join(F3_29.set_index('ID'), on='ID')

# F3.30 时间间隔_倒数第3个
F3_30 = top3time.groupby('userid', as_index=False).tail(1)
F3_30 = F3_30[['userid', 'interval']]
# 对空值进行填补，填补值为该特征最大值
F3_30null = F3_30.set_index('userid').isnull()
F3_30null = F3_30null[F3_30null.interval == True]
for i in F3_30null.index.values:
    max = top3timemax.at[i, "interval"]
    F3_30.loc[F3_30['userid'] == i, 'interval'] = max
F3_30.columns = ['ID', 'F3.30']
F3 = F3.join(F3_30.set_index('ID'), on='ID')
#print(F3)

# 继续处理剩余特征
#根据actionTime 降序，再根据userid分组，获取前3条数据
top3action = userAction.sort_values('actionTime', ascending=False).groupby('userid', as_index=False).head(3)
#读取userid和actionType两列
top3actionmax = top3action[['userid', 'actionType']]  #actionType行为类型
top3actionmax = top3actionmax.groupby('userid').max()  #根据userid分组，求最大值
# F3.31 动作_倒数第1个
F3_31 = top3action.groupby('userid', as_index=False).head(1)
F3_31 = F3_31[['userid', 'actionType']]  #重新命名列名
# 对空值进行填补，填补值为该特征最大值
F3_31null = F3_31.set_index('userid').isnull()
F3_31null = F3_31null[F3_31null.actionType == True]
for i in F3_31null.index.values:
    max = top3actionmax.at[i, "actionType"]
    F3_31.loc[F3_31['userid'] == i, 'actionType'] = max
F3_31.columns = ['ID', 'F3.31']
F3 = F3.join(F3_31.set_index('ID'), on='ID')  #合并特征

# F3.32 动作_倒数第2个
F3_32 = top3action.groupby('userid', as_index=False).head(2)
F3_32 = top3action.groupby('userid', as_index=False).tail(1)
F3_32 = F3_32[['userid', 'actionType']]
# 填充空值
F3_32null = F3_32.set_index('userid').isnull()
F3_32null = F3_32null[F3_32null.actionType == True]
for i in F3_32null.index.values:
    max = top3actionmax.at[i, "actionType"]
    F3_32.loc[F3_32['userid'] == i, 'actionType'] = max
F3_32.columns = ['ID', 'F3.32']
F3 = F3.join(F3_32.set_index('ID'), on='ID')

# F3.33 动作_倒数第3个
F3_33 = top3action.groupby('userid', as_index=False).tail(1)
F3_33 = F3_33[['userid', 'actionType']]
# 对空值进行填补，填补值为该特征最大值
F3_33null = F3_33.set_index('userid').isnull()
F3_33null = F3_33null[F3_33null.actionType == True]
for i in F3_33null.index.values:
    max = top3actionmax.at[i, "actionType"]
    F3_33.loc[F3_33['userid'] == i, 'actionType'] = max
F3_33.columns = ['ID', 'F3.33']
F3 = F3.join(F3_33.set_index('ID'), on='ID')
#print(F3)

#继续处理剩余特征
# F3.34 时间间隔_倒数3个_均值
F3_34 = top3time[['userid', 'interval']].groupby('userid',as_index=False).mean()
F3_34.columns = ['ID', 'F3.34']
F3 = F3.join(F3_34.set_index('ID'), on='ID')

# F3.35 时间间隔_倒数3个_方差
F3_35 = top3time[['userid', 'interval']].groupby('userid', as_index=False).var()
F3_35.columns = ['ID', 'F3.35']
F3 = F3.join(F3_35.set_index('ID'), on='ID')
#print(F3)


"""
下面分析1～9每个动作对最后一次动作时间距离最后一个动作的时间间隔
首先计算出最后一个动作的时间，然后分别计算出每个动作的的最后一次的动作时间，再将两者相减，就可以得到想要的特征。
同样也要对空值进行填补，填补值为空值所在特征对最大值
"""
#根据actionTime降序，再根据userid分组，获取第一条数据（计算出最后一个动作的时间）
lastTime = userAction.sort_values('actionTime', ascending=False).groupby('userid', as_index=False).head(1)
#读取userid和actionTime两列
lastTime = lastTime[['userid', 'actionTime']]
lastTime.columns = ['userid', 'lastTime']#重命名列名
#根据actionTime降序，再根据userid和actionType分组，获取第一条数据（计算出每个动作的的最后一次的动作时间）
lastActionTime = userAction.sort_values('actionTime', ascending=False).groupby(['userid', 'actionType'], as_index=False).head(1)
lastActionTime.columns = ['userid', 'actionType', 'lastActionTime']  #重命名列名
actionType = lastActionTime
lastActionTime = lastActionTime.join(lastTime.set_index('userid'), on='userid') #合并两张表，指定userid
#计算每一个动作的最后一次动作时间与最后一次动作时间的差值
lastActionTime['diff'] = lastActionTime['lastTime'] - lastActionTime['lastActionTime']
#读取actionType和diff两列，再根据actionType分组，求最大值
lastActionTimemax = lastActionTime[['actionType', 'diff']].groupby('actionType').max()

# F3.36 时间间隔_最近动作1
# F3.37 时间间隔_最近动作2
# F3.38 时间间隔_最近动作3
# F3.39 时间间隔_最近动作4
# F3.40 时间间隔_最近动作5
# F3.41 时间间隔_最近动作6
# F3.42 时间间隔_最近动作7
# F3.43 时间间隔_最近动作8
# F3.44 时间间隔_最近动作9
a3 = 36
for i in range(1, 10):
    #列名
    title3 = 'F3.' + str(a3)
    #读取每一个动作的数据
    action3 = lastActionTime[lastActionTime.actionType == i]
    #读取userid和diff两列
    action3 = action3[['userid', 'diff']]
    #重命名列名
    action3.columns = ['ID', title3]
    #合并特征
    F3 = F3.join(action3.set_index('ID'), on='ID')
    a3 = a3 + 1
    # 对空值进行填补，填补值为该特征最大值
    action3null = F3[['ID', title3]]
    action3null = action3null.set_index('ID').isnull()
    action3null = action3null[action3null[title3] == True]
    for id in action3null.index.values:
        max = lastActionTimemax.at[i, "diff"]
        F3.loc[F3['ID'] == id, title3] = max
#print(F3)

"""通过上面知道了1～9每个动作对最后一次动作的时间，因此，只需要知道客户操作时间大于每个动作对最后一次动作时间的资料笔数，
就是动作距离，空值填补为每个特征最大值"""

# F3.45 动作距离_最近动作1
# F3.46 动作距离_最近动作2
# F3.47 动作距离_最近动作3
# F3.48 动作距离_最近动作4
# F3.49 动作距离_最近动作5
# F3.50 动作距离_最近动作6
# F3.51 动作距离_最近动作7
# F3.52 动作距离_最近动作8
# F3.53 动作距离_最近动作9
a4 = 45
for i in range(1, 10):
    title4 = 'F3.' + str(a4)
    #获取每个动作的数据
    Type = actionType[actionType.actionType == i]
    #读取userid和lastActionTime两列
    Type = Type[['userid', 'lastActionTime']]
    #根据userid合并userAction和Type两张表
    action4 = userAction.join(Type.set_index('userid'), on='userid')
    #获取actionTime大于等于lastActionTime的数据
    action4 = action4[action4.actionTime >= action4.lastActionTime]
    #根据userid分组，求每个用户actionTime大于等于lastActionTime的数据计数
    action4 = action4.groupby('userid', as_index=False).count()
    #读取userid和'actionType两列数据
    action4 = action4[['userid', 'actionType']]
    #根据actionType降序，获取第一条数据
    action4max = action4.sort_values('actionType', ascending=False).head(1)
    #重命名列名
    action4.columns = ['ID', title4]
    #合并特征
    F3 = F3.join(action4.set_index('ID'), on='ID')
    a4 = a4 + 1
    #获取该特征最大值
    max = action4max.get('actionType').values[0] #values() 方法，这个方法把dict转换成一个包含所有value的list，因前面按actionType降序，再values[0]即取第一个也就是最大值
    # 对空值进行填补，填补值为该特征最大值
    action4null = F3[['ID', title4]]
    action4null = action4null.set_index('ID').isnull()
    action4null = action4null[action4null[title4] == True]
    for id in action4null.index.values:
        F3.loc[F3['ID'] == id, title4] = max

#print(F3)
"""计算动作1～9时间间隔对均值、方差、最小值、最大值。首先筛选出相同动作的操作，然后按照userid进行分组，分别计算时间间隔，
之后筛选出大于0的时间间隔。最后分别以userid分组计算不同动作是按间隔的均值、方差、最小值、最大值"""

# 3-54 时间间隔_动作1_均值
# 3-55 时间间隔_动作1_方差
# 3-56 时间间隔_动作1_最小值
# 3-57 时间间隔_动作1_最大值
# 3-58 时间间隔_动作2_均值
# 3-59 时间间隔_动作2_方差
# 3-60 时间间隔_动作2_最小值
# 3-61 时间间隔_动作2_最大值
# 3-62 时间间隔_动作3_均值
# 3-63 时间间隔_动作3_方差
# 3-64 时间间隔_动作3_最小值
# 3-65 时间间隔_动作3_最大值
# 3-66 时间间隔_动作4_均值
# 3-67 时间间隔_动作4_方差
# 3-68 时间间隔_动作4_最小值
# 3-69 时间间隔_动作4_最大值
# 3-70 时间间隔_动作5_均值
# 3-71 时间间隔_动作5_方差
# 3-72 时间间隔_动作5_最小值
# 3-73 时间间隔_动作5_最大值
# 3-74 时间间隔_动作6_均值
# 3-75 时间间隔_动作6_方差
# 3-76 时间间隔_动作6_最小值
# 3-77 时间间隔_动作6_最大值
# 3-78 时间间隔_动作7_均值
# 3-79 时间间隔_动作7_方差
# 3-80 时间间隔_动作7_最小值
# 3-81 时间间隔_动作7_最大值
# 3-82 时间间隔_动作8_均值
# 3-83 时间间隔_动作8_方差
# 3-84 时间间隔_动作8_最小值
# 3-85 时间间隔_动作8_最大值
# 3-86 时间间隔_动作9_均值
# 3-87 时间间隔_动作9_方差
# 3-88 时间间隔_动作9_最小值
# 3-89 时间间隔_动作9_最大值

#读取userid、'actionType、actionTime三列
timeinterval2 = userAction[['userid', 'actionType', 'actionTime']]
#根据'userid', 'actionType'分组，获取actionTime列每一行值与上一行的差值，并赋值到新列interval
timeinterval2['interval'] = timeinterval2.groupby(['userid', 'actionType']).actionTime.diff()
a5 = 54
for i in range(1, 10):
    #列名
    actionMeanTitle = 'F3.' + str(a5)
    actionVarTitle = 'F3.' + str(a5 + 1)
    actionMinTitle = 'F3.' + str(a5 + 2)
    actionMaxTitle = 'F3.' + str(a5 + 3)
    #读取每个动作的数据
    actionType = timeinterval2[timeinterval2.actionType == i]
    #读取'userid', 'interval'两列
    actionType = actionType[['userid', 'interval']]
    #根据userid分组，求均值
    actionMean = actionType.groupby('userid', as_index=False).mean()
    #重命名列
    actionMean.columns = ['ID', actionMeanTitle]
    # 根据userid分组，求方差
    actionVar = actionType.groupby('userid', as_index=False).var()
    actionVar.columns = ['ID', actionVarTitle]
    #根据userid分组，求最小值
    actionMin = actionType.groupby('userid', as_index=False).min()
    actionMin.columns = ['ID', actionMinTitle]
    # 根据userid分组，求最大值
    actionMax = actionType.groupby('userid', as_index=False).max()
    actionMax.columns = ['ID', actionMaxTitle]
    #合并特征
    F3 = F3.join(actionMean.set_index('ID'), on='ID')
    F3 = F3.join(actionVar.set_index('ID'), on='ID')
    F3 = F3.join(actionMin.set_index('ID'), on='ID')
    F3 = F3.join(actionMax.set_index('ID'), on='ID')
    a5 = a5 + 4

#将NA替换空值
F3 = F3.fillna('NA')
F3.to_csv('workeddata/F3.csv', index=False, encoding="utf_8_sig")
#print(F3)

