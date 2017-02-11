from datetime import date

from django.core.urlresolvers import reverse
from django.db import models


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item')
    created_date = models.DateField(
            default=date.today
    )
    expiration_date = models.DateField(
            blank=True, null=True)

    class Meta:
        ordering = ['expiration_date',]

    def __str__(self):
        return self.season

    def get_absolute_url(self):
        return reverse(
            'menu:menu_detail',
            kwargs={
                'pk': self.pk
            }
        )


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateField(
            default=date.today)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient', related_name='ingredients')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'menu:item_detail',
            kwargs={
                'pk': self.pk
            }
        )


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
