from django.contrib import admin

from coffee.models import *


# Register your models here.
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available_portions', 'photo')
    search_fields = ('name', )


admin.site.register(Drink, DrinkAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name', )


admin.site.register(Ingredient, IngredientAdmin)
