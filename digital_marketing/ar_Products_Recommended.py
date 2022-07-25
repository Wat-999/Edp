"""————————————————实现思路————————————————————————
1关联规则需要先创建商品项集，商品项集类似超市购物后得到的小票，每一条项集就是一张小票的商品的列表
2计算频繁项集
3编写关联规则算法，挖掘关联规则
————————————————————————————————————————————————————
"""
import pandas as pd
import numpy as np

orders = pd.read_csv('data/orders.csv')

#由于部分列标题中存在空格，因此需要先清洗掉
column = []
for i in range(orders.shape[1]):
    column.append(orders.columns[i].strip())
orders.columns = column
orders['宝贝标题'] = orders['宝贝标题'].apply(lambda x: x.replace(' ', ''))
dataSet = list(orders['宝贝标题'].apply(lambda x: x. split('，'))) #注意输入为字符串"，"

#遍历数据集中的每件商品，创建一项集
def createC1(dataSet):
    C1 = []
    #遍历每条记录
    for transaction in dataSet:
        for item in transaction:
            #判断如果该商品没在列表中
            if not [item] in C1:
                #将该商品加入列表中
                C1.append([item])
    #对所有商品排序
    C1.sort() #默认升序
    return list(map(frozenset, C1)) 
C1 = createC1(dataSet)

#建立函数挑选最小支持度项集
#下面建立函数scanD()，用于挑选满足最小支持度的项集，输入为：数据集D，候选集Ck，minSupport。候选集Ck是由上一层(第k-1层)的频繁项集Lk-1组合得到的
#用最小支持度minSupport对候选集Ck过滤
#函数输出：本层(第k层）的频繁项集Lk，每项的支持度。例如，由频项1-项集（L1)内部组合生成候选集C2。

def scanD(D, Ck, minSupport):
    #建立字典{key, value}
    #候选集Ck中每项集在所有商品记录中出现的次数
    #key-候选集中的每项
    #value-该商品在所有物品记录中出现的次数
    ssCnt = {} #空字典用来计数
    #对比候选集中的每项与原商品记录，统计出现的次数

    #遍历每条商品记录
    for tid in D:
        #遍历候选集Ck中的每一项，用于对比
        for can in Ck:
            #如果候选集Ck中该项在商品记录中出项
            #即当前项是当前商品记录的子集
            if can.issubset(tid):  #issubset() 方法用于判断集合的所有元素是否都包含在指定集合中,即判断集合A是否为集合B的子集
                #如果候选集Ck中第一次被统计到，次数记为1
                if not can in ssCnt:
                    ssCnt[can] = 1
                #否则次数在原有基础上加1
                else:
                    ssCnt[can] += 1
                    #ssCnt[can] = ssCnt.get(can, 0) + 1

    #数据集中总的记录数，商品购买记录总数，用于计算支持度
    numltems = float(len(D))
    #记录经最小支持度过滤后的频繁项集
    retList = []
    #记录候选集中满足条件的项的支持度{key, value}
    #key-候选集中满足条件的项
    #value-该项的支持度
    supportData = {}
    #遍历候选集中的每项出现次数
    for key in ssCnt:
        #计算每项的支持度
        support = ssCnt[key]/numltems
        #用最小支持度过滤
        if support >= minSupport:
            #保留满足条件的商品组合
            #使用retList.insert(0,key)
            #在列表的首部插入新的组合
            #只是为列让列表看起来有组织
            retList.insert(0, key)  #insert()函数中第一个参数表示的是index即被插的起始位置，第二个参数为被插的对象。0表示从头部插入

        #记录该项的支持度
        #注意：候选集中所有项的支持度均被保持下来
        #不仅仅是满足最小支持度的项
        supportData[key] = support
    #返回满足条件的商品项，以及每项的支持度
    return retList, supportData
#创建一个商品项集D
D = list(map(set, dataSet))
#print(D[0:2])

#调用自定义的scanD()函数
L1, supportData = scanD(D, C1, minSupport=0.05)
#print(L1[:5])
#print(supportData)


# 项集迭代函数
def aprioriGen(Lk):
    retList = []
    lenLk = len(Lk)
    k = len(Lk[0])
    for i in range(lenLk): #遍历频繁一项集
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-1]; L2 = list(Lk[j])[:k-1]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j]) #|表示或
    return retList
#调用项集迭代函数
#print(aprioriGen(L1))

# 使用Apriori频繁项挖掘关联规则。
def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet) #生成备选一项集
    D = list(map(set, dataSet)) #更改原数据为list
    L1, supportData = scanD(D, C1, minSupport)
    #L1是频繁一项集，supportData是所有一项集的支持度
    L = [L1] #将一项集放入list中
    while (len(L[-1]) > 1):
        Ck = aprioriGen(L[-1])
        Lk, supK = scanD(D, Ck, minSupport)#得到频繁K项集
        supportData.update(supK)#所有项集的支持度
        L.append(Lk) #L是所有项集组成的list
    return L, supportData

# 调用自定义的apriori函数
L, supportData= apriori(dataSet, minSupport = 0.01)

# 频繁二项集的置信度计算函数
def calcConf(freqSet, H, supportData, brl, minConf=0.5): #calcConf()函数对规则进行评估;最小可信度阈值minConf
    #H是freqSet的所有子集
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq) #把后键单独存储，为了后面有可能用到后键的超项集
    return prunedH

# 频多项集的置信度计算函数
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7): #rulesFromConseq()函数用于生成候选规则集合
    Hmp = True
    while Hmp:
        Hmp = False #防止Hmp失效导致进入无限循环
        H = calcConf(freqSet, H, supportData, brl, minConf)
        H = aprioriGen(H)
        Hmp = not(H == [] or len(H[0]) == len(freqSet))

# Apriori关联规则挖掘函数
def generateRules(L, supportData, minConf=0.7): #为主函数，最小可信度阈值minConf
    bigRuleList = []
    for i in range(1, len(L)): #从频繁二项集开始挖掘规则
        for freqSet in L[i]: #找出每个频繁项集的子集
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

brl = generateRules(L, supportData, minConf=0.05)
print(brl)
# 将结果转变成表格。
col = ['宝贝1', '宝贝2', '置信度']
data = pd.DataFrame(columns=col, data=brl)
print(data)

# 对置信度进行降序，可以找到置信度高的规则，建议根据运营人员使用这些规则。
print(data.sort_values(by="置信度", ascending=False))


