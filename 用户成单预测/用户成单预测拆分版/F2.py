import pandas as pd
import math

#3用户订单资料分析处理
userOrder = pd.read_csv('rawdata/table_2.csv')
"""提取以下特征：F2.1:订单的数量  F2.2:是否为精品订单 F2.3精品订单的数量 F2.4精品订单的占比"""

#读取订单类型为1对数据，把订单类型为1对订单定义为精品订单 orderType为订单类型
JPorder = userOrder[userOrder.orderType == 1]
# F2.1:订单的数量， userid为用户ID，orderid为订单id
orderNum = userOrder[['userid', 'orderid']]
F2 = orderNum.groupby('userid', as_index=False).count()  #as_index=False时,表示为默认自然数字索引，不将主键设置为索引
#将F2表的字段重命名
F2.columns = ['ID', 'F2.1']

# F2.3 精品订单_个数 ,
orderType = JPorder[['userid']]  #读取精品订单用户ID
orderType['number'] = 1  #新建number列，列初始值为1
orderType = orderType.groupby('userid', as_index=False).sum() #根据用户ID分组求精品订单数
#根据用户id合并orderType和F2两张表
orderType = orderType.join(F2.set_index('ID'), on='userid')
# F2.4 精品订单_占比
orderType['F2.4'] = orderType['number']/orderType['F2.1']
# F2.2 精品订单_是否有,1表示精品订单，0表示没有精品订单
orderType['F2.2'] = 1
F2_2_3_4 = orderType[['userid', 'F2.2', 'number', 'F2.4']]
F2_2_3_4.columns = ['ID', 'F2.2', 'F2.3', 'F2.4'] #重命名列名
#把F2表和F2_2_3_4表合并
F2 = F2.join(F2_2_3_4.set_index('ID'), on='ID')
#print(F2)

#从userOder表清洗出以下新增字段
#F2.5:旅游最多城市次数
#F2.6:旅游城市数
#F2.7:旅游最多国家次数
#F2.8:旅游国家数
#F2.9:旅游最多大洲次数
#F2.10:旅游大洲数
#创建分组，分别为城市(city)、国家(country)、和大洲(continent）
site = ['city', 'country', 'continent']
a = 5
for i in range(0, 3):
    #设定列名
    title1 = 'F2.' + str(a)
    title2 = 'F2.' + str(a+1)
    #读取读取全部订单的userid,city,country,continent字段到siteinfo表
    siteinfo = userOrder[['userid', site[i]]]
    #新建number列，列值为1
    siteinfo['number'] = 1
    #根据userid和city,country,continent分组，求每个用户去过每个城市/国家/大洲的次数汇总求和
    siteinfo = siteinfo.groupby(['userid', site[i]], as_index=False).sum()
    #根据userid分组，求用户去过最多城市/国家/大洲的次数
    siteinfo1 = siteinfo.groupby('userid', as_index=False).max()
    siteinfo1 = siteinfo1[['userid', 'number']]
    #重命名列名
    siteinfo1.columns = ['ID', title1]
    #根据userid分组，求用户去过城市/国家/大洲的次数的计数
    siteinfo2 = siteinfo.groupby('userid', as_index=False).count()
    siteinfo2 = siteinfo2[['userid', site[i]]]
    #重命名列名
    siteinfo2.columns = ['ID', title2]
    #根据ID合并特征
    F2 = F2.join(siteinfo1.set_index('ID'), on='ID')
    F2 = F2.join(siteinfo2.set_index('ID'), on='ID')
    a = a + 2

#print(F2)

#从JPorder表清洗出以下新增字段
#F2.11:精品旅游最多城市次数
#F2.12:精品旅游城市数
#F2.13:精品旅游最多国家次数
#F2.14:精品旅游国家数
#F2.15:精品旅游最多大洲次数
#F2.16:精品旅游大洲数

