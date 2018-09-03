from django.db import models

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
    name = models.CharField(max_length=50, primary_key=True)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    series = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    priceNew = models.FloatField()
    engineSize = models.FloatField()
    fuelSystem = models.CharField(max_length=50)
    tankCapacity = models.FloatField()
    power = models.FloatField()
    seatingCapacity = models.FloatField()
    standardTransmission = models.CharField(max_length=50)
    bodyType = models.CharField(max_length=50)
    drive = models.CharField(max_length=5)
    wheelBase = models.FloatField()

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class Order(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)