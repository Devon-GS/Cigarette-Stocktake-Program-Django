from django.db import models

class Cigarette(models.Model):
    barcode = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=100)
    product_sales= models.CharField(max_length=100, default=0)
    product_purchases = models.CharField(max_length=100, default=0)
    product_stock_on_hand = models.CharField(max_length=100, default=0)
    stock_level = models.CharField(max_length=100, default=0)
       
    def __str__(self):
        return self.product_name