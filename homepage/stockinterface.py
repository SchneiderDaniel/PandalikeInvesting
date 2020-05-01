
import yfinance as yf


def isTickerValid(ticker):
    try:
        aTicker = yf.Ticker(ticker)
        aTicker.info
        return True
    except:
        return False
    

def getNameToTicker(ticker):
    companyName = ""
    try:
        aTicker = yf.Ticker(ticker)
        companyName = aTicker.info['shortName']
        # print('_____________',  file=sys.stderr)
        # print(str(aTicker.info),  file=sys.stderr)
    except:
        try:
                companyName= aTicker.info['longName']

        except:
            companyName = " Name not found"
    return companyName


def getCorrelationDiagram(ticker1, ticker2):
    
    result = [['2017-01-01',0.1],['2018-01-01',0.8],['2018-01-01',0.5] ]
    
    return result

def getCorrelationMatrix(tickers):
    
    result = [[1.0,0.1,0.25,0.1],[0.3,1.0,0.2,0.1],[0.6,0.5,1.0,0.1],[0.6,0.5,0.4,1.0] ]
    
    return result