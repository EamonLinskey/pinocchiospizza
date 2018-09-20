from django.db import models

# Create your models here.

class Food(models.Model):
	name = models.CharField(max_length=32)
	style = models.ForeignKey(Style, on_delete=models.CASCADE)
	def __str__(self):
   		return f'{self.name}'

class Style(models.Model):
	name = models.CharField(max_length=32)
	numExtras = models.ManyToManyField(NumExtras, on_delete=models.CASCADE)
	def __str__(self):
   		return f'{self.name}'

class NumExtras:
	name = models.CharField(max_length=32)
	sizes = models.ForeignKey(Size, on_delete=models.CASCADE)
	def __str__(self):
   		return f'{self.name}'

class Size(models.Model):
	small = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	large = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
   		return f'Small:{self.small} Large:{self.large}'

class SandwitchExtras(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
   		return self.name

class PizzaExtras(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
   		return self.name


	