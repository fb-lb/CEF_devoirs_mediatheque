from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Member(models.Model):
    first_name = models.fields.CharField(max_length=30)
    last_name = models.fields.CharField(max_length=30)
    nb_current_borrowings = models.fields.IntegerField(
        default = 0,
        validators = [
            MaxValueValidator(3),
            MinValueValidator(0)
        ]
    )
    is_blocked = models.fields.BooleanField(default=False)


class BorrowableMedia(models.Model):
    name = models.fields.CharField(max_length=150)
    borrowing_date = models.fields.DateField(null=True)
    return_date = models.fields.DateField(null=True)
    is_available = models.fields.BooleanField(default=True)
    borrower = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True
    )


class Book(BorrowableMedia):
    media_type = models.fields.CharField(max_length=150, default='livre')
    author = models.fields.CharField(max_length=150)


class Cd(BorrowableMedia):
    media_type = models.fields.CharField(max_length=150, default='cd')
    artist = models.fields.CharField(max_length=150)


class Dvd(BorrowableMedia):
    media_type = models.fields.CharField(max_length=150, default='dvd')
    director = models.fields.CharField(max_length=150)


class ParlourGame(models.Model):
    media_type = models.fields.CharField(max_length=150, default='jeu de société')
    name = models.fields.CharField(max_length=150)
    creator = models.fields.CharField(max_length=150)