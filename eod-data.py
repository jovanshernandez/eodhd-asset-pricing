from sys import displayhook
import requests
import pandas as pd

api_key = 'YOUR_API_KEY'

def search_asset(asset, search_input, api_key):
    url = f'https://eodhistoricaldata.com/api/search/{search_input}?api_token={api_key}&type={asset}'
    results_json = requests.get(url).json()
    results_df = pd.DataFrame(results_json).drop('ISIN', axis = 1).rename(columns = {'Code':'Symbol'})
    
    return results_df

assets = pd.DataFrame(pd.Series(['stock', 'etf', 'fund', 'bonds', 'index', 'commodity', 'crypto'])).rename(columns = {0:'asset'})
asset = input('Type of asset [stock, etf, fund, bonds, index, commodity, crypto]: ')

if len(assets[assets.asset == asset]) == 0:
    print('Input Error: Asset not found')
else:
    search_input = input(f'Search {asset}: ')
    print(f'\nSearch Results for {search_input}')
    search_results = search_asset(asset, search_input, api_key)
    displayhook(search_results)
