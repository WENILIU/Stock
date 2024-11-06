
# coding: utf-8

# In[1]:

import time
import os
import json
import datetime
tStart = time.time()
tEnd = time.time()
print( (tEnd - tStart))
import configparser


# In[2]:

def save_json_data(tempdata,Filepath):
    json_data = json.dumps(tempdata, indent=4)
    with open(Filepath, "w") as json_file:
        json_file.write(json_data)


# In[3]:

#身分驗證
from fugle_marketdata import RestClient
client = RestClient(api_key='MmRkMTA5OWUtNjM3OS00YmQ5LTk4ZWMtNTYzOGQyMjY5MWY2IGIyYTNhYWY5LTcxY2ItNGUyMy04NTVhLTU0ZDhkNzE2ZjM1Mw==')
stock = client.stock


# In[4]:

#取得股票或指數列表
StockID_dic=stock.intraday.tickers(type='EQUITY', exchange="TWSE", isNormal=True)


# In[5]:

def ntraday_trades(StockID):
    try:
        trades_his=stock.intraday.trades(symbol=StockID)
        return 'Y',trades_his
    except Exception as e:
        print('ntraday_trades error:'+str(e)+str(e.__traceback__.tb_lineno))
        return 'N',""


# In[6]:

config = configparser.ConfigParser()
config.read('d:\\configfile\\fugle_marketdata_Get_historyData_ValueVolum.ini',encoding="utf-8")
history_File = config.get('Section_Job', 'history_File')
history_File2 = config.get('Section_Job', 'history_File2')
history_File3 = config.get('Section_Job', 'history_File3')


# In[8]:

def ntraday_candles(StockID):
    try:
        trades_his=stock.intraday.candles(symbol=StockID)
        return 'Y',trades_his
    except Exception as e:
        print('ntraday_candles error:'+str(e)+str(e.__traceback__.tb_lineno))
        return 'N',""


# In[9]:

#取得股票漲跌幅排行
#history_File='F:\\文義\\股票資料\\股票歷史資料\\股票漲跌幅排行\\'
direction_list=['up','down']
if not os.path.exists(history_File):os.makedirs(history_File)
for direction in direction_list:
    trades_his=stock.snapshot.movers(market='TSE', direction=direction, change='percent')
    date=trades_his['date']
    Filepath=history_File+'\\'+date+'_'+direction+'.json'
    save_json_data(trades_his,Filepath)


# In[10]:

#取得股票成交量值排行
#history_File2='F:\\文義\\股票資料\\股票歷史資料\\股票成交量值排行\\'
trade_list=['volume','value']
if not os.path.exists(history_File2):os.makedirs(history_File2)
for trade_list in trade_list:
    trades_his=stock.snapshot.actives(market='TSE', trade=trade_list)
    date=trades_his['date']
    Filepath=history_File2+'\\'+date+'_'+trade_list+'.json'
    save_json_data(trades_his,Filepath)


# In[11]:

#取得股票分價量表
#history_File3='F:\\文義\\股票資料\\股票歷史資料\\股票分價量表\\'
if not os.path.exists(history_File3):os.makedirs(history_File3)
for i in range(len(StockID_dic['data'])):
    StockID=StockID_dic['data'][i]['symbol']
    Stock_name=StockID_dic['data'][i]['name']
    Stock_name=Stock_name.replace('*','')
    trades_his=stock.intraday.volumes(symbol=StockID)
    date=trades_his['date']
    if not os.path.exists(history_File3+Stock_name):os.makedirs(history_File3+Stock_name)
    Filepath=history_File3+'\\'+Stock_name+'\\'+StockID+'_'+date+'.json'
    save_json_data(trades_his,Filepath)
    #break;


# In[14]:

trades_his


# In[ ]:




# In[ ]:




# In[ ]:



