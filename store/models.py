from django.db import models


# create Product model
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)


# create Customer model

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBESHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze')
        (MEMBERSHIP_SILVER, 'Silver')
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, primary_key=True)
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBESHIP_CHOICES, default=MEMBERSHIP_BRONZE)
