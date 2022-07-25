"""算法原理
协同过滤简单来说是利用兴趣相投、拥有共同经验、相似喜好来推荐用户感兴趣的信息，个人通过合作的机制给予信息相当程度的回应(如评分)并记录下来
以达到过滤的目的，进而帮助别人筛选信息，回应不一定局限于特别感兴趣的，特别不感兴趣的信息的记录也相当重要。
其中分两种过滤，一种为以用户为基础(user-based)的协同过滤， 一种为以项目为基础(item-based)的协同过滤
"""

"""业务背景
业务需求：给消费者推荐商品，提高转化率
"""

import pandas as pd

"""数据准备"""
#导入数据
orders = pd.read_csv('data/orders.csv')
items = pd.read_csv('Items_order.csv')
itemProps = pd.read_csv('Items_attribute.csv', encoding='gb2312')

#合并orders和items
orders_items = pd.merge(orders, items, on="订单编号")
#合并orders_items和itemProps
orders_items_props = pd.merge(orders_items, itemProps, on="标题")
#提取买家会员名和宝贝ID字段
result = orders_items_props[["买家会员名", "宝贝ID"]]
#创建购买次数字段，并初始值为0
result["购买次数"] = 0
#分组计数，并重置索引
freq = result.groupby(["买家会员名", "宝贝ID"]).count().reset_index()
#创建数据透视表
freq = freq.pivot(index="买家会员名", columns="宝贝ID", values="购买次数")
#缺失值用数字0填充
freqMatrix = freq.fillna(0).values

"""推荐算法建模"""

import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

def predict(similar, base='item'):
    user_cnt = freqMatrix.shape[0]
    item_cnt = freqMatrix.shape[1]
    pred = np.zeros((user_cnt, item_cnt))
    for uid in range(user_cnt):
        for iid in range(item_cnt):
            if freqMatrix[uid, iid] == 0:
                print(uid, iid)
                pred[uid, iid] = Recommendation_s(uid, iid, similar, base=base)
    return pred
#Recommendation_s()是在上下文的预测函数predict()中调用的函数，用于对商品和用户进行评分
def Recommendation_s(uid, iid, similar, k=10, base='item'):
    score = 0
    weight = 0
    uid_action = freqMatrix[uid, :]  #用户uid对所有商品对行为评分
    iid_action = freqMatrix[:, iid]  #商品iid得到对所有用户评分

    if base == 'item':
        iid_sim = similar[iid, :]  #商品iid对所有商品对相似度
        sim_indexs = np.argsort(iid_sim)[-(k+1):-1]  #最相似对k个商品对index(除了自己)  np.argsort(a)返回的是元素值从小到大排序后的索引值的数组
        iid_i_mean = np.sum(iid_action)/iid_action[iid_action != 0].size  #size()函数主要是用来统计矩阵元素个数，或矩阵某一维上的元素个数的函数 可选参数axis
        for j in sim_indexs:
            if uid_action[j] != 0:
                iid_j_action = freqMatrix[:, j]
                iid_j_mean = np.sum(iid_j_action) / iid_j_action[iid_j_action != 0].size
                score += iid_sim[j] * (uid_action[j] - iid_j_mean)
                weight += abs(iid_sim[j])

        if weight == 0:
            return 0
        else:
            return iid_i_mean + score / float(weight)
    else:
        uid_sim = similar[uid, :]  # 用户uid 对所有用户的相似度
        sim_indexs = np.argsort(uid_sim)[-(k + 1):-1]  # 最相似的k个用户的index（除了自己）
        uid_i_mean = np.sum(uid_action) / uid_action[uid_action != 0].size
        for j in sim_indexs:
            if iid_action[j] != 0:
                uid_j_action = freqMatrix[j, :]
                uid_j_mean = np.sum(uid_j_action) / uid_j_action[uid_j_action != 0].size
                score += uid_sim[j] * (iid_action[j] - uid_j_mean)
                weight += abs(uid_sim[j])

        if weight == 0:
            return 0
        else:
            return uid_i_mean + score / float(weight)

#自定义get_top10()函数用于分组排序
def get_top10(group):
    return group.sort_values("推荐指数", ascending=False)[:10]

#自定义get_recom()函数用于整理数据，输出表格形态的数据
def get_recom(prediction):
    recom_df = pd.DataFrame(prediction, columns=freq.columns, index=freq.index)
    recom_df = recom_df.stack().reset_index()
    recom_df.rename(columns={0: "推荐指数"}, inplace=True)

    grouped = recom_df.groupby("买家会员名")
    top10 = grouped.apply(get_top10)

    top10 = top10.drop(["买家会员名"], axis=1)
    top10.index = top10.index.droplevel(1)
    top10.reset_index(inplace=True)
    return top10

#使用pairwise_distances()函数创建基于用户的距离矩阵
user_similar = 1 - pairwise_distances(freqMatrix, metric="cosine")
#print(user_similar)
#使用pairwise_distances函数创建基于项目的距离矩阵
item_similar = 1 - pairwise_distances(freqMatrix.T, metric="cosine")
#print(item_similar)

#分别使用基于用户和项目的协同过滤模型进行预测
user_prediction = predict(user_similar, base="user")
item_prediction = predict(item_similar, base="item")

user_recom = get_recom(user_prediction)
item_recom = get_recom(item_prediction)
print(user_recom.head())  #用户协同过滤
print(item_recom.head())  #项目协同过滤

#输出文件(包括对每个用户退浆对商品及推荐度)
user_recom.to_csv("recom_top10_UBCF.csv", index=False, encoding="utf-8")
item_recom.to_csv("recom_top10_IBCF.csv", index=False, encoding="utf-8")



