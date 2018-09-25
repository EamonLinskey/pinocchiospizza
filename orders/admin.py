from django.contrib import admin

from .models import PriceList, SizeList, Style, Food, Extra
# Register your models here.
admin.site.register(PriceList)
admin.site.register(SizeList)
admin.site.register(Style)
admin.site.register(Food)
admin.site.register(Extra)



