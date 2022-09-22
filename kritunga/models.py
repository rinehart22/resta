
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.contrib.gis.db import models
# Create your models here.

allocation_choices = (
    ('incomplete', 'incomplete'),
    ('pending', 'pending'),
    ('complete', 'complete')
)


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category_image = models.ImageField(
        upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    product_image = models.ImageField(
        upload_to='images/', null=True, blank=True)
    #quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,)

    #location = models.ManyToManyField(Location, blank=True,null=True)

    def __str__(self):
        return self.product_name


class Location(models.Model):
    location_name = models.CharField(max_length=250)
    product = models.ManyToManyField(Products)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.location_name


# https://docs.djangoproject.com/en/4.0/ref/contrib/gis/geoquerysets/#within
# https://docs.djangoproject.com/en/4.0/ref/contrib/gis/model-api/#django.contrib.gis.db.models.GeometryField
#'%s %s %s %s' % (self.product_name, self.description, self.product_image, self.product_price)


class Chef(models.Model):
    chef_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    chef_image = models.ImageField(upload_to='images/', null=True, blank=True)
    category_name = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,)
    orders_completed = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=100)
    chef_availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.chef_name)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category_name = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,)
    product_name = models.ForeignKey(
        Products, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allocation = models.BooleanField(default=False)
    table_no = models.IntegerField(null=True, blank=True)
    prepared_by = models.ForeignKey(
        Chef, on_delete=models.SET_NULL, null=True, blank=True,)
    status = models.CharField(
        max_length=20, choices=allocation_choices, default='incomplete')

    todayorders = models.DateTimeField(auto_now=True)
    checkout_status = models.CharField(max_length=100)

# class Checkout(models.MOdel):


# class Cart(models.Model):
#     items = models.ForeignKey(
#         Products,  on_delete=models.SET_NULL, null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     product_qty = models.PositiveIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.items)

    # class Meta:
    #     db_table = "kritunga_cart"

    # def total(self):
    #     return self.product_qty * self.product_price
