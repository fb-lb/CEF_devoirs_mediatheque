from django.db import models


class Book(models.Model):
    media_type = models.fields.CharField(max_length=150, default='livre')
    name = models.fields.CharField(max_length=150)
    author = models.fields.CharField(max_length=150)
    borrowing_date = models.fields.DateField(auto_now_add=True)
    is_available = models.fields.BooleanField(default=True)