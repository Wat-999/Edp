"""
将消费者在线上留下的文字(聊天记录、评论等)进行统计分析和建模，了解消费者对品牌、商品对看法，以及消费者在需求和情感上对厌恶，
可以对品牌、商品对战略定位起到非常重要对作用，让运营者可以做出正确对决策
项目背景
某品牌方要进行品牌对升级改造，而且改造对任务十分紧急，要赶在行业会议之前推出新对概念商品，因此品牌方想通过消费者调研，掌握消费者对该品牌对态度，从而找出正确对改造方向
数据说明
评价：来自某电商平台对消费者对该品牌商品对评论
词根：根据评价切分出来对最小词语单位
词频：指某个词根出现对次数
实现思路
1通过情感分析提取情感得分，区分正面评价和负面评价
2分别分析正面评价和负面评价对词云
3通过词云掌握消费者对品牌对态度
"""
import pandas as pd
from jieba import posseg
from wordcloud import WordCloud
from snownlp import SnowNLP
from collections import Counter
import matplotlib.pyplot as plt

#1删除评论数据中此用户没有填写评价的数据
df = pd.read_excel('产品评价数据.xlsx')
data = df['评价']
data = df['评价'][-df.评价.isin(['此用户没有填写评论'])]  #isin()查看某列中是否包含某个字符串
print(data)
#2对评论数据进行情感分析，并根据情感得分，区别正面评价和负面评价,合并文本
good = ''
bad = ''
for i in data:
    s = SnowNLP(str(i))
    text = s.sentiments
    print(i, text)
    if text >= 0.5:  #根据得分区分正面评价和负面评价
        good += str(i)  #筛选出正面评价并合并
    else:
        bad += str(i) #筛选出负面评价并合并
print('正面评价：', good)
print('负面评价：', bad)

#3将正面评价和负面评价进行分词-筛选-计数
goodwords = [w for w, f in posseg.cut(good) if f[0] != 'r' and len(w) > 1 and f[0] != 'a' and f[0] != 'd']
badwords = [w for w, f in posseg.cut(good) if f[0] != 'r' and len(w) > 1 and f[0] != 'a' and f[0] != 'd']
#上面是根据Jieba分词词性进行筛选，例如r表示代词， a表示形容词， d表示副词
c1 = Counter(goodwords)
c2 = Counter(badwords)
print(c1)
print(c2)

#4绘制词云图
w1 = WordCloud(font_path='/System/Library/fonts/PingFang.ttc',
               background_color='white',
               width=900, height=600,
               max_font_size=200,
               min_font_size=3,
               random_state=50)
w2 = WordCloud(font_path='/System/Library/fonts/PingFang.ttc',
               background_color='white',
               width=900, height=600,
               max_font_size=200,
               min_font_size=3,
               random_state=50)
p1 = w1.generate_from_frequencies(dict(c1))  #给定词频画词云图并且是dict形式
p2 = w2.generate_from_frequencies(dict(c2))
plt.imshow(p1)  #使用imshow()函数可以非常容易地制作热力图。
plt.axis('off')  #关闭坐标轴
plt.show()
plt.imshow(p2)
plt.axis('off')
plt.show()
