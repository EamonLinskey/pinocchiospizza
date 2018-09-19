from django.db import models



# Create your models here.
class Price(models.Model):
	small = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	large = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
   		return f'Small:{self.small} Large:{self.large}'

class ToppingList(models.Model):
	name = models.CharField(max_length=32)
	noTop = models.ForeignKey(Price, on_delete=models.CASCADE,  related_name='noTopPrice')
	oneTop = models.ForeignKey(Price, on_delete=models.CASCADE,  related_name='oneTopPrice')
	twoTop = models.ForeignKey(Price, on_delete=models.CASCADE,  related_name='twoTopPrice')
	threeTop = models.ForeignKey(Price, on_delete=models.CASCADE,  related_name='threeTopPrice')
	specialTop = models.ForeignKey(Price, on_delete=models.CASCADE,  related_name='specialTopPrice')
	def __str__(self):
		return 	f'{self.name}'
	def listToppings(self):
		return {self.noTop, self.oneTop, self.twoTop, self.threeTop, self.specialTop}




class Style(models.Model):
	name = models.CharField(max_length=32)
	PriceList = models.ForeignKey(ToppingList, on_delete=models.CASCADE)
	def __str__(self):
   		return f'{self.name}'
	

class Pizza(models.Model):
	style = models.ForeignKey(Style, on_delete=models.CASCADE)
	def __str__(self):
   		return f'{self.style.name}'

class Topping(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
   		return self.name

class Pasta(models.Model):
	name = models.CharField(max_length=32)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	def __str__(self):
   		return self.name

class Salad(models.Model):
	name = models.CharField(max_length=32)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	def __str__(self):
   		return self.name	

class DinnerPlatter(models.Model):
	name = models.CharField(max_length=32)
	size = models.ForeignKey(Price, on_delete=models.CASCADE)
	def __str__(self):
   		return self.name

class Extra(models.Model):
	name = models.CharField(max_length=32)
	price = models.ForeignKey(Price, on_delete=models.CASCADE)
	def __str__(self):
   		return self.name	

class Sub(models.Model):
	name = models.CharField(max_length=32)
	size = models.ForeignKey(Price, on_delete=models.CASCADE)
	extras = models.ManyToManyField(Extra, blank=True)
	def __str__(self):
   		return self.name


	