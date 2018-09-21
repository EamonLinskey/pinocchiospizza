from django.db import models

# Create your models here.
class PriceList(models.Model):
	smallNoExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	largeNoExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	smallOneExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	largeOneExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	smallTwoExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	largeTwoExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	smallThreeExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	largeThreeExtra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	smallSpecial = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	largeSpecial = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
		return f'{self.smallNoExtra}, {self.largeNoExtra}, {self.smallOneExtra}, {self.largeOneExtra} {self.smallTwoExtra}, {self.largeTwoExtra}, {self.smallThreeExtra}, {self.largeThreeExtra}, {self.smallSpecial}, {self.largeSpecial}'


class Extra(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
   		return self.name

class Style(models.Model):
	name = models.CharField(max_length=32)
	priceList = models.ForeignKey(PriceList, on_delete=models.CASCADE)
	legalExtras = models.ManyToManyField(Extra)
	def __str__(self):
   		return f'{self.name}'

class Food(models.Model):
	name = models.CharField(max_length=32)
	style = models.ManyToManyField(Style)
	def __str__(self):
   		return f'{self.name}'



