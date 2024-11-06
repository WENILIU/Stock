
# coding: utf-8

# In[7]:

import time
import os
import json
import datetime
tStart = time.time()
tEnd = time.time()
print( (tEnd - tStart))


# In[8]:

def save_json_data(tempdata,Filepath):
    json_data = json.dumps(tempdata, indent=4)
    with open(Filepath, "w") as json_file:
        json_file.write(json_data)


# In[9]:

#身分驗證
from fugle_marketdata import RestClient
client = RestClient(api_key='MmRkMTA5OWUtNjM3OS00YmQ5LTk4ZWMtNTYzOGQyMjY5MWY2IGIyYTNhYWY5LTcxY2ItNGUyMy04NTVhLTU0ZDhkNzE2ZjM1Mw==')
stock = client.stock


# In[10]:

#取得股票或指數列表
StockID_dic=stock.intraday.tickers(type='EQUITY', exchange="TWSE", isNormal=True)


# In[11]:

def historical_candles(StockID,date_from,date_to,timeframe):
    try:
        trades_candles=stock.historical.candles(**{"symbol": StockID, "from": date_from, "to": date_to,"timeframe":timeframe, "fields": "open,high,low,close,volume,change"})
        return 'Y',trades_candles
    except Exception as e:
        print('historical_candles error:'+str(e)+str(e.__traceback__.tb_lineno))
        return 'N',""


# In[12]:

#取得股票價格Ｋ線(歷史日,周,月 K)
history_File='F:\\文義\\股票資料\\股票歷史資料\\股票價格Ｋ線\\'
datetime_now=str(datetime.datetime.now())
date_from=datetime_now[0:10]
date_to=datetime_now[0:10]
year='2024'
year_list=['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']
date_from=year+'-01-01'
date_to=year+'-12-31'
timeframe_list=['D','W','M']
tStart = time.time()
count=0
for year in year_list:
    for i in range(len(StockID_dic['data'])):
        StockID=StockID_dic['data'][i]['symbol']
        Stock_name=StockID_dic['data'][i]['name']
        Stock_name=Stock_name.replace('*','')
        for timeframe in timeframe_list:
            if not os.path.exists(history_File+Stock_name):os.makedirs(history_File+Stock_name)
            if not os.path.exists(history_File+Stock_name+'\\'+str(timeframe)+'\\'):os.makedirs(history_File+Stock_name+'\\'+str(timeframe)+'\\')
            #trades_candles=stock.historical.candles(**{"symbol": StockID, "from": date_from, "to": date_to,"timeframe":timeframe, "fields": "open,high,low,close,volume,change"})
            Flag=False
            while Flag==False:
                result,trades_candles=historical_candles(StockID,date_from,date_to,timeframe)
                if result=='N':
                    Flag=False
                else:
                    Flag=True
            Filepath=history_File+Stock_name+'\\'+timeframe+'\\'+StockID+'_'+year+'.json'
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



