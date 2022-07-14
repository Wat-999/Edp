import pandas as pd

table = pd.read_csv('rawdata/table1.csv')
#获取列信息
F1_1 = table[['label', 'sampleid', 'historyvisit_7ordernum', 'historyvisit_totalordernum', 'ordercanceledprecent', 'ordercanncelednum',
              'historyvisit_avghotelnum', 'delta_price1', 'businessrate_pre', 'cr_pre', 'landhalfhours', 'starprefer', 'price_sensitive',
              'commentnums_pre2', 'cancelrate_pre', 'novoters_pre2', 'novoters_pre', 'commentnums_pre2', 'cancelrate_pre', 'lowestprice_pre',
              'uv_pre', 'uv_pre2', 'hoteluv', 'cancelrate', 'novoters', 'commentnums', 'hotelcr', 'visitnum_oneyear', 'ordernum_oneyear',
              'cityorders', 'iforderpv_24h', 'consuming_capacity', 'avgprice', 'ctrip_profits', 'customer_value_profit', 'commentnums_pre',
              'delta_price2', 'ordernum_oneyear', 'firstorder_bu', 'd', 'arrival']]
#重命名列名
F1_1.columns = ['label', 'ID', 'F1.1', 'F1.2', 'F1.3', 'F1.4', 'F1.5', 'F1.6', 'F1.7', 'F1.8', 'F1.9', 'F1.10', 'F1.11', 'F1.12', 'F1.13', 'F1.14',
                'F1.15', 'F1.16', 'F1.17', 'F1.18', 'F1.19', 'F1.20', 'F1.21', 'F1.22', 'F1.23', 'F1.24', 'F1.25', 'F1.26', 'F1.27', 'F1.28', 'F1.29',
                'F1.30', 'F1.31', 'F1.32', 'F1.33', 'F1.34', 'F1.35', 'F1.36', 'F1.37', 'F1.38', 'F1.39']
#空值替换为NA
F1_1 = F1_1.fillna('NA')
F1_1.to_csv('workeddata/F1_1.csv', index=False, encoding="utf_8_sig")
#table.info()
#print(F1_1)
