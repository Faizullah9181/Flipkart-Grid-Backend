from django.contrib import admin
from .models import Product,Cart ,WishList,UserHistory,Order,RequestedProducts
# Register your models here.


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(UserHistory)
admin.site.register(Order)
admin.site.register(RequestedProducts)
