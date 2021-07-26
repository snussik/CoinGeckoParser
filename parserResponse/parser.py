import requests
import json
import time
import sqlite3
import pathlib



birg = ['Binance', 'Gate.io', 'MEXC Global', 'PancakeSwap (v2)', 'EXMO', 
			 'KuCoin', 'Poloniex', 'Kraken', 'OKEx', 'Bittrex', 'Crex24', 'BKEX', 'YoBit']
fees = {'Binance': 0.1, 'Gate.io': 0.2, 'MEXC Global': 0.2, 'EXMO': 0.3, 'KuCoin': 0.1, 'PancakeSwap (v2)': 0.25}

def collect_markets_prices(tickers):
	markets_prices = dict()
	volumes = dict()
	for i in tickers:
		trust_score = i['trust_score']
		volume = i['converted_volume']['usd']
		if int(volume) > 1:
			market_name = i['market']['name']
			if market_name in birg:
				price = float(i['converted_last']['usd'])
				markets_prices[market_name] = price
				volumes[market_name] = int(volume)
	return markets_prices, volumes


def find_diffs(markets_prices, volumes):
	data = list()
	for k, v in markets_prices.items():
		for m, p in markets_prices.items():
			feeSell, feeBuy = 0, 0
			if k in fees.keys():
				feeSell = fees.get(k)
			if m in fees.keys():
				feeBuy = fees.get(m) 
			v = v * (1-feeSell/100)
			p = p * (1+feeBuy/100)
			if v / p > 1.01:
				v1, v2 = int(volumes.get(k)), int(volumes.get(m)) 
				data.append({'from': m, 'to': k, 'fromPrice': p, 'toPrice': v, 'volumes': min(v1, v2)})
	return data


def get_markets_info(id_):
	print(id_)
	coin_info_response = requests.get('https://api.coingecko.com/api/v3/coins/{}?localization=false&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false'.format(id_))
	if coin_info_response.status_code == 200:
		coin_data = json.loads(coin_info_response.text)
		if coin_data['asset_platform_id'] == 'ethereum':
			return None
		name = coin_data['name']
		tickers = coin_data.get('tickers')
		if len(tickers) > 1 and 'Short' not in name and 'Long' not in name:
			markets_prices, volumes = collect_markets_prices(tickers)
			if len(markets_prices) > 1:
				diff = find_diffs(markets_prices, volumes)	
				if diff:
					return [name, diff]
				else:
					print('No diff 57')
			else:
				print(markets_prices, 59)
	else:
		print('Status error 55')
		return None	



response = requests.get('https://api.coingecko.com/api/v3/coins/list?include_platform=true')
parent_dir = pathlib.Path.cwd().parent
conn = sqlite3.connect(parent_dir / 'db.sqlite3')
cur = conn.cursor()
#parserResponse_arbitsituation
command = "DELETE FROM parserResponse_arbitsituation;"
cur.execute(command)
conn.commit()

if response.status_code == 200:
	while 1:
		data = json.loads(response.text)
		for d in data:
			id_ = d['id']
			if id_ == '':
				continue
			
			data = get_markets_info(id_)
			if data:
				coin = data[0]
				command = "DELETE FROM parserResponse_arbitsituation WHERE coin = ?"
				cur.execute(command, (coin,))
				for d in data[1]:
					volume = d.get('volumes')
					conn.commit()
					m1 = d.get('from')
					m2 = d.get('to')
					p1 = float(d.get('fromPrice'))
					p2 = float(d.get('toPrice'))
					profit = float(str(p2/p1)[:4])
					command = "INSERT INTO parserResponse_arbitsituation(coin, market1, market2, volume, profit) VALUES(?, ?, ?, ?, ?);"					
					cur.execute(command, (coin, m1, m2, volume, profit))
					conn.commit()
			time.sleep(1.21)


				
		