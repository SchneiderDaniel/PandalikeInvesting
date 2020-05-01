
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