
import yfinance as yf
import datetime as dt 
import matplotlib.pyplot as plt
from matplotlib import style
import  pandas  as pd 
import pandas_datareader.data as web
from flask import url_for, current_app
import os
import sys
import requests

def isTickerValid(ticker):
    try:
        # aTicker = yf.Ticker(ticker)
        # aTicker.info
        df = web.DataReader(ticker, 'yahoo', dt.datetime(2020,1,1), dt.datetime.now())
        return True
    except:
        return False
    

def getNameToTicker(ticker):
    companyName = ""
    try:
        aTicker = yf.Ticker(ticker)
        companyName = aTicker.info['longName']
        # print('_____________',  file=sys.stderr)
        # print(str(aTicker.info),  file=sys.stderr)
    except:
        try:
            url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(ticker)

            result = requests.get(url).json()

            for x in result['ResultSet']['Result']:
                if x['symbol'] == ticker:
                    companyName=  x['name']

        except:
            companyName = " Name NA (Data found) "
    return companyName


def getCorrelationDiagram(ticker1, ticker2):
    
    result = [['2017-01-01',0.1],['2018-01-01',0.8],['2018-01-01',0.5] ]




    
    return result



def getPortfolioCorrelation(positions, ticker, filterStart = dt.datetime(1971,1,1), filterEnd = dt.datetime.now(), daily=True):

    dfList = []

    for p in positions:
        updateStockData(p.ticker)
        stockdataPath = os.path.join(current_app.root_path, 'static/resources/stockdata/' + p.ticker + '.pkl')
        dfToAdd = pd.read_pickle(stockdataPath)
        dfToAdd.drop(dfToAdd.columns.difference(['Adj Close']), 1, inplace=True)
        # print(p.ticker + ' df')
        # print(dfToAdd)

        # if not daily:
        #     # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
        #     dfToAdd=dfToAdd[~dfToAdd.index.strftime('%Y-%m').duplicated()].copy()

        # dfToAdd['adj_return']=(dfToAdd['Adj Close']/ dfToAdd['Adj Close'].shift(1)) -1
        # dfToAdd.dropna(inplace=True)
        # dfToAdd.drop(dfToAdd.columns.difference(['adj_return']), 1, inplace=True)
        # dfToAdd['adj_return'] = (0.01*p.percent)*dfToAdd['adj_return']

        # print(p.ticker + ' df weighted')
        # print(dfToAdd)
        
        dfList.append(dfToAdd)


    merge = dfList[0]
    for i in range (1,len(dfList)):
        merge  = pd.merge(merge,dfList[i], how='inner', left_index=True, right_index=True) 

    # print('Merge')    
    # print(merge)

   




    updateStockData(ticker)
    stockdataPathBench = os.path.join(current_app.root_path, 'static/resources/stockdata/' + ticker + '.pkl')
    dfBench = pd.read_pickle(stockdataPathBench)
    dfBench.drop(dfBench.columns.difference(['Adj Close']), 1, inplace=True)

    dfBench.columns = ['Benchmark']

    # print('dfBench: ' + ticker )    
    # print(dfBench)

    # if not daily:
    #         # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
    #         dfBench=dfBench[~dfBench.index.strftime('%Y-%m').duplicated()].copy()


    merge  = pd.merge(merge,dfBench, how='inner', left_index=True, right_index=True) 

    if not daily:
            # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
            merge=merge[~merge.index.strftime('%Y-%m').duplicated()].copy()

    mask = (merge.index > pd.to_datetime(filterStart)) & (merge.index <= pd.to_datetime(filterEnd))
    merge = merge.loc[mask]

    # print('Merge wiith Bench')
    # print(merge)


    # merge = merge.apply(lambda x: x/x.shift(1)-1)
    # merge.dropna(inplace=True)

    for i in range(len(positions)+1):
        divisor= merge[merge.columns[i]].iloc[0]
        merge[merge.columns[i]] = merge[merge.columns[i]]/divisor

    # print('Merge')    
    # print(merge)


    for i in range(len(positions)):
        merge[merge.columns[i]] = (0.01*positions[i].percent)*merge[merge.columns[i]]


    merge['Portfolio'] = merge.drop('Benchmark', axis=1).sum(axis=1)

    merge.drop(merge.columns.difference(['Portfolio', 'Benchmark']), 1, inplace=True)

    # print('Merge2 after sum')    
    # print(merge)
    

            
    # merge['portfolio'] = merge.sum(axis=1)
    # merge.drop(merge.columns.difference(['portfolio']), 1, inplace=True)


    # print( ' df merge summed')
    # print(merge)

    

    # dfBench['adj_return']=(dfBench['Adj Close']/ dfBench['Adj Close'].shift(1)) -1
    # dfBench.dropna(inplace=True)
    # dfBench.drop(dfBench.columns.difference(['adj_return']), 1, inplace=True)


    # print( ' df bench summed')
    # print(dfBench)

    # merge = pd.merge(merge,dfBench,how='inner', left_index=True, right_index=True)

    
    
    if not merge.empty:
        evaluatedFrom = merge.index[0].strftime('%d. %B %Y')
        evaluatedTo = merge.index[-1].strftime('%d. %B %Y')
    else:
        evaluatedFrom = filterStart.strftime('%d. %B %Y')
        evaluatedTo = filterEnd.strftime('%d. %B %Y')


    # print( ' df merge corr')
    # print(merge)


    result = merge.corr().values
    result= result.round(4)

    # print('Result')
    # print (result)

    return result[0][1], evaluatedFrom, evaluatedTo


  