a = 11
for i in range(0, 3):
    # 设定列名
    title1 = 'F2.' + str(a)
    title2 = 'F2.' + str(a + 1)
    # 读取userid,city,country,continent字段到siteinfo表
    JPsiteinfo = JPorder[['userid', site[i]]]
    # 新建number列，列值为1
    JPsiteinfo['number'] = 1
    # 根据userid和city,country,continent分组，求每个用户去过每个城市/国家/大洲的次数汇总求和
    JPsiteinfo = JPsiteinfo.groupby(['userid', site[i]], as_index=False).sum()
    # 根据userid分组，求用户去过最多城市/国家/大洲的次数
    JPsiteinfo1 = JPsiteinfo.groupby('userid', as_index=False).max()
    JPsiteinfo1 = JPsiteinfo1[['userid', 'number']]
    # 重命名列名
    JPsiteinfo1.columns = ['ID', title1]
    # 根据userid分组，求用户去过城市/国家/大洲的次数的计数
    JPsiteinfo2 = JPsiteinfo.groupby('userid', as_index=False).count()
    JPsiteinfo2 = JPsiteinfo2[['userid', site[i]]]
    # 重命名列名
    JPsiteinfo2.columns = ['ID', title2]
    # 根据ID合并特征
    F2 = F2.join(JPsiteinfo1.set_index('ID'), on='ID')
    F2 = F2.join(JPsiteinfo2.set_index('ID'), on='ID')
    a = a + 2

#print(F2)

#清洗出订单的时间间隔，并命名为F2.17   orderTime为订单时间
period = userOrder.orderTime.max() - userOrder.orderTime.min()
F2['F2.17'] = period/F2['F2.1']    #订单的平均时间间隔

#清洗出精品订单的时间间隔，并命名为F2.18
JPperiod = JPorder.orderTime.max() - JPorder.orderTime.min()
F2['F2.18'] = JPperiod/F2['F2.3']  #精品订单的平均时间间隔
#print(F2)

#从userOder表清洗出以下新增字段
# F2.19 订单_热门城市_是否访问
# F2.20 订单_热门城市_访问城市数
# F2.21 订单_热门城市_访问次数
# F2.22 订单_热门国家_是否访问
# F2.23 订单_热门国家_访问国家数
# F2.24 订单_热门国家_访问次数
# F2.25 订单_热门大洲_是否访问
# F2.26 订单_热门大洲_访问大洲数
# F2.27 订单_热门大洲_访问次数

a = 19
for i in range(0, 3):
    title1 = 'F2.' + str(a)
    title2 = 'F2.' + str(a + 1)
    title3 = 'F2.' + str(a + 2)
    # 读取全部订单的userid,city,country,continent字段到siteinfo表
    siteinfo = userOrder[['userid', site[i]]]
    #根据city/country/continent分组，求城市/国家/大洲的订单数(计数)
    topsite = siteinfo.groupby(site[i], as_index=False).count()
    #获取前20%的热门城市/国家/大洲的信息
    topsite = topsite.sort_values('userid', ascending=False).head(math.floor((len(topsite) * 0.2)))
    #math.floor()方法是数学模块的库方法，用于获取给定数字的下限值，用于获取数字的下限值，它接受数字/数值表达式并返回最大整数(整数)值，该值不大于数字。
    #获取热门城市/国家/大洲
    topsite = topsite[[site[i]]]
    #获取去过热门城市/国家/大洲全部订单信息
    topsiteOrder = topsite.join(siteinfo.set_index(site[i]), on=site[i])
    #新建number列，列值为1
    topsiteOrder['number'] = 1
    #根据userid和city,country,continent分组，求每个用户去过的每个城市/国家/大洲的次数(汇总求和)
    topsiteOrder1 = topsiteOrder.groupby(['userid', site[i]], as_index=False).sum()
    # 根据userid分组，求每个用户去过的热门城市/国家/大洲数(计数)
    topsiteOrder1 = topsiteOrder1.groupby('userid', as_index=False).count()
    topsiteOrder1 = topsiteOrder1[['userid', site[i]]]
    #重命名列名
    topsiteOrder1.columns = ['ID', title2]
    #新建列是否访问过热门城市/国家/大洲，1为访问过，0为没有访问过
    topsiteOrder1[title1] = 1
    #根据userid分组，求每个用户去过的热门城市/国家/大洲的次数(汇总求和)
    topsiteOrder2 = topsiteOrder.groupby('userid', as_index=False).sum()
    #重命名列名
    topsiteOrder2.columns = ['ID', title3]
    #根据ID合并特征
    F2 = F2.join(topsiteOrder1.set_index('ID'), on='ID')
    F2 = F2.join(topsiteOrder2.set_index('ID'), on='ID')
    a = a + 3

