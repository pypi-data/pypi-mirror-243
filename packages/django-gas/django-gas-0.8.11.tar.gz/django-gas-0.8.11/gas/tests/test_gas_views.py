from django.test import TestCase, Client
from django.urls import reverse

from model_bakery import baker

from gas.gas.core.views import GASLoginView


class GASLoginTestCase(TestCase):
    def test_load(self):
        client = Client()
        response = client.get(reverse('gas:login'))
        self.assertEqual(response.status_code, 200)


class IndexTestCase(TestCase):
    def test_load(self):
        admin_user = baker.make(
            'auth.User',
            username='admin',
            is_superuser=True,
        )

        client = Client()
        response = client.get(reverse('gas:index'))
        self.assertEqual(response.status_code, 302)

        client.force_login(admin_user)
        response = client.get(reverse('gas:index'))
        self.assertEqual(response.status_code, 200)
