from django.db import models

class Member(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
