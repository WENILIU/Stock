
# coding: utf-8

# In[9]:

import time
import os
import json
import datetime
tStart = time.time()
tEnd = time.time()
print( (tEnd - tStart))


# In[10]:

def save_json_data(tempdata,Filepath):
    json_data = json.dumps(tempdata, indent=4)
    with open(Filepath, "w") as json_file:
        json_file.write(json_data)


# In[11]:

#身分驗證
from fugle_marketdata import RestClient
client = RestClient(api_key='MmRkMTA5OWUtNjM3OS00YmQ5LTk4ZWMtNTYzOGQyMjY5MWY2IGIyYTNhYWY5LTcxY2ItNGUyMy04NTVhLTU0ZDhkNzE2ZjM1Mw==')
stock = client.stock


# In[13]:

#取得股票或指數列表
StockID_dic=stock.intraday.tickers(type='EQUITY', exchange="TWSE", isNormal=True)


# In[14]:

def historical_candles(StockID,timeframe):
    try:
        trades_candles=stock.historical.candles(**{"symbol": StockID,"timeframe":timeframe, "fields": "open,high,low,close,volume,change"})
        return 'Y',trades_candles
    except Exception as e:
        print('historical_candles error:'+str(e)+str(e.__traceback__.tb_lineno))
        return 'N',""


# In[16]:

#取得股票價格Ｋ線(歷史分K)
#history_File='D:\\股票價格Ｋ線\\'
history_File='F:\\文義\\股票資料\\股票歷史資料\\股票價格Ｋ線\\'
if not os.path.exists(history_File):os.makedirs(history_File)
datetime_now=str(datetime.datetime.now())
date=datetime_now[0:10]
timeframe_list=['1','5','15','30','60']
#timeframe='1'
tStart = time.time()
count=0
for i in range(len(StockID_dic['data'])):
    StockID=StockID_dic['data'][i]['symbol']
    Stock_name=StockID_dic['data'][i]['name']
    Stock_name=Stock_name.replace('*','')
    for timeframe in timeframe_list:
        if not os.path.exists(history_File+Stock_name):os.makedirs(history_File+Stock_name)
        if not os.path.exists(history_File+Stock_name+'\\'+timeframe+'\\'):os.makedirs(history_File+Stock_name+'\\'+timeframe+'\\')
        #trades_candles=stock.historical.candles(**{"symbol": StockID,"timeframe":timeframe, "fields": "open,high,low,close,volume,change"})
        Filepath=history_File+Stock_name+'\\'+timeframe+'\\'+StockID+'_'+date+'.json'
        Flag=False
        while Flag==False:
            result,trades_candles=historical_candles(StockID,timeframe)
            if result=='N':
                Flag=False
            else:
                Flag=True
        save_json_data(trades_candles,Filepath)
        count=count+1
        if count>=60:
            #進行等待與reset工作
            tEnd = time.time()
            tspent=tEnd-tStart
            twait=60-tspent
            print('twait:'+str(twait))
            if twait>=0:
                time.sleep(twait+10)
            count=0
            tStart = time.time()
    #break;


# In[ ]:



