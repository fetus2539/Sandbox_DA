from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import pdfkit
import wkhtmltopdf

cg = CoinGeckoAPI()

exchange = cg.get_exchanges_list(per_page=20)
criteria = pd.DataFrame(exchange)
criteria = criteria[['id','name','trust_score_rank']]
criteria

df = pd.DataFrame(columns=['Coin','Exchange', 'Volume', 'Volume_Criteria','Average Volume 7 Days'])

def start(ids, coins):
    
    coin = cg.get_exchanges_tickers_by_id(id=ids,coin_ids=coins)
    df_coin = pd.DataFrame(coin)
    
    if df_coin['tickers'].all() == True:
        b = False
    else:    
        d = df_coin['tickers'][0]
        d = pd.DataFrame(d)      
        b = (d.iloc[0,2] == criteria.iloc[0,1])

    volume = cg.get_coin_market_chart_by_id(id=coins, vs_currency='usd', days=7, interval='daily')
    vol = pd.DataFrame(volume['total_volumes'], columns=['Date','Volume'])
    vol['Date'] = pd.to_datetime(vol['Date'], unit='ms')
    vol = vol.iloc[:-1]

    x = []
    y = []

    if vol['Volume'].mean() > 1000e6:
        x.append(vol['Volume'].mean())
        y.append('Criteria A')

    elif (vol['Volume'].mean() < 1000e6) & (vol['Volume'].mean() >= 500e6) :
        x.append(vol['Volume'].mean())
        y.append('Criteria B')

    elif (vol['Volume'].mean() < 500e6) & (vol['Volume'].mean() >= 100e6) :
        x.append(vol['Volume'].mean())
        y.append('Criteria C')

    elif (vol['Volume'].mean() < 100e6) & (vol['Volume'].mean() >= 50e6) :
        x.append(vol['Volume'].mean())
        y.append('Criteria D')

    elif (vol['Volume'].mean() < 50e6) & (vol['Volume'].mean() >= 10e6) :
        x.append(vol['Volume'].mean())
        y.append('Criteria E')

    list = [coins, b , vol['Volume'].mean()>10e6, y, x]

    a = len(df.index)
    df.loc[a] = list

    return df


ids = 'binance'
coins = 'bitcoin','ethereum','dogecoin','maps','dopple-finance','cardano','alpha-finance','verge'

for i in range(len(coins)):
    test = coins[i]
    
    start(ids,test)


f = open('exp.html','w')
c = df.to_html()
f.write(c)
f.close()

config = pdfkit.configuration(wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

pdfkit.from_file('exp.html', 'DA.pdf',configuration=config)