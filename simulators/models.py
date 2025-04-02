from django.db import models


class SimulatorType(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name

class SimulatorCategory(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

class Simulators(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='simulator_img')
    link = models.URLField()
    types = models.ManyToManyField(SimulatorType)
    categories = models.ManyToManyField(SimulatorCategory)
    
    def __str__(self):
        return self.title
