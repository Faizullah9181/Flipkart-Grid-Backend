from django.db import models
from user.models import Users
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    type = models.CharField(max_length=255 )


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    gender = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    image = models.CharField(max_length=2555)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductInventory(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productId.name
    

class Cart(models.Model):
    productInventoryId = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.productInventoryId.productId.name

class WishList(models.Model):
    productInventoryId = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.productInventoryId.productId.name
    

class UserHistory(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        return self.productId.name+" "+self.created_by.name