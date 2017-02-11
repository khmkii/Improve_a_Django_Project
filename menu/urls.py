from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.create_new_or_edit_menu, name='menu_edit'),
    url(r'^menu/item/new/$', views.create_new_item, name="new_item"),
    url(r'^menu/(?P<pk>\d+)/', views.menu_detail, name='menu_detail'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^menu/new/$', views.create_new_or_edit_menu, name='menu_new'),
    url(r'^menu/item/(?P<pk>\d+)/edit/$', views.edit_item, name="item_edit")
]