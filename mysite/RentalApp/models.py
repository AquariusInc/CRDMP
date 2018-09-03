from django.db import models

# Create your models here.
class ModelTest(models.Model):
    name = models.TextField()

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)