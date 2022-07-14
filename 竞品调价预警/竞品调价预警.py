import pandas as pd
import datetime


skuAllData = pd.read_excel('单品SKU价格.xlsx')
sku = skuAllData[['日期', '商家昵称', '商品ID', 'SKU ID', 'SKU名称', 'SKU价格']]
#根据商品ID对数据进行分组，如果有某一天有重复对数据，取当天价格对最大值
df = sku.groupby('商品ID').max()

#使用for循环对比价格
for i in df['日期']:
    df2 = sku[sku['日期'] == i]  #取出当前日期的数据放入df2
    df3 = sku[sku['日期'] == (i - datetime.timedelta(days=1))]  #取出当前日期的前一天对数据放入df3
    for id in df2['SKU ID']:
        df22 = df2[df2['SKU ID'] == id] #从df2中取出当前sku id放入df22
        df33 = df3[df3['SKU ID'] == id] #从df3中取出当前sku id放入df33
        #分别读取前2天的价格
        money1 = int(df22.get('SKU价格'))
        money2 = int(df33.get('SKU价格'))
        #计算价格的变化幅度
        bl = (money1-money2)/money2
        #设置提醒条件为增长或下降10%
        if bl >= 0.1 or bl <= -0.1:
            print('当前SKU价格较昨天波动大于10%')
            for i in df22.iterrows():
                print(i[1])
            print('===================================================')
            print('===================================================')


