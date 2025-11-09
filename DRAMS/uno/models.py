from django.db import models


class User(models.Model):
    name = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=29, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=500, null=True, blank=True)
    age = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class City(models.Model):
    name = models.CharField(max_length=500, null=True)
    coordinates = models.CharField(max_length=50, null=True)
    total_nodes = models.CharField(max_length=10, null=True)
    live_nodes = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.name)


class Location(models.Model):
    sc = (
        ("N", "None"),
        ("L", "Low"),
        ("M", "Medium"),
        ("H", "High")
    )
    ncc = (
        ("parking", "Police"),
        ("first-aid", "Ambulance"),
        ("fire-extinguisher", "Fire Brigade")
    )
    als = (
        ("N", "Not Sent"),
        ("Y", "Sent")
    )
    geography = models.CharField(max_length=500, null=True)
    coordinates = models.CharField(max_length=50, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    severity = models.CharField(max_length=50, null=True, choices=sc, default="N")
    population = models.BigIntegerField(null=True)
    nodal_center = models.CharField(max_length=500, null=True)
    nc_category = models.CharField(max_length=50, null=True, choices=ncc, default="first-aid")
    alert_status = models.CharField(max_length=10, null=True, choices=als, default="N")
    cctv = models.CharField(max_length=100, null=True)
    covid_status = models.CharField(max_length=5, null=True, default=0)
    fire_status = models.CharField(max_length=5, null=True, default=0)
    flood_status = models.CharField(max_length=5, null=True, default=0)

    def __str__(self):
        return str(self.geography)
