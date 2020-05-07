import datetime as dt 
import matplotlib.pyplot as plt
from matplotlib import style
import  pandas  as pd 
import pandas_datareader.data as web


# style.use('ggplot')
# start = dt.datetime(1971,1,1)
# end = dt.datetime.now()

start = dt.datetime(2018,1,1)
end = dt.datetime(2020,1,1)

df = web.DataReader('SKT', 'yahoo', start, end)
df2 = web.DataReader('MSFT', 'yahoo', start, end)
df3 = web.DataReader('AAPL', 'yahoo', start, end)

print(df)

df['adj_return']=(df['Adj Close']/ df['Adj Close'].shift(1)) -1
df.dropna(inplace=True)

df2['adj_return']=(df2['Adj Close']/ df2['Adj Close'].shift(1)) -1
df2.dropna(inplace=True)

df3['adj_return']=(df3['Adj Close']/ df3['Adj Close'].shift(1)) -1
df3.dropna(inplace=True)

df.drop(df.columns.difference(['adj_return']), 1, inplace=True)
df2.drop(df2.columns.difference(['adj_return']), 1, inplace=True)
df3.drop(df3.columns.difference(['adj_return']), 1, inplace=True)


print(df)
print(df2)
print(df3)

dfList = []
dfList.append(df)
dfList.append(df2)
dfList.append(df3)

print('__________')

for i in range (0,len(dfList)):
    dfList[i]['adj_return'] = 0.33*dfList[i]['adj_return']
    print(dfList[i])





merge = dfList[0]
for i in range (1,len(dfList)):
    merge  = pd.merge(merge,dfList[i],how='inner', left_index=True, right_index=True) 



merge['portfolio'] = merge.sum(axis=1)
merge.drop(merge.columns.difference(['portfolio']), 1, inplace=True)

# dfRes['adj_return'] = 0.33*dfList[0]['adj_return']

# for i in range (0,len(dfList)):
#     dfList[i].mul(0.33)


# dfRes=dfList[0]
# for i in range (1,len(dfList)):
#     dfRes.add(dfList[i])


print(merge)



# pf['adj_return'] = 
# print(df)



# filterStart = '2018-04-27'
# filterEnd = '2020-11-19'

# mask = (df.index > filterStart) & (df.index <= filterEnd)

# df = df.loc[mask]

# mask = df.index.is_month_start 
# df = df.loc[mask]
# df=df[~df.index.strftime('%Y-%m').duplicated()].copy()


# print(df)

# print('XXXXXXX')
# print(df.index[-1])
# endNow = dt.datetime.now()

# df2 = web.DataReader('AAPL', 'yahoo', df.index[-1], endNow)
# df2FirstRowRemoved = df2.iloc[1:]

# print(df)
# print(df2FirstRowRemoved)
# print('XXXXXXX')
# df = df.append(df2.iloc[1:])

# print('XXXXXXX')
# print(df)




# df.drop(df.columns.difference(['Adj Close']), 1, inplace=True)
# df2.drop(df2.columns.difference(['Adj Close']), 1, inplace=True)
# df3.drop(df3.columns.difference(['Adj Close']), 1, inplace=True)


# dfReduced = df.drop(df.columns.difference(['Adj Close']), 1)
# dfReduced2 = df2.drop(df2.columns.difference(['Adj Close']), 1)
# dfReduced3 = df3.drop(df2.columns.difference(['Adj Close']), 1)


# dfList  = []
# dfList.append(dfReduced)
# dfList.append(dfReduced2)
# dfList.append(dfReduced3)


# merge = dfList[0]

# for i in range (1,len(dfList)):
#     merge  = pd.merge(merge,dfList[i],how='inner', left_index=True, right_index=True) 




# merge  = pd.merge(dfReduced,dfReduced2,how='inner', left_index=True, right_index=True)



# print(dfReduced.head(6))
# print(dfReduced2.head(6))
# print(dfReduced3.head(6))
# print(merge.head(6))
# print (merge.corr())


