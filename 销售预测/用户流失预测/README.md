# [用户流失预测]()

## [一.算法原理]()
1. 流失用户是指那些曾经使用过产品或服务，由于对产品失去兴趣等种种原因，不再使用产品或服务;
1. 对用户根据流失用户所处对用户关系生命周期阶段可以将流失用户分为4类，即考察阶段流失用户、形成阶段流失用户、稳定阶段流失用户和衰退阶段流失用户;
1. 根据用户流失对原因也可以将流失用户分为4类:第1类流失用户是自然消亡类、第2类流失用户是需求变化类、第3类流失用户是趋利流失类、第4类流失用户是失望流失类;
1. 根据以上用户流失的原因，我们在原始的51个特征种重新提取分析出50个新的特征，再利用线性回归进行分析，求得回归系数，最后根据这个系数进行判断。

## [二.项目背景]()
- 在海量的网站访问量中，可分析用户的行为数据来挖掘潜在的信息资源。
其中，客户流失率是考虑业务成绩的一个非常关键的指标。

## [三.项目作用]()
- 深入了解使用者画像及行为偏好，找到最优算法，挖掘出影响用户流失的关键因素从而更好地完善产品设计、提升用户体验。


## [四.项目实现思路]()
### 整个分析的流程分为两个阶段，分别如下:
#### (一)准备阶段，在用户基本资料、用户订单资料、用户APP行为资料中选取并变换出与目标相关的指标货特征，做出一系列的数值处理。具体包括以下6步:
1. 导入与导出数据表;
1. 用户基本资料分析处理，主要是缺失值填补;
1. 用户订单资料分析处理，主要是新特征的分析与产生;
1. 用户APP行为的分析处理，主要是新特征的分析与产生、缺失值调整、极值调整;
1. 基于用户订单资料与用户APP行为的整合分析处理，强调基于已产生的特征进行再此特征发现;
1. 汇总所有特征，并处理缺失值本项目有大量的特征需要从原始资料中提取，过程比较烦琐，可结合代码调试。

#### (二)数据挖掘阶段，主要是技能型成单预测，要先将前整理汇总的特征与目标组合成能进行分析的格式，而后通过分析工具(分类器)对用户是否会购买服务进行预测,并将预测结果与实际结果进行比较，测试模型的准确程度。具体包括以下两步:
1. 将特含恶搞与目标数据表进行合并，产生新的数据集用于数据挖掘;
1. 以XGBoost为例对精品旅行服务成单进行预测。

## [五.数据说明]()
- tablel原始数据集包含51个字段及689945条数据。

字段名  | 数据类型  | 字段定义
 ---- | ----- | ------  
 label  | int64 |  用户是否流失
  sampleid   | int64  | 样本ID  
 d  | object | 访问时间
 arrival  | object | 入住时间
 iforderpv_24h      | int64 | 24小时内是否询问订单填写
 decisionhabit_user   | float64 | 用户行为类型(决策习惯)
  historyvisit_7ordernum  |  float64 | 近7天用户历史订单数
 historyvisit_totalordernum   | float64 | 近一年用户历史订单数
  hotelcr  | float64 | 当前酒店历史流动率
 hotelcr  | float64 | 当前酒店历史流动率
  ordercanceledprecent   | float64 | 用户一年内取消订单率
 landhalfhours  | float64 | 24小时登录时长
  ordercanncelednum   | float64 | 用户一年内取消订单数
 commentnums  | float64 |当前酒店点评数
   starprefer   |float64 | 星级偏好 
 novoters   | float64 | 当前酒店评分人数
  consuming_capacity  | float64 | 消费能力指数 
 historyvisit_avghotelnum  | float64 | 酒店对平均历史访客数
  cancelrate  | float64 | 当前酒店历史取消率 
 historyvisit_visit_detailpagenum  | float64 | 酒店详情页对访客数
  delta_price1  | float64 | 用户偏好价格 
 price_sensitive   | float64 | 价格敏感指数
  hoteluv  | float64 | 当前酒店历史UV 
 businessrate_pre  | float64 | 24小时内历史浏览次数最多对酒店的商务属性指数
  ordernum_oneyear   | float64 | 用户一年内订单数 
 cr_pre  | float64 | 24小时历史浏览次数最多的酒店的历史流动率
  avgprice   | float6 | 平均价格 
 lowestprice  | float64 | 当前酒店可订最低价格
  firstorder_bu  | float64 | 首个订单 
 customereval_pre2   | float64 | 24小时历史浏览酒店客户评分均值
  delta_price2   | float64 | 用户偏好价格，算法：近24小时内浏览酒店的平均价格 
 commentnums_pre  | float64 | 24小时内历史浏览次数最多的酒店的点评数
  customer_value_profit  | float64  | 近一年的用户价值
 commentnums_pre2  | float64 | 24小时内历史浏览酒店并点评的次数均值 cancelrate_pre  | float64 | 24小时内访问次数最多的酒店的历史取消率
 novoters_pre2   | float64 | 24小时内历史浏览酒店评分数均值
 novoters_pre  | float64 | 24小时内历史浏览次数最多的酒店的评分数 
 ctrip_profits   | float64 | 客户价值
 deltaprice_pre2_t1  | float64 | 24小时内访问酒店价格与对手价差均值T+1
 lowestprice_pre  | float64 | 20小时内最低的价格
 uv_pre  | float64 | 24小时内历史浏览次数最多的酒店历史UV
 uv_pre2   |  float64 | 24小时内历史浏览次数最多的酒店历史UV均值
 lowestprice_pre2  | float64 | 24小时内访问次数最多的酒店的可订最低价
 lasthtlordergap  | float64 | 一年内距离上次下单时长
 businessrate_pre2   | float64 | 24小时内访问酒店的商务属性均值
 cityuvs  | float64 | 城市的访客数量
cityorders  | float64 | 城市的订单量
 lastpvgap  | float64 | 最终PV的差值
 cr  | float64 | 流动率
 sid | int64 | 唯一身份编码
 visitnum_oneyear  | float64 | 年访问次数
 h  | int64 | 访问时间点
