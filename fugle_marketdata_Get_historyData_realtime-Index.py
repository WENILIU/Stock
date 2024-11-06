
# coding: utf-8

# In[53]:

import time
import os
import json
import datetime
tStart = time.time()
tEnd = time.time()
print( (tEnd - tStart))


# In[54]:

def save_json_data(tempdata,Filepath):
    json_data = json.dumps(tempdata, indent=4)
    with open(Filepath, "w") as json_file:
        json_file.write(json_data)


# In[55]:

#身分驗證
from fugle_marketdata import RestClient
client = RestClient(api_key='MmRkMTA5OWUtNjM3OS00YmQ5LTk4ZWMtNTYzOGQyMjY5MWY2IGIyYTNhYWY5LTcxY2ItNGUyMy04NTVhLTU0ZDhkNzE2ZjM1Mw==')
stock = client.stock


# In[56]:

#取得股票或指數列表
StockID_dic=stock.intraday.tickers(type='INDEX', exchange="TWSE")


# In[57]:

def ntraday_trades(StockID):
    try:
        trades_his=stock.intraday.trades(symbol=StockID)
        return 'Y',trades_his
    except Exception as e:
        print('ntraday_trades error:'+str(e)+str(e.__traceback__.tb_lineno))
        return 'N',""


# In[58]:

#trades_his=stock.intraday.trades(symbol='IX0001')


# In[59]:

#取得股票成交明細
history_File='F:\\文義\\股票資料\\股票歷史資料\\指數成交明細\\'
for i in range(len(StockID_dic['data'])):
    StockID=StockID_dic['data'][i]['symbol']
    Stock_name=StockID_dic['data'][i]['name']
    Stock_name=Stock_name.replace('*','')
    if not os.path.exists(history_File+Stock_name):os.makedirs(history_File+Stock_name)
    #trades_his=stock.intraday.trades(symbol=StockID) 
    Flag=False
    while Flag==False:
        result,trades_his=ntraday_trades(StockID)
        if result=='N':
            Flag=False
        else:
            Flag=True
    date=trades_his['date']
    Filepath=history_File+Stock_name+'\\'+StockID+'_'+date+'.json'
    save_json_data(trades_his,Filepath)
    print(i)
    #break;


# In[60]:

def ntraday_candles(StockID):
    try:
        trades_his=stock.intraday.candles(symbol=StockID)
        return 'Y',trades_his
    except Exception as e:
        print('ntraday_candles error:'+str(e)+str(e.__traceback__.tb_lineno))
        return 'N',""


# In[61]:

#取得股票價格Ｋ線(即時)
history_File='F:\\文義\\股票資料\\股票歷史資料\\指數價格Ｋ線(即時)\\'
for i in range(len(StockID_dic['data'])):
    #if i <=755:continue
    StockID=StockID_dic['data'][i]['symbol']
    Stock_name=StockID_dic['data'][i]['name']
    Stock_name=Stock_name.replace('*','')
    if not os.path.exists(history_File+Stock_name):os.makedirs(history_File+Stock_name)
    #trades_his=stock.intraday.candles(symbol=StockID)
    Flag=False
    while Flag==False:
        result,trades_his=ntraday_candles(StockID)
        if result=='N':
            Flag=False
        else:
            Flag=True
    date=trades_his['date']
    Filepath=history_File+Stock_name+'\\'+StockID+'_'+date+'.json'
    save_json_data(trades_his,Filepath)
    #time.sleep(1)
    print(i)


# In[ ]:




# In[ ]:



