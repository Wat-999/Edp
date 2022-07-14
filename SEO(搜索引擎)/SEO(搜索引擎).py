"""
SEO(搜索引擎优化)是利用搜索引擎的规则提高网站在有关搜索引擎内的自然排名。目的是让其在行业内占据领先地位，获得品牌收益。
很大程度上是网站经营者的一种商业行为，将自己或自己公司的排名前移。
在做SEO的过程中会产生关键词效果分析，相关指标字段有访客数，成交金额、交易客户数，应用python可以实现关键词的效果分析，为搜索优化提供数据支撑
SEO中有词根的概念，词根是最小的标题粒度，根据自己的标题确定词根，比如中文关键词"修身 连衣裙"可以分为修身和连衣裙两个词根，最小粒度的概念就是不能再拆分
如中文词根'连衣裙'，不可以再分为"连衣""衣裙"在消费者搜索行为中不具备意义，因此连衣裙就是最小词根
业务需求：运营人员想确定可删除替换的词根，删除表现差的词根不会对整体数据带来太大的影响。如果运营人员把表现好的词根删掉了，对整体数据的影响就会非常大
分析目的：找出数据反馈差的词根
示例标题：儿童汉服女童中国风12岁夏季薄款超仙春秋齐胸襦长袖裙唐装复古装
标题拆解为词根：儿童,汉服,女童,中国风,12,岁,夏季,薄款,超仙,春秋,齐胸,襦,长袖,裙,唐装,复古装

实现思路
1设置词根列表；2用for循环判断关键词中是否包含某个词根；3统计词根的数据；4绘制柱状图
"""

import pandas as pd
import matplotlib.pyplot as plt

# 标题词根拆解
# 示例标题：儿童汉服女童中国风12岁夏季薄款超仙春秋齐胸襦长袖裙唐装复古装
# 标题拆解为词根：儿童,汉服,女童,中国风,12,岁,夏季,薄款,超仙,春秋,齐胸,襦,长袖,裙,唐装,复古装
word = ['儿童', '汉服', '女童', '中国风', '12', '岁', '夏季', '薄款', '超仙', '春秋', '齐胸', '襦', '长袖', '裙', '唐装', '复古装']
# 读取一个星期商品手淘关键词详情
stss = pd.read_excel('/U商品三级流量来源详情.xls')
# 读取需要的数据
data = stss[['来源名称', '访客数', '收藏人数', '加购人数', '支付买家数']]
# 创建一个空的表格
wordData = pd.DataFrame(columns=['词根', '访客数', '收藏人数', '加购人数', '支付买家数'])

#使用for循环判断关键词中是否包含词根
for i in word:
    data2 = data[data.来源名称.str.contains(i)]
    #contains函数就是检查数据中是否包含某种设定的字符(contains筛选的其实是正则表达式)
    #df['Discount_rate'].str.contains(':')  比如这个就是赛选df文件下Discount_rate标签是否包含‘：’这个符号 有的话返回Ttue 没有的话返回False

    data3 = data2[['访客数', '收藏人数', '加购人数', '支付买家数']]
    data3['词根'] = i
    wordData = wordData.append(data3, ignore_index=True)
    #ignore_index = True并不意味忽略index然后连接，而是指连接后再重新赋值index(len(index))

#根据词根分组汇总访客数、收藏人数、加购人数、和支付买家数
wordData2 = wordData.groupby('词根').sum()

#计算转化率 = 支付买家数/访客数
wordData2['转化率'] = wordData2['支付买家数']/wordData2['访客数']*100

#计算加购率 = 加购人数/访客数
wordData2['加购率'] = wordData2['加购人数']/wordData2['访客数']*100

#计算收藏率 = 收藏人数/访客数
wordData2['收藏率'] = wordData2['收藏人数']/wordData2['访客数']*100
print(wordData2['转化率'])

#可视化
#设置参数，以确保图形正确显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 将词根设置为x轴，访客数、转化率、加购率、收藏率设置为y轴
x = wordData2.index.values.tolist()
y1 = wordData2['访客数'].values.tolist()
y2 = wordData2['转化率'].values.tolist()
y3 = wordData2['加购率'].values.tolist()
y4 = wordData2['收藏率'].values.tolist()

# 设置画布大小
# 表示图片的大小为宽8inch、高6inch（单位为inch）
plt.figure(figsize=(8, 6))
# 绘制柱形图
plt.bar(x, y1)
# 设置标题以及x轴标题，y轴标题
plt.xlabel('词根')
plt.ylabel('访客数')
# 设置数字标签
for a, b in zip(x, y1):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
plt.show()

# 设置画布大小
# 表示图片的大小为宽8inch、高6inch（单位为inch）
plt.figure(figsize=(8, 6))
# 绘制柱形图
plt.bar(x, y2)
# 设置标题以及x轴标题，y轴标题
plt.xlabel('词根')
plt.ylabel('转化率')
# 设置数字标签
for a, b in zip(x, y2):
    plt.text(a, b, '%.2f%%' % b, ha='center', va='bottom', fontsize=8) #'%.2f%%'转化成百分比，2是表示保留2位小数点
plt.show()

# 设置画布大小
# 表示图片的大小为宽8inch、高6inch（单位为inch）
plt.figure(figsize=(8, 6))
# 绘制柱形图
plt.bar(x, y3)
# 设置标题以及x轴标题，y轴标题
plt.xlabel('词根')
plt.ylabel('加购率')
# 设置数字标签
for a, b in zip(x, y3):
    plt.text(a, b, '%.2f%%' % b, ha='center', va='bottom', fontsize=8)
plt.show()

# 设置画布大小
# 表示图片的大小为宽8inch、高6inch（单位为inch）
plt.figure(figsize=(8, 6))
# 绘制柱形图
plt.bar(x, y4)
# 设置标题以及x轴标题，y轴标题
plt.xlabel('词根')
plt.ylabel('收藏率')
# 设置数字标签
for a, b in zip(x, y4):
    plt.text(a, b, '%.2f%%' % b, ha='center', va='bottom', fontsize=8)
plt.show()

#我们首先先要看词根的访客数，这个是最主要的。如果有个别词根的流量特别低，就可以考虑把这个词根换掉。然后看词根的转化率，一些转化率特别低的词根，要看收藏和加购数
#，如果收藏和加购数也特别低，则可以考虑换一下。通过分析结果确认"薄款""唐装""春秋""齐胸"可以优先替换成其他词根，删除这些词根只会影响6个访客数
#等于几乎没影响，因此可以放心地替换这些词根。
