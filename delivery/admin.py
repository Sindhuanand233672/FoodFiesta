# from django.contrib import admin
# from .models import Customer, Restaurant

# # Register your models here.
# admin.site.register(Customer)
# admin.site.register(Restaurant)

from django.contrib import admin
from .models import Recipe
from .models import (
    Customer,
    Restaurant,
    Item,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'restaurant',
        'price',
        'is_grocery',
    )
    list_filter = ('is_grocery', 'vegetarian', 'restaurant')
    search_fields = ('name', 'restaurant__name')


admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'cooking_time',
        'vegetarian',
        'created_at',
    )

    search_fields = ('name', 'ingredients')

    list_filter = ('vegetarian',)