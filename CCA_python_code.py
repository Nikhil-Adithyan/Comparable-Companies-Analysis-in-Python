# IMPORTING PACKAGES

import pandas as pd
import requests
import numpy as np
from termcolor import colored as cl

# EXTRACTING THE FINANCIAL METRICS

ticker = ['MSFT', 'AMZN', 'GOOGL', 'FB', 'BABA', 'NVDA', 'PYPL', 'INTC', 'NFLX', 'AAPL']

def get_metrics(stock):
    iex_api_key = 'YOUR SANDBOX API KEY'
    fundamentals = []
    
    # 1. PRICE
    
    price_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/price?token={iex_api_key}'
    raw_price = requests.get(price_url)
    price = raw_price.json()    
    fundamentals.append(price)
    
    # 2. MARKET CAP
    
    marketcap_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/stats?token={iex_api_key}'
    raw_marketcap = requests.get(marketcap_url)
    marketcap = raw_marketcap.json()['marketcap']
    fundamentals.append(marketcap)
    
    # 3. PE RATIO
    
    peRatio_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/stats?token={iex_api_key}'
    raw_peRatio = requests.get(peRatio_url)
    peRatio = raw_peRatio.json()['peRatio']
    fundamentals.append(peRatio)
    
    # 4. EBITDA
    
    ebitda_url = f'https://sandbox.iexapis.com/stable/time-series/fundamentals/{stock}/quarterly?token={iex_api_key}'
    raw_ebitda = requests.get(ebitda_url)
    ebitda = raw_ebitda.json()[0]['ebitdaReported']
    fundamentals.append(ebitda)
    
    # 5. EBIT
    
    ebit_url = f'https://sandbox.iexapis.com/stable/time-series/fundamentals/{stock}/quarterly?token={iex_api_key}'
    raw_ebit = requests.get(ebit_url)
    ebit = raw_ebit.json()[0]['ebitReported']
    fundamentals.append(ebit)
    
    # 6. REVENUE
    
    revenue_url = f'https://sandbox.iexapis.com/stable/time-series/fundamentals/{stock}/quarterly?token={iex_api_key}'
    raw_revenue = requests.get(revenue_url)
    revenue = raw_revenue.json()[0]['revenue']
    fundamentals.append(revenue)
    
    # 7. ENTERPRISE VALUE
    
    entvalue_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/advanced-stats?token={iex_api_key}'
    raw_entvalue = requests.get(entvalue_url)
    entvalue = raw_entvalue.json()['enterpriseValue']
    fundamentals.append(entvalue)
    
    print(cl(f'Extracted {stock} Fundamentals', attrs = ['bold']))
    
    return fundamentals

msft_fundamentals = get_metrics(ticker[0])
amzn_fundamentals = get_metrics(ticker[1])
googl_fundamentals = get_metrics(ticker[2])
fb_fundamentals = get_metrics(ticker[3])
baba_fundamentals = get_metrics(ticker[4])
nvda_fundamentals = get_metrics(ticker[5])
pypl_fundamentals = get_metrics(ticker[6])
intc_fundamentals = get_metrics(ticker[7])
nflx_fundamentals = get_metrics(ticker[8])
aapl_fundamentals = get_metrics(ticker[9])

# FORMATTING THE DATA

raw_data = [msft_fundamentals, amzn_fundamentals, googl_fundamentals, fb_fundamentals, baba_fundamentals, 
            nvda_fundamentals, pypl_fundamentals, intc_fundamentals, nflx_fundamentals, aapl_fundamentals]

fundamentals = pd.DataFrame(columns = ['price', 'marketcap', 'pe', 'ebitda', 'ebit', 'revenue', 'ev'])
fundamentals.iloc[:,0] = range(0, 10)

for i in range(len(fundamentals)):
    fundamentals.iloc[i] = raw_data[i]

fundamentals['symbol'] = ticker
fundamentals = fundamentals.set_index('symbol')
fundamentals

# VALUATION MULTIPLES CALCULATION

valuation_multiples = fundamentals.copy().iloc[:, 2:].drop('ev', axis = 1)
valuation_multiples = valuation_multiples.rename(columns = {'ebitda':'ev/ebitda', 'ebit':'ev/ebit', 'revenue':'ev/revenue'})

valuation_multiples.iloc[:, 1] = fundamentals['ev'] / fundamentals['ebitda']
valuation_multiples.iloc[:, 2] = fundamentals['ev'] / fundamentals['ebit']
valuation_multiples.iloc[:, 3] = fundamentals['ev'] / fundamentals['revenue']

valuation_multiples

# AVERAGE AND DIFFERENCE OF MULTIPLES

index = ['avg', 'diff']
avg_diff = pd.DataFrame(columns = ['pe', 'ev/ebitda', 'ev/ebit', 'ev/revenue'])
avg_diff.iloc[:, 0] = np.arange(0,2)

avg_diff.iloc[0] = valuation_multiples[:9].sum() / 10
avg_diff.iloc[1] = valuation_multiples.iloc[9] / avg_diff.iloc[0]
avg_diff['avg/diff'] = index
avg_diff = avg_diff.set_index('avg/diff')
avg_diff

# CALCULATING THE INTRINSIC VALUE

price_diff = raw_data[9][0] / avg_diff.iloc[1]
intrinsic_price = round((sum(price_diff) / 4), 2)
percentage_difference = round(((raw_data[9][0] / intrinsic_price) * 100), 2)

print(cl(f'The listed price of Apple : {raw_data[9][0]}', attrs = ['bold']))
print(cl(f'The intrinsic value of Apple : {intrinsic_price}', attrs = ['bold']))
if intrinsic_price > raw_data[9][0]:
    print(cl(f'The Underlying Value of Apple stock is {percentage_difference}% Higher than the Listed price', attrs = ['bold']))         
else:
    print(cl(f'The Underlying Value of Apple stock is {percentage_difference}% Lower than the Listed price', attrs = ['bold']))