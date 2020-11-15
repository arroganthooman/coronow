from django.http import response
from django.test import TestCase
from django.test.client import Client
from django.urls.base import reverse

# Create your tests here.
class LandingPageTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()

    #URL Test
    def test_url_exists(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    #View Test
    def test_view_is_using_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, 'landing/landing.html')