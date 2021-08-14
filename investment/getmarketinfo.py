import requests 
import pandas as pd
import datetime

headers = { "Host": "finance.daum.net", "Connection": "keep-alive", "Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36", "Referer": "http://finance.daum.net/domestic/all_quotes", "Accept-Encoding": "gzip, deflate", "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7", } 

def get_symbol_name(market="KOSPI") : 
	url = "http://finance.daum.net/api/quotes/sectors?fieldName=&order=&perPage=&market={}&page=&changes=UPPER_LIMIT%2CRISE%2CEVEN%2CFALL%2CLOWER_LIMIT".format(market) 
	r = requests.get(url, headers=headers) 
	results = [] 

	for category in r.json()['data'] : 
		stocks = category['includedStocks'] 
		results += stocks 
	return results

if __name__ == '__main__': 
	markets = ["KOSPI", "KOSDAQ"] 
	codes = []

	for market in markets : 
		codes += get_symbol_name(market=market)
	
	res_list = [] 

	for i in range(len(codes)): 
		if codes[i] not in codes[i + 1:]: 
			res_list.append(codes[i]) 

	codes = res_list

	df = pd.DataFrame(codes) 
	df.to_csv('market_{:%Y%m%d}.csv'.format(datetime.datetime.now()), encoding="euc-kr", index=False)