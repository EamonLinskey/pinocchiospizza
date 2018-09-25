from django.db import models

# Create your models here.
class PriceList(models.Model):
	noExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	oneExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	twoExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	threeExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	special = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
		return f'{self.noExtra}, {self.oneExtra}, {self.twoExtra}, {self.threeExtra}, {self.special}'
	@property
	def fields(self):
		return [f.name for f in self._meta.fields]
	

class SizeList(models.Model):
	name = models.CharField(max_length=32)
	small = models.ForeignKey(PriceList, on_delete=models.CASCADE, null=True, blank=True, related_name='smallPrices')
	large = models.ForeignKey(PriceList, on_delete=models.CASCADE, null=True, blank=True, related_name='largePrices')
	def __str__(self):
		return f'{self.name}'
	@property
	def sizes(self):
		sizes = []
		if self.small != None:
			sizes.append("Small")
		if self.large != None:
			sizes.append("Large")
		return sizes

class Extra(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
   		return self.name

class Style(models.Model):
	name = models.CharField(max_length=32)
	sizeList = models.ForeignKey(SizeList, on_delete=models.CASCADE)
	legalExtras = models.ManyToManyField(Extra, blank=True)
	def __str__(self):
   		return f'{self.name}'
	def trim(self):
		return self.name.replace(" ", "")

class Food(models.Model):
	name = models.CharField(max_length=32)
	style = models.ManyToManyField(Style)
	def __str__(self):
   		return f'{self.name}'



