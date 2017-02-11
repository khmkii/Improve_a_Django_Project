import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from menu import forms, models, views


later = datetime.date.today()


class DataForTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='head chef'
        )
        self.menu = models.Menu.objects.create(
            season='Bleak Mid Winter',
            expiration_date=(datetime.date.today() + datetime.timedelta(days=20)),
        )
        self.item = models.Item.objects.create(
            name='something tasty',
            description='tastes good',
            chef=self.user,
        )
        self.ingredient = models.Ingredient.objects.create(
            name='an ingredient'
        )
        self.menu_detail_url = reverse('menu:menu_detail', kwargs={
            'pk': self.menu.pk
        })
        self.item_detail_url = reverse(
            'menu:item_detail',
            kwargs={'pk': self.item.pk}
        )
        self.edit_menu_url = reverse('menu:menu_edit', kwargs={
            'pk': self.menu.pk
        })
        self.new_menu_url = reverse('menu:menu_new')
        self.new_item_url = reverse('menu:new_item')
        self.edit_item_url = reverse(
            'menu:item_edit',
            kwargs={
                'pk': self.item.pk
            }
        )
        self.menu_data = {
            'expiration_date_day': str(later.day),
            'expiration_date_month': str(later.month),
            'expiration_date_year': str(later.year),
            'items': self.item,
            'season': 'later this year',
        }
        self.item_data = {
            'name': 'an item',
            'description': 'a new fantastic item for eating',
            'standard': '1',
            'ingredients': self.ingredient
        }


class MenuListViewTest(TestCase):

    def test_menu_list_url_resolves_to_menu_list_view(self):
        menu_list_url = reverse('menu:menu_list')
        found = resolve(menu_list_url)
        self.assertEqual(found.func, views.menu_list)

    def test_menu_list_view_returns_correct_template(self):
        response = self.client.get(reverse('menu:menu_list'))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/list_all_current_menus.html')


class MenuDetailViewTest(DataForTest):

    def test_menu_detail_url_resolves_to_menu_detail_view(self):
        found = resolve(self.menu_detail_url)

        self.assertEqual(found.func, views.menu_detail)

    def test_menu_detail_view_returns_correct_template(self):
        resp = self.client.get(self.menu_detail_url)

        self.assertTemplateUsed(resp, template_name='menu/menu_detail.html')


class ItemDetailViewTest(DataForTest):

    def test_item_detail_url_resolves_to_item_detail_view(self):

        found = resolve(self.item_detail_url)

        self.assertEqual(found.func, views.item_detail)

    def test_item_detail_returns_correct_template(self):
        resp = self.client.get(self.item_detail_url)

        self.assertTemplateUsed(resp, 'menu/detail_item.html')


class CreateOrEditMenuViewTest(DataForTest):

    def test_url_new_menu_resolves(self):
        found = resolve(self.new_menu_url)

        self.assertEqual(found.func, views.create_new_or_edit_menu)

    def test_url_edit_menu_resolves(self):
        found = resolve(self.edit_menu_url)

        self.assertEqual(found.func, views.create_new_or_edit_menu)

    def test_create_or_edit_view_get_returns_correct_template(self):
        resp = self.client.get(self.new_menu_url)
        resp2 = self.client.get(self.edit_menu_url)

        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertTemplateUsed(resp2, 'menu/menu_edit.html')

    def test_create_or_edit_view_get_uses_menu_form(self):
        resp = self.client.get(self.new_menu_url)
        resp2 = self.client.get(self.edit_menu_url)

        self.assertIsInstance(resp.context['form'], forms.MenuForm)
        self.assertIsInstance(resp2.context['form'], forms.MenuForm)

    def test_create_or_edit_menu_view_accepts_post_correct_template_used(self):
        resp = self.client.post(
            self.new_menu_url,
            data=self.menu_data
        )

        self.assertIn('later this year', resp.content.decode())
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')


class CreateNewItemViewTest(DataForTest):

    def test_url_create_new_item_resolves(self):
        found = resolve(self.new_item_url)

        self.assertEqual(found.func, views.create_new_item)

    def test_create_new_item_view_get_returns_correct_template(self):
        resp = self.client.get(self.new_item_url)

        self.assertTemplateUsed(resp, 'menu/item_new.html')

    def test_create_or_edit_view_get_uses_menu_form(self):
        resp = self.client.get(self.new_item_url)

        self.assertIsInstance(resp.context['form'], forms.ItemForm)

    def test_create_new_item_view_accepts_post(self):
        resp = self.client.post(
            self.new_item_url,
            data=self.item_data
        )

        self.assertIn('a new fantastic item for eating', resp.content.decode())


class EditItemViewTest(DataForTest):

    def test_edit_item_view_get_returns_correct_template(self):
        resp = self.client.get(self.edit_item_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_new.html')

    def test_edit_item_view_accepts_post(self):
        resp = self.client.post(
            self.edit_item_url,
            self.item_data
        )

        self.assertIn('a new fantastic item for eating', resp.content.decode())


class ItemFormTest(TestCase):

    def test_form_rejects_bad_data(self):
        form = forms.ItemForm(data={
            'name': '',
            'description': '',
            'ingredients': None,
            'standard': None,
        })

        self.assertFalse(form.is_valid())


class MenuFormTest(TestCase):

    def test_form_rejects_bad_date(self):
        form = forms.MenuForm(data={
            'season': '',
            'expiration_date': datetime.date(year=2015, month=1, day=1),
            'items': None,
        })

        self.assertFalse(form.is_valid())
        self.assertIn(
            'Menu expiration date must be in the future',
            form.errors['expiration_date']
        )
        self.assertIn('This field is required.', form.errors['items'])


class ModelTests(DataForTest):

    def test_str_menu(self):
        self.assertEqual('Bleak Mid Winter', self.menu.__str__())

    def test_absolute_url_method_menu(self):
        self.assertEqual(
            self.menu.get_absolute_url(),
            '/menu/{}/'.format(self.menu.pk)
        )

    def test_str_item(self):
        self.assertEqual('something tasty', self.item.__str__())

    def test_absolute_url_method_item(self):
        self.assertEqual(
            self.item.get_absolute_url(),
            '/menu/item/{}/'.format(self.item.pk)
        )
