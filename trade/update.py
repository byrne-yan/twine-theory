##
import sys
import os
import pandas as pd
import tushare as ts
from pathlib import Path

def loadStock(rootdir,scode):
    workdir = Path(rootdir / scode)
    if not workdir.is_dir():
        return None

    lastWeek = None
    lastDay = None
    last30 = None
    last5 = None
    p_week = Path(workdir / (scode+'_w.csv'))
    if p_week.is_file():
        week = pd.read_csv(p_week,parse_dates=['date'],dtype={'code':str})
        lastWeek = week.iloc[-1].date

    p_day = Path(workdir / (scode+'_d.csv'))
    if p_week.is_file():
        day = pd.read_csv(p_day,parse_dates=['date'],dtype={'code':str})
        lastDay = day.iloc[-1].date

    p_30m = Path(workdir / (scode+'_30m.csv'))
    if p_week.is_file():
        m30 = pd.read_csv(p_30m,parse_dates=['date'],dtype={'code':str})
        last30 = m30.iloc[-1].date

    p_5m = Path(workdir / (scode+'_5m.csv'))
    if p_week.is_file():
        m5 = pd.read_csv(p_5m,parse_dates=['date'],dtype={'code':str})
        last5 = m5.iloc[-1].date

    return {
        'code':scode,
        'week':week,
        'day':day,
        'm30':m30,
        'm5':m5,
        'lastTime':[lastWeek,lastDay,last30,last5]
        }

        
def updateStock(rootdir,scode,stock):
    local = Path(rootdir / scode)
    if not local.is_dir():
        os.makedirs(local)
        
    name = scode+'_w.csv'
    p_week = Path(local / name)
    if not stock['week'].empty:
        stock['week'].to_csv(str(p_week),index=False)

    name = scode+'_d.csv'
    p_day = Path(local / name)
    if not stock['day'].empty:
        stock['day'].to_csv(str(p_day),index=False)

    name = scode+'_30m.csv'
    p_30m = Path(local / name)
    if not stock['m30'].empty:
        stock['m30'].to_csv(str(p_30m),index=False)

    name = scode+'_5m.csv'
    p_5m = Path(local / name)
    if not stock['m5'].empty:
        stock['m5'].to_csv(str(p_5m),index=False)
    
def merge(stock,scode,week,day,m30,m5):
    if not stock:
        return {
            'code':scode,
            'week':week,
            'day':day,
            'm30':m30,
            'm5':m5
            }

    w = stock['week'].append(week[week['date']>=str(stock['lastTime'][0])],ignore_index=True)
    d = stock['day'].append(day[day['date']>=str(stock['lastTime'][1])],ignore_index=True)
    m30 = stock['m30'].append(m30[m30['date']>=str(stock['lastTime'][2])],ignore_index=True)
    m5 = stock['m5'].append(m5[m5['date']>=str(stock['lastTime'][3])],ignore_index=True)
    return {
            'code':scode,
            'week':w,
            'day':d,
            'm30':m30,
            'm5':m5
        }
                                   
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage:update stock_dir")
        exit()
    stocksDir = sys.argv[1]
    rootdir = Path(sys.argv[1])
    if not rootdir.is_dir():
        print("%s must be a direcory!" % rootdir)
        exit()
    
    tracks = pd.read_excel(str(rootdir / 'tracks.xlsx'),dtype={'code':str})
    basicsFile = rootdir / 'basics.xlsx'

    basics = None
    if basicsFile.exists():
        basics = pd.read_excel(basicsFile,dtype={'code':str})
    if basics is None or basics.empty:
        basics = ts.get_stock_basics()
        basics.to_excel(str(rootdir / 'basics.xlsx'))
    
    for i in range(0,len(tracks)):
        st = tracks.iloc[i]
##        scode = "%06d" % st.code
##        import pdb;pdb.set_trace()  
        scode = st.code
        isIndex = (False if pd.isnull(st.isIndex) else True)

        startTimeW = ""
        startTimeD = startTimeW
        startTime30 = startTimeW
        startTime5 = startTimeW
##        import pdb;pdb.set_trace()        
        stock = loadStock(rootdir,scode)
        if stock:
            startTimeW = stock['lastTime'][0]
            startTimeD = stock['lastTime'][1]
            startTime30 = stock['lastTime'][2]
            startTime5 = stock['lastTime'][3]
            
##        import pdb;pdb.set_trace()

        kdata_w = ts.get_k_data(code=scode,index=isIndex,start=str(startTimeW), ktype='W')
        kdata_d = ts.get_k_data(code=scode,index=isIndex,start=str(startTimeD),ktype='D')
        kdata_30 = ts.get_k_data(code=scode,index=isIndex,start=str(startTime30),ktype='30')
        kdata_5 = ts.get_k_data(code=scode,index=isIndex,start=str(startTime5),ktype='5')


        stock2 = merge(stock,scode,kdata_w,kdata_d,kdata_30,kdata_5)
        updateStock(rootdir,scode,stock2)

        print("%s updated: (%s,%d), (%s,%d), (%s,%d), (%s,%d)" % (scode,startTimeW,len(kdata_w),startTimeD,len(kdata_d),startTime30,len(kdata_30),startTime5,len(kdata_5)) )
