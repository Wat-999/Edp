"""
项目背景
运营人员经常要预估店铺的销售额，用预估的销售额来做计划，一般运营人员会使用同比、环比的方式来预估销售额
业务需求：预估第2天的销售额，以便做日计划
数据说明
某类目下行业近3年的交易额数据和同比、环比的增长数据，数据都在一张表格中，表格的格式是xls。还有在该类目下某店铺近一个月每日的交易额数据，数据来自生意参谋后台导出的表格
实现思路
1计算去年同期市场的增幅
2使用店铺的销售额乘去年同期市场增幅来预测近期数据
"""

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

market = pd.read_excel('生参_市场_行业大盘.xls')
shop = pd.read_excel('店铺交易报表.xls')
market = market[['日期', '环比增长', '同比增长', '转化率趋势']]
shop = shop[['店铺名', '统计日期', '访客数', '支付买家数', '支付金额']]

now = shop.groupby('店铺名').max()

for i in now['统计日期']:
    # 获取当前店铺数据最新一天的日期
    date = datetime.datetime.strptime(i, "%Y-%m-%d")  
    # 获取当前店铺数据最新一天的日期的第二天日期
    date2 = date + datetime.timedelta(days=1) 
    # 获取去年同期市场的销售额环比增长和转化率趋势
    date3 = (date2 - relativedelta(years=1)).strftime('%Y-%m-%d') 
    data = market[market['日期'] == date3]
    a = float(data.get('环比增长')) + 1
    # 获取店铺最新一天的销售额
    shopdata = shop[shop['统计日期'] == date.strftime('%Y-%m-%d')]
    money = float(shopdata.get('支付金额'))


    print('根据上一年市场的销售额变化预测店铺未来的销售额')
    print('当天的销售额为:', money, '元')
    print('预测第二天的销售额为:', money*a, '元')

