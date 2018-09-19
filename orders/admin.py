from django.contrib import admin

from .models import ToppingList, Price, Style, Pizza, Topping, Pasta, Salad, DinnerPlatter, Sub, Extra
# Register your models here.
admin.site.register(Price)
admin.site.register(ToppingList)
admin.site.register(Style)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
admin.site.register(Sub)
admin.site.register(Extra)


