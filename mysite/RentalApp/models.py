from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    dob = models.DateField()
    occupation = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)




class Store(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

class Stock(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    returnDate = models.DateField()
    returnStore = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='stock_return_store')


    def __str__(self):
        return str(self.car)

    def __unicode__(self):
        return str(self.car)

class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    series = models.CharField(max_length=50)
    year = models.IntegerField()
    priceNew = models.FloatField()
    engineSize = models.FloatField()
    fuelSystem = models.CharField(max_length=50)
    tankCapacity = models.FloatField()
    power = models.FloatField()
    seatingCapacity = models.IntegerField()
    standardTransmission = models.CharField(max_length=50)
    bodyType = models.CharField(max_length=50)
    drive = models.CharField(max_length=5)
    wheelBase = models.FloatField()
    image = models.TextField()

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    createDate = models.DateField()
    pickupDate = models.DateField()
    pickupStore = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='%(class)s_pickup_store')
    returnDate = models.DateField()
    returnStore = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='return_store')
    store_name = Store.name
    
    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    
class MyUser(AbstractUser):
    username = models.CharField(max_length=150, primary_key=True)
    is_management = models.BooleanField('Management Status', default=False)
    staffID = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    branchID = models.IntegerField()
    dob = models.DateField()
    
    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

class AidanStock(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='aidan_stock_car')
    returnDate = models.DateField()
    returnStore = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='aidan_stock_return_store')

    def __str__(self):
        return str(self.car)

    def __unicode__(self):
        return str(self.car)

