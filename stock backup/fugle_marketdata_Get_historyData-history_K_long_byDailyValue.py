
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

def historical_candles(StockID,date_from,date_to,timeframe):
    try:
        trades_candles=stock.historical.candles(**{"symbol": StockID, "from": date_from, "to": date_to,"timeframe":timeframe, "fields": "open,high,low,close,volume,change"})
        return 'Y',trades_candles
    except Exception as e:
        print('historical_candles error:'+str(e)+str(e.__traceback__.tb_lineno))
        return 'N',""


# In[6]:

def StockValue_File_Get(StockValue_File):
    #StockValue_File='F:\\文義\\股票資料\\股票歷史資料\\股票成交量值排行\\'
    datetime_now=str(datetime.datetime.now())
    file=datetime_now[0:10]+'_value.json'
    file='2024-10-25_value.json'
    jsonFile = open(StockValue_File+file,'r')
    r = jsonFile.read()
    data= json.JSONDecoder().decode(r)

    StockID_filter=[]
    for i in range(len(data['data'])):
        StockID=data['data'][i]['symbol']
        Stock_name=data['data'][i]['name']
        if i<100:
            StockID_filter.append(StockID)
    return StockID_filter


# In[7]:

#取得股票價格Ｋ線(歷史日,周,月 K)
config = configparser.ConfigParser()
config.read('d:\\configfile\\fugle_marketdata_Get_historyData-history_K_long_byDailyValue.ini',encoding="utf-8")
history_File = config.get('Section_Job', 'history_File')
StockValue_File = config.get('Section_Job', 'StockValue_File')
StockID_filter = config.get('Section_Job', 'StockID_filter')

history_File='F:\\文義\\股票資料\\股票歷史資料\\股票價格Ｋ線\\'
StockValue_File='F:\\文義\\股票資料\\股票歷史資料\\股票成交量值排行\\'
datetime_now=str(datetime.datetime.now())
date_from=datetime_now[0:10]
date_to=datetime_now[0:10]
year='2024'
year_list=['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']
year_list=['2024']
date_from=year+'-01-01'
date_to=year+'-12-31'
timeframe_list=['D','W','M']
if StockID_filter=='':
    StockID_filter=StockValue_File_Get(StockValue_File)
else:
    #StockID_filter=['2330','2317','3231','2454','3450']
    StockID_filter=StockID_filter.split(',')
tStart = time.time()
count=0
for year in year_list:
    for i in range(len(StockID_dic['data'])):
        StockID=StockID_dic['data'][i]['symbol']
        Stock_name=StockID_dic['data'][i]['name']
        Stock_name=Stock_name.replace('*','')
        if StockID not in StockID_filter:continue
        print(StockID)
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
                twait=70-tspent
                print('twait:'+str(twait))
                if twait>=0:
                    time.sleep(twait+10)
                count=0
                tStart = time.time()
        #break;


# In[ ]:



