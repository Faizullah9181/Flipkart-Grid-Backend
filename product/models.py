from django.db import models

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

class ProductImage(models.Model):
    ProductInventoryId = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    image = models.CharField(max_length=2555)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)