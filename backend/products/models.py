from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=60, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