def getCorrelationMatrix(tickers, filterStart = dt.datetime(1971,1,1), filterEnd = dt.datetime.now(), daily=True  ):
    
    # result = [[1.0,0.1,0.25,0.1],[0.3,1.0,0.2,0.1],[0.6,0.5,1.0,0.1],[0.6,0.5,0.4,1.0] ]
    
    # print('Compute Correlation for',  file=sys.stderr)
    # print(filterStart,  file=sys.stderr)
    # print(filterEnd,  file=sys.stderr)


    dfList = []

    for tick in tickers:
        updateStockData(tick)
        stockdataPath = os.path.join(current_app.root_path, 'static/resources/stockdata/' + tick + '.pkl')
        dfToAdd = pd.read_pickle(stockdataPath)    
        dfReduce= dfToAdd.drop(dfToAdd.columns.difference(['Adj Close']), 1)
        # print(tick)
        # print(dfReduce)

        if not daily:
            # mask = dfReduce.index.is_month_start 
            # dfReduce = dfReduce.loc[mask]


            # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
            dfReduce=dfReduce[~dfReduce.index.strftime('%Y-%m').duplicated()].copy()

        
        dfList.append(dfReduce)


    merge = dfList[0]
    for i in range (1,len(dfList)):
        merge = pd.merge(merge,dfList[i],how='inner', left_index=True, right_index=True)

    mask = (merge.index > pd.to_datetime(filterStart)) & (merge.index <= pd.to_datetime(filterEnd))

    merge = merge.loc[mask]

    # print( ' merge before')
    # print(merge)


    # for i in range(len(tickers)):
    #     divisor= merge[merge.columns[i]].iloc[0]
    #     merge[merge.columns[i]] = merge[merge.columns[i]]/divisor

    # print('Date Convert:')
    # print (pd.to_datetime(filterStart))

    # print(merge)
    # print(merge.index[0])
    # print(merge.index[-1])


    # print('merge fater')
    # print(merge)
    
    
    if not merge.empty:
        evaluatedFrom = merge.index[0].strftime('%d. %B %Y')
        evaluatedTo = merge.index[-1].strftime('%d. %B %Y')
    else:
        evaluatedFrom = filterStart.strftime('%d. %B %Y')
        evaluatedTo = filterEnd.strftime('%d. %B %Y')

    




    result = merge.corr().values
    result= result.round(4)

    return result, evaluatedFrom, evaluatedTo

def updateStockData(ticker):

    stockdataPath = os.path.join(current_app.root_path, 'static/resources/stockdata/' + ticker + '.pkl')
    if (os.path.exists(stockdataPath)):
        # print('Stock already saved. Update...',  file=sys.stderr)
        saveStockDataAlreadyExisting(ticker)
    else:
        # print('Start saving stock from Scratch',  file=sys.stderr)
        saveStockDataFromScratch(ticker)

    
def saveStockDataFromScratch(ticker):
    stockdataPath = os.path.join(current_app.root_path, 'static/resources/stockdata/' + ticker + '.pkl')
    stockdataPathCSV = os.path.join(current_app.root_path, 'static/resources/stockdata/' + ticker + '.csv')

    start = dt.datetime(1971,1,1)
    end = dt.datetime.now()
    # end = dt.datetime(2020,2,1)
    df = web.DataReader(ticker, 'yahoo', start, end)
       
    print(stockdataPath,  file=sys.stderr)

    df.to_pickle(stockdataPath)
    # df.to_csv(stockdataPathCSV)

    

def saveStockDataAlreadyExisting(ticker):
    stockdataPath = os.path.join(current_app.root_path, 'static/resources/stockdata/' + ticker + '.pkl')
    stockdataPathCSV = os.path.join(current_app.root_path, 'static/resources/stockdata/' + ticker + '.csv')
    df = pd.read_pickle(stockdataPath)



    
    lastRecord = df.index[-1]
    endNow = dt.datetime.now()

    duration = endNow-lastRecord

    # print('lastRecord')
    # print (lastRecord)
    # print('endNow')
    # print (endNow)

    # print('Duration')
    # print (duration)


    if (duration.days>4):


        df2 = web.DataReader(ticker, 'yahoo', df.index[-1], endNow)

    
        df2.drop(df.index[-1],inplace=True)

        print('Update stock DATA!!!!!')
        print('OLD',  file=sys.stderr)
        print(df,  file=sys.stderr)
        print('Add',  file=sys.stderr)
        print(df2,  file=sys.stderr)
        df = df.append(df2)

    df.to_pickle(stockdataPath)
    # df.to_csv(stockdataPathCSV)

    
