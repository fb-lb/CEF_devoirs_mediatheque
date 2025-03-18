from django.db import models


class Livre(models.Model):
    name = models.fields.CharField(max_length=150)
    auteur = models.fields.CharField(max_length=150)
    borrowingDate = models.fields.DateField(auto_now_add=True)
    is_available = models.fields.BooleanField()