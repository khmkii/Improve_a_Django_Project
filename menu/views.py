from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from menu import models
from menu import forms


def menu_list(request):
    menus = models.Menu.objects.prefetch_related('items').filter(
        Q(expiration_date__gte=timezone.now().date()) |
        Q(expiration_date__isnull=True)
    ).order_by('-expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu.objects.prefetch_related('items'), pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_or_edit_menu(request, pk=None):
    """
     POST DATA:
        'expiration_date_day': ['int'],
        'expiration_date_month': ['int'],
        'expiration_date_year': ['int'],
        'items': ['int'],
        'season': [string]
    """
    if pk:
        menu = models.Menu.objects.get(pk=pk)
        form = forms.MenuForm(instance=menu)
        if request.method == 'POST':
            form = forms.MenuForm(data=request.POST, instance=menu)
            if form.is_valid():
                for item in menu.items.all():
                    item.menu_set.remove(menu)
                menu = form.save()
                return redirect(menu.get_absolute_url())
        return render(
            request,
            'menu/menu_edit.html',
            {'form': form, 'menu': menu})
    else:
        form = forms.MenuForm()
        if request.method == "POST":
            form = forms.MenuForm(request.POST)
            if form.is_valid():
                menu = form.save()
                for item in menu.items.all():
                    item.menu_set.add(menu)
                return redirect(menu.get_absolute_url())
        return render(
            request,
            'menu/menu_edit.html',
            {'form': form}
        )


def create_new_item(request):
    form = forms.ItemForm()
    if request.method == 'POST':
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.chef = request.user
            item.save()
            for ing in item.ingredients.all():
                ing.item_set.add(item)
            return redirect(item.get_absolute_url())
    return render(
        request=request,
        template_name='menu/item_new.html',
        context={'form': form}
    )


def edit_item(request, pk):
    item = models.Item.objects.get(pk=pk)
    form = forms.ItemForm(instance=item)
    if request.method == 'POST':
        form = forms.ItemForm(data=request.POST)
        if form.is_valid():
            for ing in item.ingredients.all():
                ing.ingredients.remove(item)
            item = form.save(commit=False)
            item.chef = request.user
            item.save()
            for ing in item.ingredients.all():
                ing.item_set.add(item)
            return redirect(item.get_absolute_url())
    return render(
        request=request,
        template_name='menu/item_new.html',
        context={
            'item': item,
            'form': form,
        }
    )
