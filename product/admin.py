from django.contrib import admin
from .models import Category, Product, ProductInventory,Cart ,WishList,UserHistory
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductInventory)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(UserHistory)
