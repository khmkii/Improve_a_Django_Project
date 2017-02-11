from datetime import date

from django import forms
from django.forms.extras.widgets import SelectDateWidget


from .models import Menu, Item


def must_expire_in_the_future(expire):
    if expire <= date.today():
        raise forms.ValidationError(
            "Menu expiration date must be in the future"
        )


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = (
            'season',
            'expiration_date',
            'items'
        )
        widgets = {
            'expiration_date': SelectDateWidget,
        }

    def clean_expiration_date(self):
        expirate = self.cleaned_data['expiration_date']
        must_expire_in_the_future(expirate)

        return expirate


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = (
            'name',
            'description',
            'standard',
            'ingredients',
        )
