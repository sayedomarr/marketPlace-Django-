from django.db import models
from categories.models import Category
import uuid

# Product model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # charfield to store the name of the product
    name = models.CharField(max_length=200, db_index=True)
    # decimalfield to store the price of the product
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    # textfield to store the description of the product (with db_index for search performance)
    description = models.TextField(blank=True)
    # imagefield to store the image of the product
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # booleanfield to store if the product is in stock
    in_stock = models.BooleanField(default=True)
    # positiveintegerfield to store the stock quantity of the product
    stock_quantity = models.PositiveIntegerField(default=0)
    # datetimefield with auto_now_add to set the date and time when the object is created
    created_at = models.DateTimeField(auto_now_add=True)
    # datetimefield with auto_now to set the date and time when the object is updated
    updated_at = models.DateTimeField(auto_now=True)
    # code field to store the code of the product and make it unique
    code = models.CharField(max_length=50, unique=True, db_index=True)

    # meta class to set the verbose name, ordering, and database table name and it's used for the admin site
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        db_table = 'products'
    
    # __str__ method to return the name of the product
    def __str__(self):
        return self.name
    
    # save method to generate a unique code for the product
    def save(self, *args, **kwargs):    
        # if the code is not set, generate a unique code for the product
        if not self.code:
            # generate a unique code for the product
            self.code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
        return self



