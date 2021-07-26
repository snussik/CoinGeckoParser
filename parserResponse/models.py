from django.db import models


class ArbitSituation(models.Model):
	coin = models.CharField('Coin name', max_length=64)
	market1 = models.CharField('Market 1', max_length=32)
	market2 = models.CharField('Market 2', max_length=32)
	volume = models.IntegerField('Market volume')
	profit = models.FloatField('Profit')

	def __str__(self):
		return self.coin

	def get_coingecko_page(self):
		return 'https://www.coingecko.com/en/coins/{}'.format(self.coin)


	def save(self, *args, **kwargs):
		self.profit = float(str(self.profit)[:4])
		super(ArbitSituation, self).save(*args, **kwargs)