from django.contrib import admin

from .models import PriceList, Style, Food, Extra
# Register your models here.
admin.site.register(PriceList)
admin.site.register(Style)
admin.site.register(Food)
admin.site.register(Extra)



