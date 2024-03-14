from django.db import models


class Client(models.Model):
    category = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
