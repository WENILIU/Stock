
# coding: utf-8

# In[1]:

import time
import json
import pandas as pd
import numpy as np
tStart = time.time()
tEnd = time.time()
print( (tEnd - tStart))


# In[2]:


#重要支撐壓力指標
#盤中新高點(B點)
#回檔新低點(C點)-->止跌點
#交易量指標(by分K)
#相對成交量 (分K成交量/平均成交量)
#跌破前一隻分K的低點
#橫向盤整期的旗形
#多頭旗形(Bull Flag)
#十字線
#分K連續出現上漲或下跌的線形(算隻數 ex:連續5隻上漲)
#RSI
#移動平均趨勢交易
#紅轉綠交易
#開盤區間突破
#壘包指標(一壘,二壘,三壘,全壘打,場外全壘打,0壘包)
#每日特定時
#發展自己的策略
#技術指標只是指標,不是命令


# In[ ]:




# In[172]:

#VWAP指標
def calculate_vwap(data):
    data=data['data']
    grouped_data = {}
    for entry in data:
        timestamp = entry['date']  # 提取日期和時間部分（不包含秒）
        
        if timestamp not in grouped_data:
            grouped_data[timestamp] = {
                'volume': 0,
                'value': 0
            }
        
        volume = entry['volume']
        price = (entry['high'] + entry['low'] + entry['close']) / 3
        closeprice=entry['close']
        value = volume * price

        grouped_data[timestamp]['volume'] = volume
        grouped_data[timestamp]['value'] = value
        grouped_data[timestamp]['closeprice'] = closeprice
    
    vwap_list = []
    
    total_volume=0
    total_value=0
    for timestamp, values in grouped_data.items():
        total_volume += values['volume']
        total_value += values['value']
        closeprice = values['closeprice']
        
        vwap = total_value / total_volume if total_volume != 0 else 0
        
        vwap_list.append({
            'timestamp': timestamp,
            'vwap': vwap,
            'closeprice': closeprice
        })
    
    return vwap_list


# In[ ]:

#VWAP指標
def calculate_vwap_adjust(data,adjust_thre):
    data=data['data']
    grouped_data = {}
    for entry in data:
        timestamp = entry['date']  # 提取日期和時間部分（不包含秒）
        
        if timestamp not in grouped_data:
            grouped_data[timestamp] = {
                'volume': 0,
                'value': 0
            }
        
        volume = entry['volume']
        price = (entry['high'] + entry['low'] + entry['close']) / 3
        closeprice=entry['close']
        value = volume * price

        grouped_data[timestamp]['volume'] = volume
        grouped_data[timestamp]['value'] = value
        grouped_data[timestamp]['closeprice'] = closeprice
    
    vwap_list = []
    
    total_volume=0
    total_value=0
    adjust_count=0
    
    for timestamp, values in grouped_data.items():
        total_volume += values['volume']
        total_value += values['value']
        closeprice = values['closeprice']
        adjust_count+=1
        if adjust_count> adjust_thre:
            strat_index=adjust_count-adjust_thre
            end_index=adjust_count
            total_volume=0
            total_value=0
            for index in range(strat_index,end_index):
                total_volume += list(grouped_data.values())[index]['volume']
                total_value += list(grouped_data.values())[index]['value']
        
        vwap = total_value / total_volume if total_volume != 0 else 0
        
        vwap_list.append({
            'timestamp': timestamp,
            'vwap': vwap,
            'closeprice': closeprice
        })
    
    return vwap_list


# In[173]:

#MA指標(週期5,10,20,60)
def calculate_ma(data,K=5):
    data=data['data']
    grouped_data = {}
    value_list=[]
    MA_list=[]
    #K=5
    for entry in data:
        timestamp = entry['date']  # 提取日期和時間部分（不包含秒）

        if timestamp not in grouped_data:
            grouped_data[timestamp] = {
                'value': 0
            }
        price = (entry['close'])
        value = price
        grouped_data[timestamp]['value'] = value
        value_list.append(value)

    df = pd.DataFrame(data) 
    df['MA'] = df['close'].rolling(window=K).mean()
    latest_ma = df['MA'].tail(1)

    count=0
    for timestamp, values in grouped_data.items():
        #if count<K-1:
        #    MA=np.nan
        #else:
        #    MA = sum(value_list[count-K+1:count+1])/K
        MA =df['MA'][count]
        count=count+1
        MA_list.append({
            'timestamp': timestamp,
            'MA': MA
        })
    return MA_list


# In[ ]:

#VMA指標(週期5,10,20,60)
def calculate_vma(data,K=5):
    data=data['data']
    grouped_data = {}
    value_list=[]
    MA_list=[]
    #K=5
    for entry in data:
        timestamp = entry['date']  # 提取日期和時間部分（不包含秒）

        if timestamp not in grouped_data:
            grouped_data[timestamp] = {
                'value': 0
            }
        volume = (entry['volume'])
        value = volume
        grouped_data[timestamp]['value'] = value
        value_list.append(value)

    df = pd.DataFrame(data) 
    df['MA'] = df['volume'].rolling(window=K).mean()
    latest_ma = df['MA'].tail(1)

    count=0
    for timestamp, values in grouped_data.items():
        #if count<K-1:
        #    MA=np.nan
        #else:
        #    MA = sum(value_list[count-K+1:count+1])/K
        MA =df['MA'][count]
        count=count+1
        MA_list.append({
            'timestamp': timestamp,
            'MA': MA
        })
    return MA_list


# In[174]:

#EMA指標(週期5,10,20,60)
def calculate_ema(data,K=5):
    data=data['data']
    grouped_data = {}
    value_list=[]
    EMA_list=[]
    for entry in data:
        timestamp = entry['date']  # 提取日期和時間部分（不包含秒）

        if timestamp not in grouped_data:
            grouped_data[timestamp] = {
                'value': 0
            }
        price = (entry['close'])
        value = price
        grouped_data[timestamp]['value'] = value
        value_list.append(value)

    df = pd.DataFrame(data) 
    df['EMA'] = df['close'].ewm(span=K, adjust=False).mean()
    latest_ema = df['EMA'].tail(1)

    count=0
    for timestamp, values in grouped_data.items():
        EMA =df['EMA'][count]
        count=count+1
        EMA_list.append({
            'timestamp': timestamp,
            'EMA': EMA
        })
    return EMA_list


# In[ ]:

def calculate_rsi(data, period=14):
    close_prices = [item['close'] for item in data['data']]
    deltas = np.diff(close_prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(close_prices)
    rsi[:period] = 100. - 100./(1. + rs)

    for i in range(period, len(close_prices)):
        delta = deltas[i-1]

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(period - 1) + upval)/period
        down = (down*(period - 1) + downval)/period

        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)

    return rsi


# In[ ]:




# In[ ]:




# In[ ]:



