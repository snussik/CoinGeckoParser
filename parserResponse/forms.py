from django import forms
from .models import ArbitSituation



markets = [('Binance', 'Binance'), ('Gate.io', 'Gate.io'), ('MEXC Global', 'MEXC Global'), ('PancakeSwap (v2)', 'PancakeSwap (v2)'), 
			('EXMO', 'EXMO'), ('KuCoin', 'KuCoin'), ('Poloniex', 'Poloniex'), 
			('Kraken', 'Kraken'), ('OKEx', 'OKEx'), ('Bittrex', 'Bittrex'), ('Crex24', 'Crex24'), ('BKEX', 'BKEX')]


class FilterForm(forms.Form):
	markets = forms.MultipleChoiceField(choices=markets, widget=forms.CheckboxSelectMultiple, required=False)
	profitUp = forms.FloatField(required=False)
	profitDown = forms.FloatField(required=False)
	volume = forms.IntegerField(required=False)
	volumeDown = forms.IntegerField(required=False)