#print(F2)


#从JPoder表清洗出以下新增字段
# F2.28 精品订单_热门城市_是否访问
# F2.29 精品订单_热门城市_访问城市数
# F2.30 精品订单_热门城市_访问次数
# F2.31 精品订单_热门国家_是否访问
# F2.32 精品订单_热门国家_访问国家数
# F2.33 精品订单_热门国家_访问次数
# F2.34 精品订单_热门大洲_是否访问
# F2.35 精品订单_热门大洲_访问大洲数
# F2.36 精品订单_热门大洲_访问次数

a = 28
for i in range(0, 3):
    title1 = 'F2.' + str(a)
    title2 = 'F2.' + str(a + 1)
    title3 = 'F2.' + str(a + 2)
    # 读取全部订单的userid,city,country,continent字段到siteinfo表
    JPsiteinfo = JPorder[['userid', site[i]]]
    #根据city/country/continent分组，求城市/国家/大洲的订单数(计数)
    JPtopsite = JPsiteinfo.groupby(site[i], as_index=False).count()
    #获取前20%的热门城市/国家/大洲的信息
    JPtopsite = JPtopsite.sort_values('userid', ascending=False).head(math.floor((len(JPtopsite) * 0.2)))
    #math.floor()方法是数学模块的库方法，用于获取给定数字的下限值，用于获取数字的下限值，它接受数字/数值表达式并返回最大整数(整数)值，该值不大于数字。
    #获取热门城市/国家/大洲
    JPtopsite = JPtopsite[[site[i]]]
    #获取去过热门城市/国家/大洲全部订单信息
    JPtopsiteOrder = JPtopsite.join(JPsiteinfo.set_index(site[i]), on=site[i])
    #新建number列，列值为1
    JPtopsiteOrder['number'] = 1
    #根据userid和city,country,continent分组，求每个用户去过的每个城市/国家/大洲的次数(汇总求和)
    JPtopsiteOrder1 = JPtopsiteOrder.groupby(['userid', site[i]], as_index=False).sum()
    # 根据userid分组，求每个用户去过的热门城市/国家/大洲数(计数)
    JPtopsiteOrder1 = JPtopsiteOrder1.groupby('userid', as_index=False).count()
    JPtopsiteOrder1 = JPtopsiteOrder1[['userid', site[i]]]
    #重命名列名
    JPtopsiteOrder1.columns = ['ID', title2]
    #新建列是否访问过热门城市/国家/大洲，1为访问过，0为没有访问过
    JPtopsiteOrder1[title1] = 1
    #根据userid分组，求每个用户去过的热门城市/国家/大洲的次数(汇总求和)
    JPtopsiteOrder2 = JPtopsiteOrder.groupby('userid', as_index=False).sum()
    #重命名列名
    JPtopsiteOrder2.columns = ['ID', title3]
    #根据ID合并特征
    F2 = F2.join(JPtopsiteOrder1.set_index('ID'), on='ID')
    F2 = F2.join(JPtopsiteOrder2.set_index('ID'), on='ID')
    a = a + 3

#print(F2)
#将全部空值替换为0
F2 = F2.fillna(0)
F2 = F2[['ID', 'F2.1', 'F2.2', 'F2.3', 'F2.4', 'F2.5', 'F2.6', 'F2.7', 'F2.8', 'F2.9', 'F2.10',
    'F2.11', 'F2.12', 'F2.13', 'F2.14', 'F2.15', 'F2.16', 'F2.17', 'F2.18', 'F2.19', 'F2.20',
    'F2.21', 'F2.22', 'F2.23', 'F2.24', 'F2.25', 'F2.26', 'F2.27', 'F2.28', 'F2.29', 'F2.30',
    'F2.31', 'F2.32', 'F2.33', 'F2.34', 'F2.35', 'F2.36']]
#取出F2表中所需的特征字段，并写入文件中
F2.to_csv('workeddata/F2.csv', index=False, encoding="utf_8_sig")
#print(F2)
